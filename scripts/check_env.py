#!/usr/bin/env python3
"""Check that this machine and repo are ready for Framesmith V1 (blueprint R11, Day 1).

Usage:
    python scripts/check_env.py

One line per check: [ OK ] ready, [FAIL] required and missing, [WARN] needs attention,
[ -- ] optional and not present. Never prints secret values. Exit code 1 if any [FAIL].
Standard library only, so it also works before `pip install`.
"""

from __future__ import annotations

import csv
import importlib.util
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

import common

ROOT = common.ROOT

REQUIRED_DIRS = [
    "configs/brands",
    "schemas",
    "prompts",
    "scripts",
    "provenance",
    "v1/ideas",
    "v1/scripts",
    "v1/assets",
    "v1/audio",
    "v1/subtitles",
    "v1/renders",
    "v1/published",
]
REQUIRED_FILES = [
    "AGENTS.md",
    "Roadmap.md",
    "blueprint.md",
    "log.csv",
    ".env.example",
    "configs/brands/lanternfall.yaml",
    "schemas/idea.schema.json",
    "schemas/script.schema.json",
    "schemas/render_spec.schema.json",
]
REQUIRED_PACKAGES = {
    "jsonschema": "jsonschema",
    "yaml": "pyyaml",
    "dotenv": "python-dotenv",
    "httpx": "httpx",
}
OPTIONAL_PACKAGES = {
    "kokoro": "kokoro",
    "soundfile": "soundfile",
    "faster_whisper": "faster-whisper",
}
PROVIDERS = ("gemini", "openrouter", "openai", "ollama")

failures = 0


def report(status: str, message: str) -> None:
    global failures
    if status == "FAIL":
        failures += 1
    label = {"OK": "[ OK ]", "FAIL": "[FAIL]", "WARN": "[WARN]", "OPT": "[ -- ]"}[status]
    print(f"{label} {message}")


def run_version(cmd: list[str]) -> str | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=15, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    text = (out.stdout or out.stderr).strip()
    return text.splitlines()[0] if text else ""


def check_tool(name: str, args: list[str], required: bool, hint: str = "") -> None:
    path = shutil.which(name)
    if not path:
        suffix = f" ({hint})" if hint else ""
        report("FAIL" if required else "OPT", f"{name} not found on PATH{suffix}")
        return
    report("OK", f"{name}: {run_version([path, *args]) or path}")


def check_python() -> None:
    v = sys.version_info
    if v >= (3, 11):
        report("OK", f"python {v.major}.{v.minor}.{v.micro}")
    else:
        report("FAIL", f"python {v.major}.{v.minor} found; blueprint needs 3.11+")


def check_packages() -> None:
    for module, package in REQUIRED_PACKAGES.items():
        if importlib.util.find_spec(module):
            report("OK", f"python package {package}")
        else:
            report("FAIL", f"python package {package} missing (pip install -r requirements.txt)")
    for module, package in OPTIONAL_PACKAGES.items():
        if importlib.util.find_spec(module):
            report("OK", f"python package {package}")
        else:
            report("OPT", f"python package {package} not installed (requirements-audio.txt)")


def provider_status(values: dict[str, str]) -> list[tuple[str, str]]:
    """(status, message) per LLM provider, from .env values. Never includes key text."""
    results: list[tuple[str, str]] = []
    for name in PROVIDERS:
        prefix = f"FRAMESMITH_{name.upper()}"
        key = values.get(f"{prefix}_API_KEY", "").strip()
        model = values.get(f"{prefix}_MODEL", "").strip()
        if name == "ollama":
            if model:
                results.append(("OK", "llm ollama: model set (last-resort fallback)"))
            else:
                results.append(("OPT", "llm ollama: not configured (optional fallback)"))
        elif key and model:
            results.append(("OK", f"llm {name}: key and model set"))
        elif key:
            results.append(("WARN", f"llm {name}: key set but {prefix}_MODEL is empty"))
        elif model:
            results.append(("WARN", f"llm {name}: model set but {prefix}_API_KEY is empty"))
        else:
            results.append(("OPT", f"llm {name}: not configured"))
    return results


def check_env_file() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        report("FAIL", ".env missing (copy .env.example to .env and add your keys)")
        return
    values = common.load_env()
    statuses = provider_status(values)
    for status, message in statuses:
        report(status, message)
    cloud_ready = sum(1 for s, m in statuses if s == "OK" and "ollama" not in m)
    if cloud_ready == 0:
        report("FAIL", "no usable cloud LLM provider (need a key and a model name)")
    elif cloud_ready == 1:
        report("WARN", "only one cloud LLM provider ready; R11 wants a second as backup")
    publishing = common.env_flag(values, "FRAMESMITH_PUBLISHING_ENABLED", False)
    generation = common.env_flag(values, "FRAMESMITH_GENERATION_ENABLED", True)
    report("OK", f"kill switches: publishing={publishing}, generation={generation}")
    if publishing:
        report("WARN", "FRAMESMITH_PUBLISHING_ENABLED is true but V1 publishing is manual")


def check_layout() -> None:
    missing = [d for d in REQUIRED_DIRS if not (ROOT / d).is_dir()]
    missing += [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    if missing:
        report("FAIL", "missing repo paths: " + ", ".join(missing))
    else:
        report("OK", "repo folders and key files present")
    log_path = ROOT / "log.csv"
    if log_path.is_file():
        with log_path.open(newline="", encoding="utf-8-sig") as handle:
            header = next(csv.reader(handle), [])
        if header == common.LOG_COLUMNS:
            report("OK", "log.csv header matches the tracking columns (R14)")
        else:
            report("FAIL", "log.csv header differs from LOG_COLUMNS in scripts/common.py")


def check_comfyui() -> None:
    values = common.load_env()
    url = values.get("FRAMESMITH_COMFYUI_URL", "http://127.0.0.1:8188").rstrip("/")
    try:
        with urllib.request.urlopen(f"{url}/system_stats", timeout=1.5) as response:
            report("OK", f"ComfyUI reachable at {url} (HTTP {response.status})")
    except (urllib.error.URLError, OSError, ValueError):
        report("OPT", f"ComfyUI not reachable at {url} (start it before generating images)")


def main() -> int:
    print(f"Framesmith environment check ({ROOT})")
    check_python()
    check_tool("node", ["--version"], required=True, hint="install Node LTS")
    check_tool("npm", ["--version"], required=True, hint="comes with Node")
    check_tool("ffmpeg", ["-version"], required=True, hint="install FFmpeg and add to PATH")
    check_tool("git", ["--version"], required=True)
    check_tool("espeak-ng", ["--version"], required=False, hint="needed by Kokoro on Day 1")
    check_tool("ollama", ["--version"], required=False, hint="last-resort local LLM")
    check_tool(
        "nvidia-smi",
        ["--query-gpu=name,memory.total", "--format=csv,noheader"],
        required=False,
        hint="NVIDIA driver",
    )
    check_packages()
    check_env_file()
    check_layout()
    check_comfyui()
    print()
    if failures:
        print(f"{failures} required check(s) failed.")
        return 1
    print("All required checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
