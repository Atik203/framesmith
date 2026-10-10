"""Shared helpers for Framesmith scripts.

Standard library only (check_env.py must run before `pip install`), except `load_brand`,
which imports PyYAML when called.
"""

from __future__ import annotations

import csv
import os
import re
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONTENT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,40}$")
TRUE_VALUES = {"1", "true", "yes", "y", "on"}

# Blueprint R14. Keep in sync with the R14 "Tracking log" row; tests compare them.
LOG_COLUMNS = [
    "content_id",
    "content_type",
    "parent_content_id",
    "title",
    "date",
    "platform",
    "url",
    "story_structure",
    "hook_family",
    "narrator_style",
    "visual_treatment",
    "duration_seconds",
    "script_version",
    "model_names",
    "active_minutes",
    "cost_usd",
    "human_pass",
    "disclosure",
    "views_24h",
    "views_72h",
    "views_latest",
    "viewed_vs_swiped",
    "avg_pct_viewed",
    "followers_gained",
    "ctr",
    "first30_retention",
    "avg_view_duration_s",
    "notes",
]


class KillSwitchError(RuntimeError):
    """A kill switch in .env blocks this operation (blueprint Appendix D)."""


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = re.sub(r"\s+#.*$", "", value.strip())
        values[key.strip()] = value.strip("'\"")
    return values


def load_env(root: Path = ROOT) -> dict[str, str]:
    """Values from `.env`, overridden by real FRAMESMITH_* environment variables."""
    values: dict[str, str] = {}
    env_path = root / ".env"
    if env_path.is_file():
        values.update(parse_env_file(env_path))
    values.update({k: v for k, v in os.environ.items() if k.startswith("FRAMESMITH_")})
    return values


def env_flag(env: dict[str, str], name: str, default: bool) -> bool:
    raw = (env.get(name) or "").strip()
    if not raw:
        return default
    return raw.lower() in TRUE_VALUES


def require_generation_enabled(env: dict[str, str] | None = None) -> None:
    env = load_env() if env is None else env
    if not env_flag(env, "FRAMESMITH_GENERATION_ENABLED", True):
        raise KillSwitchError("FRAMESMITH_GENERATION_ENABLED is false; generation is switched off")


def require_publishing_enabled(env: dict[str, str] | None = None) -> None:
    env = load_env() if env is None else env
    if not env_flag(env, "FRAMESMITH_PUBLISHING_ENABLED", False):
        raise KillSwitchError("FRAMESMITH_PUBLISHING_ENABLED is not true; publishing is off")


def data_dir(env: dict[str, str] | None = None) -> Path:
    env = load_env() if env is None else env
    path = Path(env.get("FRAMESMITH_DATA_DIR") or "v1")
    return path if path.is_absolute() else ROOT / path


def read_log(path: Path | None = None) -> list[dict[str, str]]:
    path = path or ROOT / "log.csv"
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_brand(brand_id: str = "framesmith", root: Path = ROOT) -> dict:
    import yaml

    path = root / "configs" / "brands" / f"{brand_id}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def script_files(data: Path) -> list[Path]:
    """Script JSON files in data/scripts, without the .meta.json sidecars."""
    folder = data / "scripts"
    return sorted(p for p in folder.glob("*.json") if not p.name.endswith(".meta.json"))


def next_content_id(
    prefix: str, kind: str, data: Path, log_rows: Iterable[dict[str, str]] = ()
) -> str:
    """Next free id such as fs-short-004, looking at script files and log.csv rows."""
    pattern = re.compile(rf"^{re.escape(prefix)}-{re.escape(kind)}-(\d+)$")
    numbers = [0]
    names = [p.stem for p in script_files(data)]
    names += [row.get("content_id") or "" for row in log_rows]
    for name in names:
        match = pattern.match(name)
        if match:
            numbers.append(int(match.group(1)))
    return f"{prefix}-{kind}-{max(numbers) + 1:03d}"
