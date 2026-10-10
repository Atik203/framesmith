#!/usr/bin/env python3
"""Generate story ideas or a timed script with free-tier LLMs (blueprint R5, R11 Day 1).

    python scripts/generate.py ideas [--count 10] [--seed TEXT] [--structure NAME]
    python scripts/generate.py script --idea-file v1/ideas/ideas-XXXX.json --pick 2
    python scripts/generate.py script --premise "Your own one-sentence premise" [--duration 45]

Output is validated against schemas/ (up to FRAMESMITH_LLM_MAX_RETRIES attempts per provider,
then the next provider). Needs API keys and model names in .env (see .env.example).
Exit code: 0 ok, 1 failed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import common
import llm
import validate

PROMPT_DIR = common.ROOT / "prompts" / "niches" / "ai_stories"
IDEA_PROMPT = "story_idea_v1.md"
SCRIPT_PROMPT = "story_writer_v1.md"
NICHE = "ai_stories"
SHORT_SECONDS = (30, 55)

SHAPE_IDEAS = """{
  "ideas": [
    {
      "title": "short title",
      "one_sentence_premise": "one sentence",
      "hook": "the first spoken line",
      "twist": "the reveal or payoff",
      "visual_potential": 4,
      "novelty": 3,
      "production_difficulty": 2,
      "policy_risk": 1
    }
  ]
}"""

SHAPE_SCRIPT = """{
  "working_title": "short title",
  "hook": "the first spoken sentence",
  "script": [
    {
      "index": 1,
      "text": "narration for this segment",
      "duration_seconds": 4.0,
      "emotion": "one word",
      "visual": "one still image: subject, setting, framing, light"
    }
  ],
  "cta": null,
  "estimated_duration_seconds": 45
}"""


def load_prompt(name: str, prompt_dir: Path = PROMPT_DIR) -> dict[str, str]:
    """Read a prompt file: front matter (id), then `## SYSTEM` and `## USER` sections."""
    text = (prompt_dir / name).read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    front = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if front:
        for line in front.group(1).splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        text = text[front.end() :]
    system = re.search(r"^## SYSTEM\s*\n(.*?)(?=^## USER)", text, re.DOTALL | re.MULTILINE)
    user = re.search(r"^## USER\s*\n(.*)$", text, re.DOTALL | re.MULTILINE)
    if not system or not user:
        raise ValueError(f"{name}: needs '## SYSTEM' and '## USER' sections")
    return {
        "id": meta.get("id", name),
        "system": system.group(1).strip(),
        "user": user.group(1).strip(),
    }


def fill(template: str, values: dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise KeyError(f"prompt variable {key!r} has no value")
        return str(values[key])

    return re.sub(r"\{\{(\w+)\}\}", replace, template)


def known_titles(data: Path, limit: int = 40) -> list[str]:
    """Titles of earlier ideas and scripts, so new ideas avoid repeating them (R7)."""
    titles: list[str] = []
    for path in sorted((data / "ideas").glob("*.json")):
        if path.name.endswith(".meta.json"):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        titles += [i.get("title", "") for i in payload.get("ideas", []) if isinstance(i, dict)]
    for path in common.script_files(data):
        try:
            titles.append(json.loads(path.read_text(encoding="utf-8")).get("working_title", ""))
        except (OSError, json.JSONDecodeError):
            continue
    return list(dict.fromkeys(t for t in titles if t))[-limit:]


def last_structure(data: Path) -> str:
    """Story structure of the most recently generated script, from its .meta.json sidecar."""
    metas = sorted((data / "scripts").glob("*.meta.json"), key=lambda p: p.stat().st_mtime)
    for path in reversed(metas):
        try:
            value = json.loads(path.read_text(encoding="utf-8")).get("story_structure", "")
        except (OSError, json.JSONDecodeError):
            continue
        if value:
            return value
    return ""


def next_structure(structures: list[str], last: str) -> str:
    """Rotate through the brand's structures so none repeats back to back (R7)."""
    if last in structures:
        return structures[(structures.index(last) + 1) % len(structures)]
    return structures[0]


