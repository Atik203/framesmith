#!/usr/bin/env python3
"""Validate Framesmith JSON files against schemas/ plus a few sanity checks.

Usage:
    python scripts/validate.py idea        v1/ideas/lf-short-001.json
    python scripts/validate.py script      v1/scripts/lf-short-001.json
    python scripts/validate.py render_spec path/to/render_spec.json

Exit code: 0 = valid (warnings allowed), 1 = invalid, 2 = usage or file error.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
KINDS = ("idea", "script", "render_spec")

WORDS_PER_SECOND_RANGE = (1.8, 3.2)  # blueprint plans 130-160 wpm (2.2-2.7 wps); allow some slack
SHORT_DURATION_RANGE = (25.0, 60.0)


def load_schema(kind: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / f"{kind}.schema.json").read_text(encoding="utf-8"))


def schema_errors(kind: str, data: Any) -> list[str]:
    validator = Draft202012Validator(load_schema(kind))
    errors = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        location = "/".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(f"{location}: {err.message}")
    return errors


def _script_checks(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    segments = data.get("script", [])
    indexes = [s.get("index") for s in segments]
    if indexes != list(range(1, len(segments) + 1)):
        errors.append("script: segment index values must run 1..N in order")
    total = sum(float(s.get("duration_seconds", 0)) for s in segments)
    estimated = float(data.get("estimated_duration_seconds", 0))
    if abs(total - estimated) > 1.5:
        errors.append(
            f"estimated_duration_seconds={estimated:g} but segment durations sum to {total:g}"
        )
    if data.get("content_type", "short") == "short":
        low, high = SHORT_DURATION_RANGE
        if not low <= total <= high:
            warnings.append(f"short is {total:g}s; blueprint target is about 30-55s")
    for seg in segments:
        words = len(str(seg.get("text", "")).split())
        seconds = float(seg.get("duration_seconds", 0)) or 1.0
        wps = words / seconds
        if not WORDS_PER_SECOND_RANGE[0] <= wps <= WORDS_PER_SECOND_RANGE[1]:
            warnings.append(
                f"segment {seg.get('index')}: {words} words in {seconds:g}s = {wps:.1f} words/s "
                f"(expected about 2.2-2.7)"
            )
    first_text = segments[0].get("text", "") if segments else ""
    if segments and data.get("hook", "").strip().lower() not in first_text.strip().lower():
        warnings.append("hook text is not contained in the first segment's text")
    return errors, warnings


def _render_spec_checks(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    scenes = data.get("scenes", [])
    if not scenes:
        errors.append("scenes must contain at least one scene")
        return errors, warnings
    expected_start = 0.0
    for i, scene in enumerate(scenes, start=1):
        start = float(scene.get("start", 0))
        if abs(start - expected_start) > 0.05:
            errors.append(
                f"scene {i}: starts at {start:g}s, expected {expected_start:g}s (gap or overlap)"
            )
        expected_start = start + float(scene.get("duration", 0))
    total = data.get("duration_seconds", data.get("target_duration_seconds"))
    if total is not None and expected_start > float(total) + 0.05:
        errors.append(
            f"scenes run to {expected_start:g}s, past the video duration of {float(total):g}s"
        )
    if total is not None and expected_start < float(total) - 0.05:
        errors.append(
            f"scenes end at {expected_start:g}s, before the video duration of {float(total):g}s"
        )
    return errors, warnings


def validate(kind: str, data: Any) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Semantic checks only run when the schema check passes."""
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}; expected one of {KINDS}")
    errors = schema_errors(kind, data)
    warnings: list[str] = []
    if errors:
        return errors, warnings
    if kind == "script":
        e, w = _script_checks(data)
    elif kind == "render_spec":
        e, w = _render_spec_checks(data)
    else:
        e, w = [], []
    return errors + e, warnings + w


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in KINDS:
        print(__doc__)
        return 2
    kind, path = argv[1], Path(argv[2])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot read {path}: {exc}")
        return 2
    errors, warnings = validate(kind, data)
    for message in warnings:
        print(f"[WARN] {message}")
    for message in errors:
        print(f"[FAIL] {message}")
    if errors:
        print(f"{path}: invalid {kind}")
        return 1
    print(f"[ OK ] {path}: valid {kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
