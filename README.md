# Framesmith

Private repo for **Lanternfall**, an AI-assisted English video brand (original cinematic stories as Shorts and
8–12 minute YouTube episodes). *Framesmith* is the internal codename; never use it publicly.

Current stage: **V1, zero cost, no framework.** One folder of Python scripts, one Remotion project, one tracking
sheet. The plan, gates and rules are in [`blueprint.md`](blueprint.md) (Revision 1.2 and R14 win on conflicts).
Progress is in [`Roadmap.md`](Roadmap.md). AI agents read [`AGENTS.md`](AGENTS.md).

## 1. Set up (Windows, PowerShell)

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
Copy-Item .env.example .env        # then add your free-tier keys and model names
python scripts/check_env.py
python -m pytest -q
```

Install what `check_env.py` reports as missing: Node LTS, FFmpeg, Git, and on Day 1 ComfyUI (portable build) and
espeak-ng. Heavy audio packages are separate: `python -m pip install -r requirements-audio.txt`.

```powershell
git init -b main
git add .
git commit -m "Initial Framesmith scaffold"
```

### `.env`

Put Gemini and OpenRouter keys in `.env` for free-first generation. OpenAI `gpt-6-luna` is the paid final
fallback and must use only the existing $5 credit; do not enable auto-recharge or add credit. Groq is not
used. Model defaults are shown in `.env.example` and configured in `.env`; recheck free availability before generation.
`FRAMESMITH_PUBLISHING_ENABLED` stays `false` in V1 (publishing is manual).

## 2. Daily commands

```powershell
python scripts/generate.py ideas --count 10                      # ideas -> v1/ideas/
python scripts/generate.py script --idea-file v1\ideas\<file>.json --pick 2
python scripts/generate.py script --premise "Your own one-sentence premise"
python scripts/validate.py script v1\scripts\lf-short-001.json
python scripts/build_render_spec.py v1\scripts\lf-short-001.json --audio v1\audio\lf-short-001.wav
python scripts/review.py                                         # gates and variation rules from log.csv
```

`generate.py` validates every reply against `schemas/`, retries with feedback (3 attempts per provider), then falls
back to the next provider. It picks a story structure that differs from the last script's (rule R7). Edit the
premise and the opening lines yourself before going on: every script and final cut needs a human pass.

## 3. Where things are

See the tree in `AGENTS.md`. Working data lives in `v1/`; media files there are gitignored. Scripts, ideas, subtitle
JSON and render specs are small text and are committed.

## 4. Tracking

One row per video per platform in `log.csv` (columns in blueprint R14). Record metrics at 24 h and 72 h, refresh
`views_latest` weekly, and use only the structure, hook, narrator and visual values listed in
`configs/brands/lanternfall.yaml`. Weekly 30-minute review: copy `notes/weekly-review.md` and run `review.py`.

## 5. What is not built yet

Narration (Kokoro), caption alignment, MP4 QA checks, the ComfyUI driver and the Remotion project come on Days 1–2;
see `Roadmap.md`. `docs/renderer-setup.md` has the Remotion notes. The LLM provider code was tested against mocked
HTTP, so the first live `generate.py` run on your keys is the real test; send me the error output if it fails.