def character_block(brand: dict) -> str:
    people = brand.get("character_identity") or []
    fields = (
        "name",
        "age_range",
        "hair",
        "face_shape",
        "clothing",
        "palette",
        "distinguishing_props",
    )
    for person in people:
        parts = [f"{f.replace('_', ' ')}: {person[f]}" for f in fields if person.get(f)]
        if parts:
            return "; ".join(parts)
    return (
        "none defined yet: invent one recurring original character and describe them "
        "identically in every visual"
    )


def normalize_script(data: Any, content_id: str) -> Any:
    """Set the deterministic fields in code instead of trusting the model (blueprint R14)."""
    if not isinstance(data, dict):
        return data
    fixed = dict(data)
    fixed.update(
        content_id=content_id,
        content_type="short",
        parent_content_id=None,
        niche=NICHE,
        language="en",
    )
    fixed.setdefault("cta", None)
    segments = fixed.get("script")
    if isinstance(segments, list):
        for number, segment in enumerate(segments, start=1):
            if isinstance(segment, dict):
                segment["index"] = number
        try:
            total = sum(float(s["duration_seconds"]) for s in segments)
        except (KeyError, TypeError, ValueError):
            total = 0.0
        if total > 0:
            fixed["estimated_duration_seconds"] = round(total, 2)
    return fixed


