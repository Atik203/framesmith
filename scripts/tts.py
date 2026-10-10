#!/usr/bin/env python3
"""Render validated script JSON into a 24 kHz Kokoro WAV on CPU."""

from __future__ import annotations

import argparse
import json
import os
import sys
import wave
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import common
import validate

SAMPLE_RATE = 24_000


def narration_lines(script: dict[str, Any]) -> list[str]:
    """Return non-empty narration lines in script order."""
    lines = [str(segment.get("text", "")).strip() for segment in script.get("script", [])]
    lines = [line for line in lines if line]
    if not lines:
        raise ValueError("script has no narration segments")
    return lines


def synthesize(lines: list[str], voice: str, speed: float) -> Any:
    """Synthesize on CPU and join phrase chunks with a short pause."""
    if not os.environ.get("HF_HOME"):
        os.environ["HF_HOME"] = str(common.ROOT / ".cache" / "huggingface")
    import numpy as np
    from kokoro import KPipeline

    pipeline = KPipeline(lang_code="a", device="cpu")
    chunks = []
    for _, _, audio in pipeline("\n".join(lines), voice=voice, speed=speed, split_pattern=r"\n+"):
        chunks.append(np.asarray(audio, dtype=np.float32).reshape(-1))
    if not chunks:
        raise RuntimeError("Kokoro returned no audio")
    silence = np.zeros(round(SAMPLE_RATE * 0.12), dtype=np.float32)
    pieces = []
    for index, chunk in enumerate(chunks):
        if index:
            pieces.append(silence)
        pieces.append(chunk)
    return np.concatenate(pieces)


def run(args: argparse.Namespace) -> int:
    env = common.load_env()
    common.require_generation_enabled(env)
    try:
        script = json.loads(args.script.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot read script {args.script}: {exc}")
        return 2
    errors, warnings = validate.validate("script", script)
    for warning in warnings:
        print(f"[WARN] {warning}")
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1

    try:
        lines = narration_lines(script)
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1
    brand = common.load_brand(env.get("FRAMESMITH_BRAND") or "framesmith")
    narration = brand.get("narration", {})
    candidates = narration.get("voice_candidates", ["am_michael"])
    voice = args.voice or narration.get("voice_id") or candidates[0]
    rate = float(narration.get("rate", 1.0))
    content_id = script["content_id"]
    out = args.out or common.data_dir(env) / "audio" / f"{content_id}.wav"
    meta = out.with_suffix(".tts.json")
    if (out.exists() or meta.exists()) and not args.force:
        print(f"[FAIL] output exists: {out} (use --force to overwrite)")
        return 1

    try:
        audio = synthesize(lines, voice, rate)
        import soundfile as sf

        out.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(out), audio, SAMPLE_RATE, subtype="PCM_16")
        seconds = len(audio) / SAMPLE_RATE
        if seconds < 1:
            raise RuntimeError("generated WAV is unexpectedly short")
        with wave.open(str(out), "rb") as wav:
            if wav.getframerate() != SAMPLE_RATE or wav.getnchannels() != 1:
                raise RuntimeError("generated WAV must be mono at 24 kHz")
        meta.write_text(
            json.dumps(
                {
                    "content_id": content_id,
                    "engine": "kokoro",
                    "voice": voice,
                    "device": "cpu",
                    "sample_rate": SAMPLE_RATE,
                    "duration_seconds": round(seconds, 3),
                    "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"[FAIL] narration synthesis failed: {type(exc).__name__}: {exc}")
        return 1
    print(f"[ OK ] {out}: {seconds:.2f}s, 24 kHz mono, Kokoro voice {voice} on CPU")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path, help="validated script JSON")
    parser.add_argument("--voice", help="Kokoro voice id; defaults to brand configuration")
    parser.add_argument("--out", type=Path, help="output WAV path")
    parser.add_argument("--force", action="store_true", help="overwrite existing outputs")
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
