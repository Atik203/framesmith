#!/usr/bin/env python3
"""Turn a validated script JSON into a render spec for Remotion (blueprint Part IV, R14).

    python scripts/build_render_spec.py v1/scripts/lf-short-001.json \
        --audio v1/audio/lf-short-001.wav
    python scripts/build_render_spec.py v1/scripts/lf-short-001.json --audio-seconds 41.7 \
        --music audio/bgm-01.mp3

Paths inside the spec are relative to v1/. Scene durations are scaled to the real narration
length when --audio or --audio-seconds is given; without it the script's estimates are used.
Only Shorts are supported: long-form scene planning is manual in V1.5 (R12).
Exit code: 0 ok, 1 invalid input or spec, 2 usage or file error.
"""

from __future__ import annotations

import argparse
import json
import sys
import wave
from pathlib import Path
from typing import Any

import common
import validate

# Gentle motions for ordinary beats; micro_shake and focus_pull are hero moments
# that you pick by hand.
MOTION_CYCLE = ["push_in", "pan_left", "push_out", "pan_right", "parallax"]
SIZES = {"short": (1080, 1920), "long_form": (1920, 1080)}
FPS = 30


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / handle.getframerate()


def build_spec(
    script: dict[str, Any],
    *,
    audio_seconds: float | None = None,
    tail: float = 0.6,
    music: str | None = None,
    subtitles_ext: str = "json",
) -> dict[str, Any]:
    content_type = script.get("content_type", "short")
    if content_type != "short":
        raise ValueError(
            "only short scripts are supported; long-form scene planning is manual (R12)"
        )
    content_id = script["content_id"]
    segments = script["script"]
    durations = [float(s["duration_seconds"]) for s in segments]
    if audio_seconds is not None:
        if audio_seconds <= 0:
            raise ValueError("audio length must be positive")
        scale = audio_seconds / sum(durations)
        durations = [d * scale for d in durations]
        durations[-1] += tail

    scenes: list[dict[str, Any]] = []
    elapsed = 0.0
    cursor = 0.0
    for number, duration in enumerate(durations, start=1):
        elapsed += duration
        start, end = round(cursor, 2), round(elapsed, 2)
        scenes.append(
            {
                "asset": f"assets/{content_id}/scene-{number:02d}.png",
                "start": start,
                "duration": round(end - start, 2),
                "motion": MOTION_CYCLE[(number - 1) % len(MOTION_CYCLE)],
            }
        )
        cursor = end
    width, height = SIZES[content_type]
    return {
        "content_id": content_id,
        "content_type": content_type,
        "width": width,
        "height": height,
        "fps": FPS,
        "duration_seconds": round(cursor, 2),
        "scenes": scenes,
        "voice": f"audio/{content_id}.wav",
        "subtitles": f"subtitles/{content_id}.{subtitles_ext}",
        "music": music,
        "sfx": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("script", type=Path, help="script JSON, e.g. v1/scripts/lf-short-001.json")
    length = parser.add_mutually_exclusive_group()
    length.add_argument("--audio", type=Path, help="narration WAV; its length sets the timing")
    length.add_argument("--audio-seconds", type=float, help="narration length in seconds")
    parser.add_argument("--tail", type=float, default=0.6, help="seconds held after the narration")
    parser.add_argument("--music", help="licensed music path relative to v1/ (log it first)")
    parser.add_argument("--subtitles-ext", choices=["json", "ass"], default="json")
    parser.add_argument("--out", type=Path, help="default: v1/renders/<content_id>.spec.json")
    args = parser.parse_args(argv)

    try:
        script = json.loads(args.script.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot read {args.script}: {exc}")
        return 2
    errors, _ = validate.validate("script", script)
    if errors:
        for message in errors:
            print(f"[FAIL] {message}")
        return 1

    seconds = args.audio_seconds
    if args.audio:
        try:
            seconds = wav_seconds(args.audio)
        except (OSError, wave.Error, EOFError) as exc:
            print(f"[FAIL] cannot read WAV {args.audio}: {exc} (try --audio-seconds)")
            return 2
    try:
        spec = build_spec(
            script,
            audio_seconds=seconds,
            tail=args.tail,
            music=args.music,
            subtitles_ext=args.subtitles_ext,
        )
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1
    errors, warnings = validate.validate("render_spec", spec)
    for message in warnings:
        print(f"[WARN] {message}")
    if errors:
        for message in errors:
            print(f"[FAIL] {message}")
        return 1

    out = args.out or common.data_dir() / "renders" / f"{spec['content_id']}.spec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    note = "narration length" if seconds is not None else "script estimates (pass --audio later)"
    print(f"[ OK ] {out}: {len(spec['scenes'])} scenes, {spec['duration_seconds']}s from {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
