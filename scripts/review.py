#!/usr/bin/env python3
"""Gate and variation report from log.csv (blueprint R7, R8). Read-only.

    python scripts/review.py
    python scripts/review.py --log log.csv --today 2026-10-24

A video counts as published once a `date` is filled in. Per video, active_minutes and cost_usd
use the maximum across platform rows, views are summed and percentages averaged (blueprint R14).
Gate C and D are revenue gates and are not in log.csv.
"""

from __future__ import annotations

import argparse
import math
import statistics
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import common

GATE_A_DAY, GATE_A_VIDEOS, GATE_A_MAX_MINUTES = 14, 10, 60
GATE_B_DAY, GATE_B_SHORTS, GATE_B_LONG_FORM = 30, 30, 2
GATE_B_SWIPE_PCT, GATE_B_BIG_VIDEOS, GATE_B_BIG_VIEWS = 65.0, 3, 10_000
SPEND_CAP_USD = 20.0
WINDOW_DAYS = 7
VIEW_FIELDS = ("views_latest", "views_72h", "views_24h")
YES = {"yes", "y", "true", "1"}


def number(text: str | None) -> float | None:
    if text is None:
        return None
    cleaned = str(text).strip().replace(",", "").replace("$", "").rstrip("%").strip()
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def parse_date(text: str | None) -> date | None:
    try:
        return date.fromisoformat((text or "").strip())
    except ValueError:
        return None


@dataclass
class Video:
    content_id: str
    content_type: str
    published: date | None
    order: int
    structure: str = ""
    hook_family: str = ""
    narrator: str = ""
    visual: str = ""
    minutes: float | None = None
    cost: float = 0.0
    views: float | None = None
    swipe_pct: float | None = None
    human_pass: bool = False


def _first_number(row: dict[str, str], fields: tuple[str, ...]) -> float | None:
    for name in fields:
        value = number(row.get(name))
        if value is not None:
            return value
    return None


def load_videos(rows: list[dict[str, str]]) -> list[Video]:
    groups: dict[str, list[tuple[int, dict[str, str]]]] = {}
    for index, row in enumerate(rows):
        content_id = (row.get("content_id") or "").strip()
        if content_id:
            groups.setdefault(content_id, []).append((index, row))
    videos: list[Video] = []
    for content_id, items in groups.items():
        group = [row for _, row in items]

        def text(field: str, rows: list[dict[str, str]] = group) -> str:
            return next(
                ((r.get(field) or "").strip() for r in rows if (r.get(field) or "").strip()), ""
            )

        dated = [r for r in group if parse_date(r.get("date"))]
        minutes = [n for n in (number(r.get("active_minutes")) for r in group) if n is not None]
        costs = [n for n in (number(r.get("cost_usd")) for r in group) if n is not None]
        views = [n for n in (_first_number(r, VIEW_FIELDS) for r in group) if n is not None]
        swipes = [n for n in (number(r.get("viewed_vs_swiped")) for r in group) if n is not None]
        videos.append(
            Video(
                content_id=content_id,
                content_type=text("content_type") or "short",
                published=min(parse_date(r.get("date")) for r in dated) if dated else None,
                order=items[0][0],
                structure=text("story_structure"),
                hook_family=text("hook_family"),
                narrator=text("narrator_style"),
                visual=text("visual_treatment"),
                minutes=max(minutes) if minutes else None,
                cost=max(costs) if costs else 0.0,
                views=sum(views) if views else None,
                swipe_pct=statistics.mean(swipes) if swipes else None,
                human_pass=bool(dated)
                and all((r.get("human_pass") or "").strip().lower() in YES for r in dated),
            )
        )
    return videos


def _check(label: str, ok: bool) -> str:
    return f"[{'x' if ok else ' '}] {label}"


def gate_lines(videos: list[Video], today: date) -> list[str]:
    published = [v for v in videos if v.published]
    if not published:
        return ["No published videos in log.csv yet (a video counts once its date is filled in)."]
    start = min(v.published for v in published)
    shorts = [v for v in published if v.content_type != "long_form"]
    long_form = [v for v in published if v.content_type == "long_form"]
    minutes = [v.minutes for v in published if v.minutes is not None]
    spend = sum(v.cost for v in published)
    lines = [f"Day {(today - start).days + 1} since the first published video ({start})", ""]

    lines.append(f"Gate A (due day {GATE_A_DAY})")
    lines.append(
        _check(
            f"{GATE_A_VIDEOS} videos published: {len(published)}", len(published) >= GATE_A_VIDEOS
        )
    )
    if minutes:
        longest = max(minutes)
        over = sum(1 for m in minutes if m > GATE_A_MAX_MINUTES)
        missing = len(published) - len(minutes)
        lines.append(
            _check(
                f"every video <= {GATE_A_MAX_MINUTES} active minutes: "
                f"{longest:g} ({over} over, {missing} missing)",
                over == 0 and missing == 0,
            )
        )
    else:
        lines.append(
            _check(
                f"every video <= {GATE_A_MAX_MINUTES} active minutes: none recorded "
                f"({len(published)} missing)",
                False,
            )
        )
    lines.append(
        _check(f"spend in log <= ${SPEND_CAP_USD:.0f}: ${spend:.2f}", spend <= SPEND_CAP_USD)
    )

    with_views = sorted((v for v in published if v.views is not None), key=lambda v: -v.views)
    third = with_views[: max(1, math.ceil(len(with_views) / 3))] if with_views else []
    swipes = [v.swipe_pct for v in third if v.swipe_pct is not None]
    big = [v for v in with_views if v.views >= GATE_B_BIG_VIEWS]
    lines += ["", f"Gate B (due day {GATE_B_DAY})"]
    lines.append(
        _check(f"{GATE_B_SHORTS} Shorts published: {len(shorts)}", len(shorts) >= GATE_B_SHORTS)
    )
    lines.append(
        _check(
            f"{GATE_B_LONG_FORM} long-form pilots published: {len(long_form)}",
            len(long_form) >= GATE_B_LONG_FORM,
        )
    )
    if swipes:
        avg = statistics.mean(swipes)
        lines.append(
            _check(
                f"viewed-vs-swiped on the top third >= {GATE_B_SWIPE_PCT:.0f}%: {avg:.0f}%",
                avg >= GATE_B_SWIPE_PCT,
            )
        )
    else:
        lines.append(_check("viewed-vs-swiped on the top third: no data yet", False))
    lines.append(
        _check(
            f"{GATE_B_BIG_VIDEOS} videos above {GATE_B_BIG_VIEWS:,} views "
            f"(all platforms summed): {len(big)}",
            len(big) >= GATE_B_BIG_VIDEOS,
        )
    )
    lines.append(_check(f"spend <= ${SPEND_CAP_USD:.0f}: ${spend:.2f}", spend <= SPEND_CAP_USD))
    lines.append("[ ] one format clearly ahead (judge from the medians below)")
    return lines


