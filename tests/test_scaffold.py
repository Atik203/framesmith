import csv
import json
import re
from pathlib import Path

import check_env
import common
import validate
import yaml

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "schemas" / "examples"
BRAND = ROOT / "configs" / "brands" / "lanternfall.yaml"


def load_example(kind: str) -> dict:
    return json.loads((EXAMPLES / f"{kind}.example.json").read_text(encoding="utf-8"))


def load_brand() -> dict:
    return yaml.safe_load(BRAND.read_text(encoding="utf-8"))


# --- schemas and examples -------------------------------------------------------------------


def test_examples_are_valid():
    for kind in validate.KINDS:
        errors, _ = validate.validate(kind, load_example(kind))
        assert errors == [], f"{kind}: {errors}"


def test_script_example_has_no_warnings():
    _, warnings = validate.validate("script", load_example("script"))
    assert warnings == []


def test_render_spec_example_has_no_warnings():
    _, warnings = validate.validate("render_spec", load_example("render_spec"))
    assert warnings == []


def test_script_missing_hook_is_rejected():
    data = load_example("script")
    del data["hook"]
    errors, _ = validate.validate("script", data)
    assert any("hook" in e for e in errors)


def test_script_duration_mismatch_is_rejected():
    data = load_example("script")
    data["estimated_duration_seconds"] = 90
    errors, _ = validate.validate("script", data)
    assert any("estimated_duration_seconds" in e for e in errors)


def test_script_bad_index_is_rejected():
    data = load_example("script")
    data["script"][1]["index"] = 5
    errors, _ = validate.validate("script", data)
    assert any("index" in e for e in errors)


def test_short_script_requires_six_to_ten_segments():
    too_short = load_example("script")
    too_short["script"] = too_short["script"][:5]
    too_short["estimated_duration_seconds"] = sum(
        segment["duration_seconds"] for segment in too_short["script"]
    )
    assert any("script" in error for error in validate.validate("script", too_short)[0])

    too_long = load_example("script")
    template = too_long["script"][0]
    too_long["script"] = [dict(template, index=index) for index in range(1, 12)]
    too_long["estimated_duration_seconds"] = sum(
        segment["duration_seconds"] for segment in too_long["script"]
    )
    assert any("script" in error for error in validate.validate("script", too_long)[0])


def test_idea_score_out_of_range_is_rejected():
    data = load_example("idea")
    data["ideas"][0]["novelty"] = 9
    assert validate.validate("idea", data)[0]


def test_render_spec_dimensions_follow_content_type():
    short = load_example("render_spec")
    short["width"], short["height"] = 1920, 1080
    assert validate.validate("render_spec", short)[0]

    long_form = load_example("render_spec")
    long_form.update(content_type="long_form", width=1920, height=1080)
    assert validate.validate("render_spec", long_form)[0] == []

    wrong = load_example("render_spec")
    wrong["content_type"] = "long_form"
    assert validate.validate("render_spec", wrong)[0]


def test_render_spec_unknown_motion_is_rejected():
    data = load_example("render_spec")
    data["scenes"][0]["motion"] = "spin"
    assert validate.validate("render_spec", data)[0]


def test_render_spec_rejects_empty_scenes():
    data = load_example("render_spec")
    data["scenes"] = []
    errors, _ = validate.validate("render_spec", data)
    assert any("scenes" in error for error in errors)


def test_short_render_spec_requires_six_to_ten_scenes():
    data = load_example("render_spec")
    data["scenes"] = data["scenes"][:5]
    errors, _ = validate.validate("render_spec", data)
    assert any("scenes" in error for error in errors)


def test_render_spec_requires_canonical_thirty_fps():
    data = load_example("render_spec")
    data["fps"] = 24
    errors, _ = validate.validate("render_spec", data)
    assert any("fps" in error for error in errors)


def test_render_spec_scene_gaps_and_overlaps_are_errors():
    gap = load_example("render_spec")
    gap["scenes"][1]["start"] += 1
    gap_errors, _ = validate.validate("render_spec", gap)
    assert any("gap or overlap" in error for error in gap_errors)

    overlap = load_example("render_spec")
    overlap["scenes"][1]["start"] -= 1
    overlap_errors, _ = validate.validate("render_spec", overlap)
    assert any("gap or overlap" in error for error in overlap_errors)


def test_render_spec_must_cover_its_full_duration():
    data = load_example("render_spec")
    data["duration_seconds"] += 2
    errors, _ = validate.validate("render_spec", data)
    assert any("before the video duration" in error for error in errors)


# --- log, brand, env ------------------------------------------------------------------------


def test_log_csv_header_matches_columns():
    with (ROOT / "log.csv").open(newline="", encoding="utf-8") as handle:
        assert next(csv.reader(handle)) == common.LOG_COLUMNS


def test_brand_config_is_lanternfall():
    config = load_brand()
    assert config["brand_id"] == "lanternfall"
    assert config["name"] == "Lanternfall"
    assert config["content_id_prefix"] == "lf"
    short, long_form = config["formats"]["short"], config["formats"]["long_form"]
    assert (short["width"], short["height"]) == (1080, 1920)
    assert (long_form["width"], long_form["height"]) == (1920, 1080)
    assert long_form["max_per_week"] <= 2


