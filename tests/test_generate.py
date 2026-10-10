import json
import re
from pathlib import Path

import common
import generate
import httpx
import validate

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "schemas" / "examples"
KEY = "key-openrouter-abcdef"


def example(kind):
    return json.loads((EXAMPLES / f"{kind}.example.json").read_text(encoding="utf-8"))


def env_for(tmp_path, **extra):
    return {
        "FRAMESMITH_LLM_PROVIDERS": "openrouter",
        "FRAMESMITH_OPENROUTER_API_KEY": KEY,
        "FRAMESMITH_OPENROUTER_MODEL": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "FRAMESMITH_DATA_DIR": str(tmp_path / "v1"),
        **extra,
    }


def client_returning(payload, bodies=None):
    def handler(request):
        if bodies is not None:
            bodies.append(json.loads(request.content))
        text = payload if isinstance(payload, str) else json.dumps(payload)
        return httpx.Response(200, json={"choices": [{"message": {"content": text}}]})

    return httpx.Client(transport=httpx.MockTransport(handler))


def run(argv, env, client):
    return generate.main(argv, env=env, client=client, sleep=lambda _: None)


def raw_script():
    """A model-style reply: right content, wrong deterministic fields."""
    data = example("script")
    data.update(content_id="made-up-id", estimated_duration_seconds=99, niche="wrong")
    del data["content_type"], data["parent_content_id"]
    return data


def test_ideas_are_written_with_meta(tmp_path, capsys):
    env = env_for(tmp_path)
    code = run(["ideas", "--count", "2"], env, client_returning(example("idea")))
    assert code == 0
    files = [p for p in (tmp_path / "v1" / "ideas").glob("ideas-*.json") if ".meta" not in p.name]
    assert len(files) == 1
    assert validate.validate("idea", json.loads(files[0].read_text(encoding="utf-8")))[0] == []
    meta = json.loads(files[0].with_name(files[0].stem + ".meta.json").read_text(encoding="utf-8"))
    assert meta["provider"] == "openrouter" and meta["prompt_id"] == "story_idea_v1"
    assert "The Forgotten Neighbor" in capsys.readouterr().out


def test_ideas_too_few_fails_after_retries(tmp_path):
    code = run(["ideas", "--count", "5"], env_for(tmp_path), client_returning(example("idea")))
    assert code == 1


def test_ideas_prompt_avoids_earlier_titles(tmp_path):
    env = env_for(tmp_path)
    scripts = tmp_path / "v1" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "lf-short-001.json").write_text(
        json.dumps({"working_title": "The Doorbell At 3:17"}), encoding="utf-8"
    )
    bodies: list = []
    run(["ideas", "--count", "2"], env, client_returning(example("idea"), bodies))
    prompt = bodies[0]["messages"][1]["content"]
    assert "The Doorbell At 3:17" in prompt


def test_script_from_premise_sets_deterministic_fields(tmp_path):
    env = env_for(tmp_path)
    code = run(
        ["script", "--premise", "A doorbell rings at 3:17 every night."],
        env,
        client_returning(raw_script()),
    )
    assert code == 0
    out = tmp_path / "v1" / "scripts" / "lf-short-001.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["content_id"] == "lf-short-001"
    assert data["niche"] == "ai_stories" and data["content_type"] == "short"
    assert data["estimated_duration_seconds"] == 38
    assert validate.validate("script", data)[0] == []
    meta = json.loads(out.with_name("lf-short-001.meta.json").read_text(encoding="utf-8"))
    brand = common.load_brand()
    assert meta["story_structure"] == brand["story_structures"][0]
    assert meta["prompt_id"] == "story_writer_v1" and meta["source"] == "premise"


def test_second_script_gets_next_id_and_next_structure(tmp_path):
    env = env_for(tmp_path)
    for _ in range(2):
        assert run(["script", "--premise", "p"], env, client_returning(raw_script())) == 0
    scripts = tmp_path / "v1" / "scripts"
    metas = {
        name: json.loads((scripts / f"{name}.meta.json").read_text(encoding="utf-8"))
        for name in ("lf-short-001", "lf-short-002")
    }
    structures = common.load_brand()["story_structures"]
    assert metas["lf-short-001"]["story_structure"] == structures[0]
    assert metas["lf-short-002"]["story_structure"] == structures[1]