def format_ideas(ideas: list[dict[str, Any]]) -> str:
    lines = [" #  rank  vis nov dif risk  title"]
    for number, idea in enumerate(ideas, start=1):
        rank = (
            idea["visual_potential"]
            + idea["novelty"]
            - idea["production_difficulty"]
            - idea["policy_risk"]
        )
        lines.append(
            f"{number:>2}  {rank:>4}  {idea['visual_potential']:>3} {idea['novelty']:>3} "
            f"{idea['production_difficulty']:>3} {idea['policy_risk']:>4}  {idea['title']}"
        )
    lines.append("rank = visual_potential + novelty - production_difficulty - policy_risk")
    return "\n".join(lines)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_meta(path: Path, meta: dict[str, Any]) -> Path:
    meta_path = path.with_name(path.stem + ".meta.json")
    write_json(meta_path, meta)
    return meta_path


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def run_ideas(
    args: argparse.Namespace,
    env: dict[str, str],
    client: Any = None,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    common.require_generation_enabled(env)
    data = common.data_dir(env)
    brand = common.load_brand(env.get("FRAMESMITH_BRAND") or "framesmith")
    if args.structure and args.structure not in brand["story_structures"]:
        raise ValueError(
            f"unknown structure {args.structure!r}; use one of {brand['story_structures']}"
        )
    prompt = load_prompt(IDEA_PROMPT)
    user = fill(
        prompt["user"],
        {
            "count": args.count,
            "story_structure": args.structure or "mixed: use a different structure for each idea",
            "seed_topic": args.seed or "(none)",
            "avoid_similar_to": "; ".join(known_titles(data)) or "(none)",
        },
    )
    user += "\n\nReturn exactly this JSON shape (values are placeholders):\n" + SHAPE_IDEAS

    def check(payload: Any) -> tuple[Any, list[str]]:
        problems = validate.schema_errors("idea", payload)
        if not problems and len(payload["ideas"]) < args.count:
            problems.append(f"expected {args.count} ideas, got {len(payload['ideas'])}")
        if not problems:
            payload = {"ideas": payload["ideas"][: args.count]}
        return payload, problems

    result = llm.generate_json(prompt["system"], user, check, env, client=client, sleep=sleep)
    out = args.out or data / "ideas" / f"ideas-{datetime.now(UTC).strftime('%Y%m%d-%H%M')}.json"
    write_json(out, result.data)
    write_meta(
        out,
        {
            "kind": "ideas",
            "provider": result.provider,
            "model": result.model,
            "prompt_id": prompt["id"],
            "attempts": result.attempts,
            "generated_at": _now(),
        },
    )
    print(format_ideas(result.data["ideas"]))
    print(
        f"\n[ OK ] {len(result.data['ideas'])} ideas -> {out} ({result.provider}: {result.model})"
    )
    print("Next: pick one, then  python scripts/generate.py script --idea-file <file> --pick N")
    return 0


def run_script(
    args: argparse.Namespace,
    env: dict[str, str],
    client: Any = None,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    common.require_generation_enabled(env)
    data = common.data_dir(env)
    brand = common.load_brand(env.get("FRAMESMITH_BRAND") or "framesmith")
    structures = brand["story_structures"]
    low, high = SHORT_SECONDS
    if not low <= args.duration <= high:
        raise ValueError(f"--duration must be {low}-{high} seconds for a Short")
    structure = args.structure or next_structure(structures, last_structure(data))
    if structure not in structures:
        raise ValueError(f"unknown structure {structure!r}; use one of {structures}")

    if args.premise:
        premise, source = args.premise.strip(), "premise"
    else:
        payload = json.loads(args.idea_file.read_text(encoding="utf-8"))
        errors = validate.schema_errors("idea", payload)
        if errors:
            raise ValueError(f"{args.idea_file} is not a valid idea file: {errors[0]}")
        ideas = payload["ideas"]
        if not 1 <= args.pick <= len(ideas):
            raise ValueError(f"--pick must be 1-{len(ideas)}")
        idea = ideas[args.pick - 1]
        premise = (
            f"{idea['title']}: {idea['one_sentence_premise']} "
            f"Hook: {idea['hook']} Twist: {idea['twist']}"
        )
        source = f"{args.idea_file.name}#{args.pick}"

    content_id = args.content_id or common.next_content_id(
        brand["content_id_prefix"], "short", data, common.read_log()
    )
    if not common.CONTENT_ID_RE.match(content_id):
        raise ValueError(f"bad content id {content_id!r}")
    out = data / "scripts" / f"{content_id}.json"
    if out.exists() and not args.force:
        raise ValueError(f"{out} already exists (use --force to overwrite)")

    prompt = load_prompt(SCRIPT_PROMPT)
    user = fill(
        prompt["user"],
        {
            "content_id": content_id,
            "premise": premise,
            "story_structure": structure,
            "target_duration_seconds": args.duration,
            "character_identity": character_block(brand),
        },
    )
    user += "\n\nReturn exactly this JSON shape (values are placeholders):\n" + SHAPE_SCRIPT
    warnings: list[str] = []

    def check(payload: Any) -> tuple[Any, list[str]]:
        payload = normalize_script(payload, content_id)
        errors, found = validate.validate("script", payload)
        warnings[:] = found
        return payload, errors

    result = llm.generate_json(prompt["system"], user, check, env, client=client, sleep=sleep)
    write_json(out, result.data)
    write_meta(
        out,
        {
            "kind": "script",
            "content_id": content_id,
            "provider": result.provider,
            "model": result.model,
            "prompt_id": prompt["id"],
            "story_structure": structure,
            "source": source,
            "attempts": result.attempts,
            "generated_at": _now(),
        },
    )
    for message in warnings:
        print(f"[WARN] {message}")
    print(f"[ OK ] {out} ({result.provider}: {result.model}, structure: {structure})")
    print(f"Log it: script_version={prompt['id']}  model_names={result.provider}:{result.model}")
    print("Next: do the human pass (R7). Edit the premise and the opening lines so they are yours.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ideas = sub.add_parser("ideas", help="generate a batch of story ideas")
    ideas.add_argument("--count", type=int, default=10)
    ideas.add_argument("--seed", default="", help="optional seed topic")
    ideas.add_argument("--structure", help="story structure from the brand config")
    ideas.add_argument("--out", type=Path, help="output file (default: v1/ideas/ideas-<time>.json)")

    script = sub.add_parser("script", help="turn one idea or premise into a timed script")
    source = script.add_mutually_exclusive_group(required=True)
    source.add_argument("--idea-file", type=Path, help="idea batch JSON from `ideas`")
    source.add_argument("--premise", help="your own one-sentence premise")
    script.add_argument("--pick", type=int, default=1, help="idea number in the file (1-based)")
    script.add_argument("--content-id", help="default: next fs-short-NNN")
    script.add_argument("--structure", help="default: rotate so none repeats back to back")
    script.add_argument("--duration", type=int, default=45, help="target seconds (30-55)")
    script.add_argument("--force", action="store_true", help="overwrite an existing script")
    return parser


def main(
    argv: list[str] | None = None,
    env: dict[str, str] | None = None,
    client: Any = None,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    args = build_parser().parse_args(argv)
    env = common.load_env() if env is None else env
    try:
        if args.command == "ideas":
            return run_ideas(args, env, client, sleep)
        return run_script(args, env, client, sleep)
    except (common.KillSwitchError, llm.LLMError, ValueError, KeyError, OSError) as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