def _median_views_by(videos: list[Video], attribute: str) -> list[str]:
    buckets: dict[str, list[float]] = {}
    for video in videos:
        key = getattr(video, attribute)
        if video.published and video.views is not None and key:
            buckets.setdefault(key, []).append(video.views)
    return [
        f"  {key}: median {statistics.median(values):,.0f} views over {len(values)} video(s)"
        for key, values in sorted(buckets.items(), key=lambda kv: -statistics.median(kv[1]))
    ]


def variation_lines(videos: list[Video], today: date) -> list[str]:
    brand = common.load_brand()
    rules = brand["variation_rules"]
    dimensions = (
        ("story structures", "structure", rules["min_story_structures"], brand["story_structures"]),
        ("narrator styles", "narrator", rules["min_narrator_styles"], brand["narrator_styles"]),
        ("visual treatments", "visual", rules["min_visual_treatments"], brand["visual_treatments"]),
    )
    published = sorted((v for v in videos if v.published), key=lambda v: (v.published, v.order))
    recent = [v for v in published if 0 <= (today - v.published).days < WINDOW_DAYS]
    lines = [f"Variation rules (R7), last {WINDOW_DAYS} days: {len(recent)} video(s)"]
    for label, attribute, minimum, allowed_values in dimensions:
        allowed = set(allowed_values)
        if len(allowed) < minimum:
            lines.append(
                f"[ ] configured {label}: {len(allowed)} allowed (need {minimum})"
            )
        observed = {getattr(v, attribute) for v in recent if getattr(v, attribute)}
        values = observed & allowed
        invalid = sorted(observed - allowed)
        if invalid:
            lines.append(f"[ ] invalid {label}: " + ", ".join(invalid))
        if len(recent) < minimum:
            lines.append(f"[ ] {label}: need {minimum}+ videos in the window to check")
            continue
        lines.append(
            _check(
                f"{label}: {len(values)} used (need {minimum})",
                len(values) >= minimum and not invalid,
            )
        )
    repeats = [
        f"{a.content_id} -> {b.content_id} ({a.structure})"
        for a, b in zip(published, published[1:], strict=False)
        if a.structure and a.structure == b.structure
    ]
    lines.append(_check("no two consecutive videos share a story structure", not repeats))
    lines += [f"    repeat: {text}" for text in repeats]
    missing = [v.content_id for v in published if not v.human_pass]
    lines.append(_check("human pass recorded for every published video", not missing))
    if missing:
        lines.append("    missing: " + ", ".join(missing))
    return lines


def ranking_lines(videos: list[Video]) -> list[str]:
    ranked = sorted(
        (v for v in videos if v.published and v.views is not None), key=lambda v: -v.views
    )
    if not ranked:
        return ["No view counts in log.csv yet."]

    def row(video: Video) -> str:
        return (
            f"  {video.content_id}: {video.views:,.0f} views ({video.structure or 'no structure'})"
        )

    lines = ["Best three"] + [row(v) for v in ranked[:3]]
    if len(ranked) >= 6:
        lines += ["Worst three"] + [row(v) for v in ranked[-3:]]
    return lines


def build_report(rows: list[dict[str, str]], today: date) -> list[str]:
    videos = load_videos(rows)
    lines = gate_lines(videos, today)
    if not any(v.published for v in videos):
        return lines
    lines += ["", *variation_lines(videos, today), "", *ranking_lines(videos)]
    for title, attribute in (("story structure", "structure"), ("hook family", "hook_family")):
        medians = _median_views_by(videos, attribute)
        if medians:
            lines += ["", f"Median views by {title}", *medians]
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--log", type=Path, default=common.ROOT / "log.csv")
    parser.add_argument("--today", type=date.fromisoformat, default=None, help="YYYY-MM-DD")
    args = parser.parse_args(argv)
    if not args.log.is_file():
        print(f"[FAIL] {args.log} not found")
        return 2
    today = args.today or date.today()
    print(f"Framesmith review, {today} ({args.log})\n")
    print("\n".join(build_report(common.read_log(args.log), today)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
