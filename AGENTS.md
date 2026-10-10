# AGENTS.md — Framesmith (public brand: Lanternfall)

Instructions for AI coding and content agents (Claude Code, Codex, Cursor, etc.) working in this repo.
Humans: start with `README.md`. Progress lives in `Roadmap.md`.

## What this project is

A private repo for an AI-assisted English-language video business: short-form (Shorts/Reels/TikTok) plus
8–12 minute YouTube long-form. First vertical: **original AI cinematic stories**.

- Public brand: **Lanternfall**. Internal codename and repo: **Framesmith**.
  Never put "Framesmith" in a video, caption, title, description, handle or any public page.
- Owner: Atikur, solo operator, Dhaka. Machine: Lenovo Legion 5 laptop, AMD Ryzen 7 5800H, **32 GB RAM**, RTX 3060 **6 GB**.
- Goal order: publish videos -> learn what earns -> earn -> only then automate.

## Source of truth and progress

- `blueprint.md` is the single source of truth. **Revision 1.2 (R1–R14, at the top) overrides any
  conflicting statement elsewhere in it.** Text under a "Revision 1.2" banner is superseded.
- If a decision conflicts with the blueprint, update `blueprint.md` first (add a change-log entry in
  Part XXXVI), then implement. Do not leave decisions only in chat, code comments or commit messages.
- `Roadmap.md` is the checkbox tracker. When you finish a task, tick its box and add the date in the same
  change. Only tick a box when its "done when" is really true. Do not invent boxes for V2/V3 work.
- External facts (YouTube/Meta/TikTok rules, prices, model and library versions) were checked on
  2026-10-08. Re-check before spending money or relying on them.

## Current stage: V1 — zero cost, no framework

- V1 is **one folder of Python scripts, one Remotion project, one tracking sheet (`log.csv`)**.
- Build a tool only when doing the task by hand has already cost more than about 2 hours per week, or when
  it covers a Day 1–3 step in blueprint R11 (narration, caption alignment, image driver, MP4 QA).
- Do **not** add or propose yet: FastAPI, Next.js, Postgres/pgvector, Redis, Temporal, a LiteLLM server,
  OpenAI Agents SDK, Docker/Kubernetes, multi-agent orchestration, platform publishing adapters, or
  browser automation. They are gated by revenue (V2 at about $500/month net for 2 consecutive months;
  V3 at about $2,000–3,000/month for 3).
- Budget is $0. Hard cap $20 total in the first 60 days, only to remove one named bottleneck written down
  first. Never add a paid service, paid API key or subscription without the owner saying so.
- Gates: **A** day 14 = 10 videos published, <= 60 active minutes per video. **B** day 30 = 30 Shorts +
  2 long-form pilots, >= 3 videos above 10k views, spend <= $20. If B fails, change hook family, format
  or niche, not the tooling. `python scripts/review.py` shows progress.
- Long-form (V1.5) is a manual content pilot in weeks 2–3 on the V1 stack: 1 per week, never more than 2.
  It is not a reason to build infrastructure.

## V1 stack (blueprint R5)

| Function | Choice |
| --- | --- |
| Ideas and scripts | OpenRouter and OpenCode Zen free models first, then the owner's existing $5 OpenAI API credit as the paid final fallback through `scripts/generate.py`. Gemini is disabled after its billing error. Use only explicitly free models; do not add credit or auto-recharge. Do not use Groq. |
| Images | ComfyUI, SDXL-family anime checkpoint, one image at a time on 6 GB. Check each checkpoint's commercial license. |
| Narration | Kokoro-82M on CPU. A/B candidate: Qwen3-TTS 0.6B. Never the 1.7B model. |
| Caption timing | Forced alignment of the known script to the audio (WhisperX or faster-whisper). Do not re-transcribe text we already have. |
| Render | Remotion + FFmpeg. Compositions `ShortVertical` (1080x1920) and `LongHorizontal` (1920x1080), 30 fps. |
| Music / SFX | Only assets with an explicit commercial license, recorded in `provenance/licenses.csv`. |
| Tracking | `log.csv`, one row per video per platform (columns in blueprint R14). |
| Publishing | Manual. Agents never publish or upload. |

## Repo layout

```text
AGENTS.md  CLAUDE.md  README.md  Roadmap.md  blueprint.md
.env.example  requirements*.txt  pyproject.toml  log.csv
configs/brands/lanternfall.yaml   brand config: structures, hook families, narrator and visual lists
schemas/                          JSON Schemas (strict) + examples: idea, script, render_spec
prompts/niches/ai_stories/        versioned prompt files (story_idea_v1.md, story_writer_v1.md)
scripts/                          plain Python scripts (no package), see Tools
tests/                            pytest checks
provenance/                       asset rights policy + licenses.csv
comfyui/workflows/                saved ComfyUI workflow JSON (seed, checkpoint, license noted)
renderer/                         Remotion project (created on Day 2; see docs/renderer-setup.md)
v1/{ideas,scripts,assets,audio,subtitles,renders,published}   working data, media gitignored
notes/  docs/                     weekly reviews, setup notes
```

Per-content files (`content_id` looks like `lf-short-001`, `lf-long-001`; derivative Shorts set
`parent_content_id`): `v1/ideas/ideas-<time>.json`, `v1/scripts/{id}.json` (+ `{id}.meta.json` sidecar),
`v1/assets/{id}/scene-01.png`, `v1/audio/{id}.wav`, `v1/subtitles/{id}.json`,
`v1/renders/{id}.spec.json` (committed) and `v1/renders/{id}.mp4` (ignored).
Paths inside a render spec are relative to `v1/`.