def test_brand_lists_exist_for_variation_rules():
    config = load_brand()
    assert len(config["story_structures"]) >= config["variation_rules"]["min_story_structures"]
    for key in ("hook_families", "narrator_styles", "visual_treatments"):
        assert config[key], key


def test_codename_not_in_public_brand_fields():
    public = {k: v for k, v in load_brand().items() if k != "internal_codename"}
    assert "framesmith" not in json.dumps(public).lower()


def test_env_example_uses_prefix_and_has_no_secrets():
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        assert key.startswith("FRAMESMITH_"), key
        if key.endswith("_API_KEY"):
            assert value == "", f"{key} must be empty in .env.example"
    assert "FRAMESMITH_PUBLISHING_ENABLED=false" in text


def test_no_api_keys_in_repo_text_files():
    patterns = [
        r"AIza[0-9A-Za-z_\-]{35}",
        r"gsk_[A-Za-z0-9]{20,}",
        r"sk-or-v1-[A-Za-z0-9]{20,}",
        r"sk-[A-Za-z0-9]{32,}",
        r"hf_[A-Za-z0-9]{30,}",
    ]
    suffixes = {".md", ".py", ".json", ".yaml", ".yml", ".csv", ".txt", ".toml", ".example"}
    skip = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or skip & set(path.relative_to(ROOT).parts):
            continue
        if path.name == ".env" or (path.suffix not in suffixes and path.name != ".env.example"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns:
            assert not re.search(pattern, text), f"possible API key in {path}"


# --- blueprint and docs stay in sync with the code ------------------------------------------


def test_blueprint_log_columns_match_code():
    text = (ROOT / "blueprint.md").read_text(encoding="utf-8")
    match = re.search(r"`log\.csv` columns: `([^`]+)`", text)
    assert match, "R14 tracking-log row not found"
    assert [c.strip() for c in match.group(1).split(",")] == common.LOG_COLUMNS


def test_blueprint_known_conflicts_stay_fixed():
    text = (ROOT / "blueprint.md").read_text(encoding="utf-8")
    for stale in (
        "render/remotion",
        "kinetic_v2",
        "max_duration_seconds: 55\n",
        "Generate 18–35 still",
        "tts_engine: qwen3_tts",
    ):
        assert stale not in text, stale
    for required in ("### R13.", "### R14.", "Revision 1.3, repo scaffold", "Lanternfall"):
        assert required in text, required


def test_roadmap_has_checkboxes_and_done_items():
    text = (ROOT / "Roadmap.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^\s*- \[ \]", text, re.MULTILINE)) > 20
    assert len(re.findall(r"^\s*- \[x\]", text, re.MULTILINE)) > 5


def test_agents_md_points_to_roadmap_and_blueprint():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Roadmap.md" in text and "blueprint.md" in text


# --- check_env ------------------------------------------------------------------------------


def test_provider_status_reports_each_state():
    env = {
        "FRAMESMITH_GEMINI_API_KEY": "a",
        "FRAMESMITH_GEMINI_MODEL": "m",
        "FRAMESMITH_GROQ_API_KEY": "b",
        "FRAMESMITH_OPENROUTER_MODEL": "m",
    }
    states = {msg.split(":")[0]: status for status, msg in check_env.provider_status(env)}
    assert states["llm gemini"] == "OK"
    assert states["llm groq"] == "WARN"  # key without model
    assert states["llm openrouter"] == "WARN"  # model without key
    assert states["llm ollama"] == "OPT"


def test_provider_status_never_prints_key_text():
    env = {"FRAMESMITH_GEMINI_API_KEY": "SECRET-VALUE", "FRAMESMITH_GEMINI_MODEL": "m"}
    assert all("SECRET-VALUE" not in msg for _, msg in check_env.provider_status(env))


# --- common helpers -------------------------------------------------------------------------


def test_env_file_parsing_strips_comments_and_quotes(tmp_path):
    path = tmp_path / ".env"
    path.write_text("# c\nA=1  # note\nB='two'\nC=\n", encoding="utf-8")
    assert common.parse_env_file(path) == {"A": "1", "B": "two", "C": ""}


def test_kill_switches():
    import pytest

    with pytest.raises(common.KillSwitchError):
        common.require_generation_enabled({"FRAMESMITH_GENERATION_ENABLED": "false"})
    common.require_generation_enabled({})
    with pytest.raises(common.KillSwitchError):
        common.require_publishing_enabled({})
    common.require_publishing_enabled({"FRAMESMITH_PUBLISHING_ENABLED": "true"})


def test_next_content_id_uses_scripts_and_log(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "lf-short-003.json").write_text("{}", encoding="utf-8")
    (tmp_path / "scripts" / "lf-short-003.meta.json").write_text("{}", encoding="utf-8")
    rows = [{"content_id": "lf-short-007"}, {"content_id": "lf-long-009"}]
    assert common.next_content_id("lf", "short", tmp_path, rows) == "lf-short-008"
    assert common.next_content_id("lf", "long", tmp_path, rows) == "lf-long-010"
    assert common.next_content_id("lf", "short", tmp_path / "missing") == "lf-short-001"
