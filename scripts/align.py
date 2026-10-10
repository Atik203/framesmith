#!/usr/bin/env python3
"""Use local word timestamps to align known narration text into subtitle chunks."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import wave
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import common
import validate


def _normal(word: str) -> str:
    return re.sub(r"[^a-z0-9]", "", word.casefold())


def resample_audio(audio: Any, sample_rate: int, target_rate: int = 16_000) -> Any:
    """Convert mono float audio to the sample rate expected by Whisper."""
    import numpy as np

    values = np.asarray(audio, dtype=np.float32).reshape(-1)
    if sample_rate <= 0 or target_rate <= 0 or not len(values):
        raise ValueError("audio and sample rates must be valid")
    if sample_rate == target_rate:
        return values
    target_length = max(1, round(len(values) * target_rate / sample_rate))
    source_positions = np.linspace(0, len(values) - 1, target_length)
    return np.interp(source_positions, np.arange(len(values)), values).astype(np.float32)


def caption_chunks(
    reference: str,
    timed_words: list[dict[str, Any]],
    duration: float,
    *,
    max_words: int = 5,
) -> list[dict[str, Any]]:
    """Map word timestamps back to exact reference words and group captions."""
    expected = reference.split()
    valid_words = [
        word
        for word in timed_words
        if str(word.get("word", "")).strip()
        and word.get("start") is not None
        and word.get("end") is not None
    ]
    observed = [str(word["word"]).strip() for word in valid_words]
    if not expected or not observed or duration <= 0:
        raise ValueError("could not align reference text to any timed audio words")
    if not 1 <= max_words <= 7:
        raise ValueError("max_words must be between 1 and 7")

    matcher = SequenceMatcher(
        a=[_normal(word) for word in expected],
        b=[_normal(word) for word in observed],
        autojunk=False,
    )
    if matcher.ratio() < 0.65:
        raise ValueError("could not align reference text to the recognized narration")

    timings: list[tuple[float, float] | None] = [None] * len(expected)
    for tag, a1, a2, b1, b2 in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(a2 - a1):
                word = valid_words[b1 + offset]
                timings[a1 + offset] = (float(word["start"]), float(word["end"]))
        elif tag == "replace" and b2 > b1:
            for offset in range(a2 - a1):
                source_index = b1 + min(
                    b2 - b1 - 1, round(offset * (b2 - b1) / max(a2 - a1, 1))
                )
                word = valid_words[source_index]
                timings[a1 + offset] = (float(word["start"]), float(word["end"]))

    # Fill deleted reference words between the nearest known word boundaries.
    for index, timing in enumerate(timings):
        if timing is not None:
            continue
        left = next((timings[i][1] for i in range(index - 1, -1, -1) if timings[i]), 0.0)
        right = next(
            (timings[i][0] for i in range(index + 1, len(timings)) if timings[i]), duration
        )
        missing_count = sum(1 for item in timings[index:] if item is None)
        span = max(right - left, 0.08)
        step = span / max(missing_count + 1, 1)
        timings[index] = (left + step / 2, left + step)

    groups: list[list[int]] = []
    current: list[int] = []
    for index, token in enumerate(expected):
        current.append(index)
        if len(current) >= max_words or re.search(r"[.!?,;:]\W*$", token):
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    output = []
    last_end = 0.0
    for group in groups:
        start = min(timings[index][0] for index in group if timings[index])
        end = max(timings[index][1] for index in group if timings[index])
        start = max(last_end, min(start, duration))
        end = max(start + 0.08, min(end, duration))
        output.append(
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "text": " ".join(expected[index] for index in group),
            }
        )
        last_end = end
    return output


def run(args: argparse.Namespace) -> int:
    env = common.load_env()
    common.require_generation_enabled(env)
    try:
        script = json.loads(args.script.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot read script {args.script}: {exc}")
        return 2
    errors, _ = validate.validate("script", script)
    if errors:
        print("[FAIL] invalid script: " + errors[0])
        return 1
    if not args.audio.is_file():
        print(f"[FAIL] audio file not found: {args.audio}")
        return 2

    reference = " ".join(segment["text"] for segment in script["script"])
    out = args.out or common.data_dir(env) / "subtitles" / f"{script['content_id']}.json"
    if out.exists() and not args.force:
        print(f"[FAIL] output exists: {out} (use --force to overwrite)")
        return 1
    try:
        with wave.open(str(args.audio), "rb") as wav:
            duration = wav.getnframes() / wav.getframerate()
        if not os.environ.get("HF_HOME"):
            os.environ["HF_HOME"] = str(common.ROOT / ".cache" / "huggingface")
        import numpy as np
        import soundfile as sf
        from faster_whisper import WhisperModel

        audio, sample_rate = sf.read(str(args.audio), dtype="float32")
        if audio.ndim == 2:
            audio = np.mean(audio, axis=1, dtype=np.float32)
        audio = resample_audio(audio, sample_rate)

        model = WhisperModel(
            args.model,
            device="cpu",
            compute_type="int8",
            download_root=str(common.ROOT / ".cache" / "faster-whisper"),
        )
        segments, _ = model.transcribe(
            audio,
            language="en",
            word_timestamps=True,
            initial_prompt=reference,
            vad_filter=False,
            beam_size=5,
        )
        words = [
            {"word": word.word, "start": word.start, "end": word.end}
            for segment in segments
            for word in (segment.words or [])
            if word.start is not None and word.end is not None
        ]
        chunks = caption_chunks(reference, words, duration)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(
                {
                    "content_id": script["content_id"],
                    "duration_seconds": round(duration, 3),
                    "alignment_model": args.model,
                    "alignment_device": "cpu",
                    "chunks": chunks,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"[FAIL] caption alignment failed: {type(exc).__name__}: {exc}")
        return 1
    print(f"[ OK ] {out}: {len(chunks)} caption chunks aligned to {duration:.2f}s audio")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path, help="validated script JSON")
    parser.add_argument("--audio", type=Path, required=True, help="narration WAV")
    parser.add_argument("--model", default="tiny.en", help="faster-whisper model size")
    parser.add_argument("--out", type=Path, help="output subtitle JSON")
    parser.add_argument("--force", action="store_true", help="overwrite existing output")
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
