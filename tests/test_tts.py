import pytest
import tts


def test_narration_lines_preserve_script_order_and_remove_blank_edges():
    script = {
        "script": [
            {"index": 1, "text": " First line. "},
            {"index": 2, "text": "Second line."},
        ]
    }

    assert tts.narration_lines(script) == ["First line.", "Second line."]


def test_narration_lines_reject_empty_script():
    with pytest.raises(ValueError, match="no narration segments"):
        tts.narration_lines({"script": []})
