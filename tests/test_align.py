import align
import numpy as np
import pytest


def test_caption_chunks_keep_reference_words_and_limit_chunk_size():
    words = [
        {"word": "Nora", "start": 0.1, "end": 0.45},
        {"word": "follows", "start": 0.46, "end": 0.85},
        {"word": "the", "start": 0.86, "end": 1.0},
        {"word": "footprints", "start": 1.1, "end": 1.65},
        {"word": "home", "start": 1.7, "end": 2.0},
        {"word": "tonight.", "start": 2.05, "end": 2.45},
    ]

    chunks = align.caption_chunks(
        "Nora follows the footprints home tonight.", words, 2.5, max_words=3
    )

    assert [chunk["text"] for chunk in chunks] == ["Nora follows the", "footprints home tonight."]
    assert chunks[0]["start"] == 0.1 and chunks[-1]["end"] == 2.45


def test_caption_chunks_reject_unmatched_reference():
    with pytest.raises(ValueError, match="could not align"):
        align.caption_chunks("Nora follows every footprint home tonight.", [], 2.5)


def test_resample_audio_returns_16khz_length():
    audio = np.linspace(-1, 1, 24_000, dtype=np.float32)

    result = align.resample_audio(audio, 24_000)

    assert result.dtype == np.float32
    assert len(result) == 16_000
