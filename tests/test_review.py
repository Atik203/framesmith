import csv
from datetime import date, timedelta

import common
import review

START = date(2026, 10, 12)


def row(**fields):
    base = dict.fromkeys(common.LOG_COLUMNS, "")
    base.update(fields)
    return base


def video_row(n, **fields):
    defaults = {
        "content_id": f"lf-short-{n:03d}",
        "content_type": "short",
        "date": (START + timedelta(days=n - 1)).isoformat(),
        "platform": "youtube",
        "story_structure": ["mystery", "psychological_twist", "future_message"][n % 3],
        "narrator_style": ["deep_neutral", "warm_intimate"][n % 2],
        "visual_treatment": ["cinematic_anime", "illustrated_realism"][n % 2],
        "active_minutes": "40",
        "cost_usd": "0",
        "human_pass": "yes",
        "views_72h": str(1000 * n),
        "viewed_vs_swiped": "70",
    }
    return row(**{**defaults, **fields})


def report(rows, today):
    return "\n".join(review.build_report(rows, today))


def test_empty_log_says_nothing_published():
    assert "No published videos" in report([], START)


def test_unpublished_rows_do_not_count():
    assert "No published videos" in report([row(content_id="lf-short-001", title="draft")], START)


def test_gate_a_passes_with_ten_videos():
    rows = [video_row(n) for n in range(1, 11)]
    text = report(rows, START + timedelta(days=13))
    assert "[x] 10 videos published: 10" in text
    assert "[x] every video <= 60 active minutes: 40 (0 over, 0 missing)" in text
    assert "[x] spend in log <= $20: $0.00" in text
    assert "Day 14 since the first published video (2026-10-12)" in text


def test_gate_a_fails_with_few_videos_and_long_edits():
    rows = [video_row(n, active_minutes="90") for n in range(1, 4)]
    text = report(rows, START + timedelta(days=3))
    assert "[ ] 10 videos published: 3" in text
    assert "[ ] every video <= 60 active minutes: 90 (3 over, 0 missing)" in text


def test_gate_a_fails_if_any_video_exceeds_sixty_minutes():
    rows = [video_row(n, active_minutes="61" if n == 1 else "40") for n in range(1, 11)]
    text = report(rows, START + timedelta(days=13))
    assert "[ ] every video <= 60 active minutes: 61 (1 over, 0 missing)" in text


def test_gate_a_fails_if_any_published_video_has_no_time_recorded():
    rows = [video_row(n, active_minutes="" if n == 1 else "40") for n in range(1, 11)]
    text = report(rows, START + timedelta(days=13))
    assert "[ ] every video <= 60 active minutes: 40 (0 over, 1 missing)" in text


def test_spend_over_cap_fails_gate():
    rows = [video_row(1, cost_usd="25")]
    assert "[ ] spend in log <= $20: $25.00" in report(rows, START)


def test_platform_rows_aggregate_per_video():
    rows = [
        video_row(1, platform="youtube", active_minutes="40", views_72h="6000"),
        video_row(1, platform="tiktok", active_minutes="40", views_72h="6000"),
    ]
    videos = review.load_videos(rows)
    assert len(videos) == 1
    assert videos[0].minutes == 40  # max, not 80
    assert videos[0].views == 12000  # summed
    assert "1 videos published" not in report(rows, START)  # counted once, not twice
    assert "10 videos published: 1" in report(rows, START)


def test_views_latest_beats_72h_and_24h():
    rows = [video_row(1, views_24h="10", views_72h="20", views_latest="30")]
    assert review.load_videos(rows)[0].views == 30


def test_gate_b_counts_and_top_third_swipe():
    rows = [
        video_row(n, views_72h=str(12000 if n <= 3 else 100), viewed_vs_swiped="80")
        for n in range(1, 10)
    ]
    rows += [video_row(n, views_72h="100", viewed_vs_swiped="40") for n in range(10, 13)]
    text = report(rows, START + timedelta(days=20))
    assert "[x] 3 videos above 10,000 views (all platforms summed): 3" in text
    assert "[x] viewed-vs-swiped on the top third >= 65%: 80%" in text
    assert "[ ] 30 Shorts published: 12" in text
    assert "[ ] 2 long-form pilots published: 0" in text


def test_long_form_counts_separately():
    rows = [video_row(1), video_row(2, content_id="lf-long-001", content_type="long_form")]
    assert "[ ] 2 long-form pilots published: 1" in report(rows, START)


