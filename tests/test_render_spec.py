import json
import wave
from pathlib import Path

import build_render_spec as brs
import validate

EXAMPLES = Path(__file__).resolve().parent.parent / "schemas" / "examples"


def script():
    return json.loads((EXAMPLES / "script.example.json").read_text(encoding="utf-8"))


def test_spec_from_script_estimates_is_valid_and_contiguous():
    spec = brs.build_spec(script())
    assert validate.validate("render_spec", spec) == ([], [])
    assert spec["duration_seconds"] == 38
    assert len(spec["scenes"]) == 7
    cursor = 0.0
    for scene in spec["scenes"]:
        assert scene["start"] == round(cursor, 2)
        cursor = scene["start"] + scene["duration"]
    assert round(cursor, 2) == spec["duration_seconds"]


def test_paths_are_relative_to_v1():
    spec = brs.build_spec(script())
    assert spec["scenes"][0]["asset"] == "assets/fs-short-example/scene-01.png"
    assert spec["voice"] == "audio/fs-short-example.wav"
    assert spec["subtitles"] == "subtitles/fs-short-example.json"
    assert brs.build_spec(script(), subtitles_ext="ass")["subtitles"].endswith(".ass")


def test_audio_length_rescales_scenes_and_adds_tail():
    spec = brs.build_spec(script(), audio_seconds=40.0, tail=0.6)
    assert spec["duration_seconds"] == 40.6
    assert validate.validate("render_spec", spec) == ([], [])
    # proportions are kept: scene 2 was 6 of 38 seconds
    assert abs(spec["scenes"][1]["duration"] - 40 * 6 / 38) < 0.02


def test_motion_never_repeats_back_to_back():
    data = script()
    data["script"] = [dict(data["script"][0], index=i) for i in range(1, 13)]
    spec = brs.build_spec(data)
    motions = [s["motion"] for s in spec["scenes"]]
    assert all(a != b for a, b in zip(motions, motions[1:], strict=False))
    assert motions[0] == "push_in"


def test_music_is_passed_through():
    assert brs.build_spec(script(), music="audio/bgm-01.mp3")["music"] == "audio/bgm-01.mp3"


def test_long_form_is_rejected():
    import pytest

    data = script()
    data["content_type"] = "long_form"
    with pytest.raises(ValueError, match="long-form"):
        brs.build_spec(data)


def test_wav_seconds_reads_real_wav(tmp_path):
    path = tmp_path / "a.wav"
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(24000)
        handle.writeframes(b"\x00\x00" * 48000)
    assert brs.wav_seconds(path) == 2.0


def test_cli_writes_spec_from_audio(tmp_path, capsys):
    script_path = tmp_path / "fs-short-example.json"
    script_path.write_text(json.dumps(script()), encoding="utf-8")
    wav = tmp_path / "voice.wav"
    with wave.open(str(wav), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(24000)
        handle.writeframes(b"\x00\x00" * 24000 * 36)
    out = tmp_path / "out" / "spec.json"
    code = brs.main([str(script_path), "--audio", str(wav), "--out", str(out)])
    assert code == 0
    spec = json.loads(out.read_text(encoding="utf-8"))
    assert spec["duration_seconds"] == 36.6
    assert "narration length" in capsys.readouterr().out


def test_cli_rejects_invalid_script_and_missing_file(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"content_id": "lf-short-001"}), encoding="utf-8")
    assert brs.main([str(bad), "--out", str(tmp_path / "x.json")]) == 1
    assert brs.main([str(tmp_path / "missing.json")]) == 2