## Tools

| Script | What it does |
| --- | --- |
| `scripts/check_env.py` | Tools on PATH, packages, `.env` (provider keys and models, never prints values), folders, `log.csv` header. |
| `scripts/validate.py` | `python scripts/validate.py idea\|script\|render_spec FILE`: schema plus sanity checks (durations, words per second, scene gaps). |
| `scripts/generate.py` | `ideas` and `script` subcommands. OpenRouter and OpenCode Zen free tiers first, optional OpenAI paid fallback last; schema validation, up to 3 attempts per provider. Gemini is disabled in the active order. Writes JSON plus a `.meta.json` with provider, model and prompt id. Rotates story structure so none repeats back to back. |
| `scripts/build_render_spec.py` | Script JSON (+ narration WAV length) -> `v1/renders/{id}.spec.json`. Shorts only. |
| `scripts/review.py` | Gate A/B progress, R7 variation rules, best/worst videos from `log.csv`. Read-only. |
| `scripts/common.py`, `scripts/llm.py` | Shared helpers (env, kill switches, ids) and the provider-fallback client. Import, do not run. |

Not built yet (Roadmap): narration (`tts.py`), caption alignment (`align.py`), MP4 QA, ComfyUI driver,
long-form script generation. Build each only when its Roadmap step is reached and the dependency is installed.

## Conventions

- Python 3.11+, type hints, `pathlib` for paths. Windows-first: no bash-only scripts, no symlinks,
  LF line endings. Scripts live in `scripts/` and run as `python scripts/<name>.py`.
- Every important output is structured JSON validated against `schemas/` before the next step uses it.
  Code, not the model, sets deterministic fields (`content_id`, `niche`, `language`, `content_type`,
  segment `index`, `estimated_duration_seconds`).
- Prompts live in `prompts/` as versioned files. Never keep production prompts only in code strings.
  Record prompt id, model and provider per video (`generate.py` prints the values for `log.csv`).
- If a step can be deterministic, write code, not an LLM call. A render must be reproducible from its
  render-spec JSON.
- Secrets live only in `.env` (gitignored). Env vars use the `FRAMESMITH_` prefix. Never print, log or
  commit keys. Send API keys in headers, never in URLs. Model names are not hard-coded: they go in `.env`.
- Kill switches: `FRAMESMITH_PUBLISHING_ENABLED` (default `false`) and `FRAMESMITH_GENERATION_ENABLED`.
  Any script that generates calls `common.require_generation_enabled()` first.
- `log.csv`: use only the values listed in `configs/brands/lanternfall.yaml` for `story_structure`,
  `hook_family`, `narrator_style` and `visual_treatment`. Repeat production fields on each platform row.
- GPU: one model loaded at a time. Narration runs on CPU. Do not suggest large local video models.
- Keep it small. Prefer the smaller, manual option and say what you skipped.

## Creative and policy rules (R7, Part XV)

- Originality over volume. No re-uploads, no franchise or copyrighted characters, no cosmetic edits of
  someone else's content, no fake "true story" framing, no generic motivational filler.
- YouTube targets templated, mass-produced content, so vary format: >= 3 story structures, 2 narrator styles,
  2 visual treatments, varied lengths; never two consecutive videos with the same structure.
- Build one owned universe: recurring original characters and a human-written premise for every video.
- Human pass on every script and final cut (5–10 minutes). Record it in `log.csv`. Agents draft; the owner
  approves. Generated ideas are raw material, not finished premises.
- No AI persona giving finance, medical or legal advice. No graphic violence, sexual content or hate.
- Use the platform's synthetic-media disclosure when content is realistic.
- Long-form: do not pad to reach 10 minutes, no 20–40 second static holds, change the shot every 4–8 seconds.
- Do not hide or delete published videos before the YouTube Partner Program application.

## Licensing and provenance

- "Open source" does not mean commercially unrestricted. Before using any model, checkpoint, voice, font,
  music or SFX in published work, add a row to `provenance/licenses.csv` with the license source.
- Keep the ComfyUI workflow JSON (seed, checkpoint, prompt) for every generated image in
  `comfyui/workflows/`. Unknown license or provenance means hold for human review.

## Commands

```text
python scripts/check_env.py
python scripts/generate.py ideas --count 10
python scripts/generate.py script --idea-file v1/ideas/<file>.json --pick 2
python scripts/validate.py script v1/scripts/lf-short-001.json
python scripts/build_render_spec.py v1/scripts/lf-short-001.json --audio v1/audio/lf-short-001.wav
python scripts/review.py
python -m pytest -q
python -m ruff check .
```

## Definition of done for a change

1. `python scripts/check_env.py` has no `[FAIL]` lines caused by the change (optional `[ -- ]` lines are fine).
2. `python -m pytest -q` and `python -m ruff check .` pass.
3. No secrets, no generated media and no large binaries are committed.
4. The change stays inside V1 scope. If it does not, stop and ask.
5. If it changes a decision, schema, brand rule, log column or the folder layout, `blueprint.md` is updated
   first. `Roadmap.md` boxes reflect reality.

## When unsure

Ask the owner before: spending money, creating accounts, publishing, deleting published work, adding a
dependency that needs a GPU, or building anything the blueprint gates behind V2/V3.