def test_consecutive_same_structure_is_flagged():
    rows = [video_row(1, story_structure="mystery"), video_row(2, story_structure="mystery")]
    text = report(rows, START + timedelta(days=1))
    assert "[ ] no two consecutive videos share a story structure" in text
    assert "lf-short-001 -> lf-short-002 (mystery)" in text


def test_variation_window_checks_structures_narrators_visuals():
    rows = [
        video_row(
            1,
            story_structure="mystery",
            narrator_style="deep_neutral",
            visual_treatment="cinematic_anime",
        ),
        video_row(
            2,
            story_structure="future_message",
            narrator_style="not_approved",
            visual_treatment="not_approved",
        ),
        video_row(
            3,
            story_structure="emotional_reveal",
            narrator_style="deep_neutral",
            visual_treatment="cinematic_anime",
        ),
    ]
    text = report(rows, START + timedelta(days=3))
    assert "[x] story structures: 3 used (need 3)" in text
    assert "[ ] narrator styles: 1 used (need 2)" in text
    assert "[ ] visual treatments: 1 used (need 2)" in text
    assert "invalid narrator styles: not_approved" in text
    assert "invalid visual treatments: not_approved" in text


def test_variation_fails_when_one_style_used():
    rows = [
        video_row(
            n,
            story_structure="mystery",
            narrator_style="deep_neutral",
            visual_treatment="cinematic_anime",
        )
        for n in (1, 2, 3)
    ]
    text = report(rows, START + timedelta(days=3))
    assert "[ ] story structures: 1 used (need 3)" in text
    assert "[ ] narrator styles: 1 used (need 2)" in text
    assert "[ ] visual treatments: 1 used (need 2)" in text


def test_variation_rejects_values_outside_brand_lists():
    rows = [
        video_row(
            1,
            story_structure="mystery",
            narrator_style="deep_neutral",
            visual_treatment="cinematic_anime",
        ),
        video_row(
            2,
            story_structure="future_message",
            narrator_style="not_a_brand_style",
            visual_treatment="not_a_visual_treatment",
        ),
        video_row(
            3,
            story_structure="emotional_reveal",
            narrator_style="deep_neutral",
            visual_treatment="cinematic_anime",
        ),
    ]
    text = report(rows, START + timedelta(days=3))
    assert "invalid narrator styles: not_a_brand_style" in text
    assert "invalid visual treatments: not_a_visual_treatment" in text
    assert "[ ] narrator styles: 1 used (need 2)" in text
    assert "[ ] visual treatments: 1 used (need 2)" in text


def test_variation_reports_invalid_values_even_before_enough_videos_exist():
    rows = [video_row(1, narrator_style="not_a_brand_style")]
    text = report(rows, START)
    assert "[ ] invalid narrator styles: not_a_brand_style" in text
    assert "[ ] narrator styles: need 2+ videos in the window to check" in text


def test_variation_reports_brand_config_cannot_reach_minimum(monkeypatch):
    brand = common.load_brand()
    brand["narrator_styles"] = brand["narrator_styles"][:1]
    brand["visual_treatments"] = brand["visual_treatments"][:1]
    monkeypatch.setattr(common, "load_brand", lambda: brand)
    rows = [video_row(n) for n in range(1, 4)]
    text = report(rows, START + timedelta(days=3))
    assert "configured narrator styles: 1 allowed (need 2)" in text
    assert "configured visual treatments: 1 allowed (need 2)" in text


def test_missing_human_pass_is_reported():
    rows = [video_row(1), video_row(2, human_pass="")]
    text = report(rows, START + timedelta(days=1))
    assert "[ ] human pass recorded for every published video" in text
    assert "missing: lf-short-002" in text


def test_ranking_and_medians_by_structure():
    rows = [video_row(n, views_72h=str(n * 100)) for n in range(1, 8)]
    text = report(rows, START + timedelta(days=7))
    assert "Best three" in text and "Worst three" in text
    assert "Median views by story structure" in text


def test_number_parsing_accepts_percent_dollar_commas():
    assert review.number("72%") == 72
    assert review.number("$1,250.50") == 1250.5
    assert (
        review.number("") is None and review.number("n/a") is None and review.number(None) is None
    )


def test_cli_prints_report_and_handles_missing_log(tmp_path, capsys):
    log = tmp_path / "log.csv"
    with log.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=common.LOG_COLUMNS)
        writer.writeheader()
        writer.writerow(video_row(1))
    assert review.main(["--log", str(log), "--today", "2026-10-12"]) == 0
    assert "Gate A" in capsys.readouterr().out
    assert review.main(["--log", str(tmp_path / "nope.csv")]) == 2