def test_script_from_idea_file_uses_picked_idea(tmp_path):
    env = env_for(tmp_path)
    idea_file = tmp_path / "ideas.json"
    idea_file.write_text(json.dumps(example("idea")), encoding="utf-8")
    bodies: list = []
    code = run(
        ["script", "--idea-file", str(idea_file), "--pick", "2"],
        env,
        client_returning(raw_script(), bodies),
    )
    assert code == 0
    prompt = bodies[0]["messages"][1]["content"]
    assert "The Forgotten Neighbor" in prompt and "Message From Ten Years" not in prompt
    assert '"working_title"' in prompt  # the JSON shape hint is appended


def test_pick_out_of_range_fails(tmp_path):
    idea_file = tmp_path / "ideas.json"
    idea_file.write_text(json.dumps(example("idea")), encoding="utf-8")
    code = run(
        ["script", "--idea-file", str(idea_file), "--pick", "9"],
        env_for(tmp_path),
        client_returning(raw_script()),
    )
    assert code == 1


def test_existing_script_is_not_overwritten_without_force(tmp_path):
    env = env_for(tmp_path)
    argv = ["script", "--premise", "p", "--content-id", "lf-short-009"]
    assert run(argv, env, client_returning(raw_script())) == 0
    assert run(argv, env, client_returning(raw_script())) == 1
    assert run([*argv, "--force"], env, client_returning(raw_script())) == 0


def test_kill_switch_blocks_generation_before_any_request(tmp_path):
    def handler(request):
        raise AssertionError("no request may be made while generation is off")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    env = env_for(tmp_path, FRAMESMITH_GENERATION_ENABLED="false")
    assert run(["ideas"], env, client) == 1
    assert run(["script", "--premise", "p"], env, client) == 1


def test_duration_and_structure_are_validated(tmp_path):
    env = env_for(tmp_path)
    client = client_returning(raw_script())
    assert run(["script", "--premise", "p", "--duration", "90"], env, client) == 1
    assert run(["script", "--premise", "p", "--structure", "nonsense"], env, client) == 1


def test_next_structure_rotates_and_wraps():
    structures = ["a", "b", "c"]
    assert generate.next_structure(structures, "") == "a"
    assert generate.next_structure(structures, "a") == "b"
    assert generate.next_structure(structures, "c") == "a"
    assert generate.next_structure(structures, "unknown") == "a"


def test_normalize_script_overrides_model_fields():
    fixed = generate.normalize_script(raw_script(), "lf-short-004")
    assert fixed["content_id"] == "lf-short-004"
    assert [s["index"] for s in fixed["script"]] == list(range(1, 8))
    assert fixed["estimated_duration_seconds"] == 38
    assert generate.normalize_script(["not", "a", "dict"], "x") == ["not", "a", "dict"]


def test_prompt_files_load_and_use_only_known_variables():
    known = {
        "story_idea_v1.md": {"count", "story_structure", "seed_topic", "avoid_similar_to"},
        "story_writer_v1.md": {
            "content_id",
            "premise",
            "story_structure",
            "target_duration_seconds",
            "character_identity",
        },
    }
    for name, allowed in known.items():
        prompt = generate.load_prompt(name)
        assert prompt["system"] and prompt["user"] and prompt["id"] == name.removesuffix(".md")
        used = set(re.findall(r"\{\{(\w+)\}\}", prompt["user"] + prompt["system"]))
        assert used <= allowed, f"{name} uses unknown variables: {used - allowed}"
        assert used, f"{name} has no variables"


def test_fill_rejects_unknown_variable():
    import pytest

    with pytest.raises(KeyError):
        generate.fill("hello {{missing}}", {})


def test_character_block_handles_empty_and_filled_brand():
    assert "invent one" in generate.character_block({"character_identity": [{"name": None}]})
    block = generate.character_block({"character_identity": [{"name": "Kai", "hair": "black"}]})
    assert "name: Kai" in block and "hair: black" in block
