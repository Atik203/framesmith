# AGENTS.md — Framesmith (audience-facing brand: Lanternfall)

Instructions for AI coding and content agents (Claude Code, Codex, Cursor, etc.) working in this repo.
Humans: start with `README.md`. Progress lives in `Roadmap.md`.

## What this project is

A local-first project for an AI-assisted English-language video business: short-form (Shorts/Reels/TikTok) plus
8–12 minute YouTube long-form. First vertical: **original AI cinematic stories**.

- Audience-facing brand: **Lanternfall**. Software project/repo name: **Framesmith**.
  Framesmith may appear on software repository pages; never put it in a Lanternfall video, caption,
  title, description, handle or other audience-facing brand page.
- Owner: Atikur, solo operator, Dhaka. Machine: Lenovo Legion 5 laptop, AMD Ryzen 7 5800H, **32 GB RAM**, RTX 3060 **6 GB**.
- Lanternfall business order: publish videos -> learn what earns -> earn -> automate content work. The owner has
  separately authorized phased development of the Framesmith local workbench under R15.

## Source of truth and progress

- `blueprint.md` is the single source of truth. **Revision 1.3 / R15 updates the software build direction
  and repo identity/license; R1–R14 still govern content, provenance, spend, and manual publishing unless
  R15 explicitly supersedes them.** Older text under superseded banners is historical reference.
- If a decision conflicts with the blueprint, update `blueprint.md` first (add a change-log entry in
  Part XXXVI), then implement. Do not leave decisions only in chat, code comments or commit messages.
- `Roadmap.md` is the checkbox tracker. When you finish a task, tick its box and add the date in the same
  change. Only tick a box when its "done when" is really true. Keep future phases unchecked until complete.
- External facts (YouTube/Meta/TikTok rules, prices, model and library versions) were checked on
  2026-10-08. Re-check before spending money or relying on them.

## Current stage: phased local-first workbench

- The current implementation is Python scripts plus one Remotion project and `log.csv`; the operator UI and
  resumable sequential workflow are planned, not yet implemented. Follow R15 and the staged Roadmap.
- Build the workbench incrementally without assuming a particular UI framework, database, or orchestration
  dependency. Prefer local files and a small serial job queue; add infrastructure only for a demonstrated need.
- Local video generation is not the default: the owner reports FramePack stresses the 6 GB laptop GPU and
  takes too long. Image-to-video APIs are optional, cost-visible, per-run approved, and disabled until the
  owner authorizes a budget. Still-image motion is not full-motion video.
- Do not add platform publishing adapters or unattended uploads. Publishing remains manual.
- Budget remains $0 by default and retains the existing $20 hard cap for the first 60 days. Never add a paid
  service, paid API key or subscription without the owner saying so.
- Gates A and B apply to publishing/business experiments, not to development of the workbench itself.
- Long-form (V1.5) remains a manual content pilot, not a reason to add publishing automation.
## V1 stack (blueprint R5)

| Function | Choice |
| --- | --- |
| Ideas and scripts | OpenRouter free model first, local Ollama second, then the owner's existing $5 OpenAI API credit as the paid final fallback through `scripts/generate.py`. No Gemini or OpenCode provider. Do not add credit or auto-recharge. |
| Images | ComfyUI, SDXL-family anime checkpoint, one image at a time on 6 GB. Check each checkpoint's commercial license. |
| Narration | Kokoro-82M on CPU. A/B candidate: Qwen3-TTS 0.6B. Never the 1.7B model. |
| Caption timing | Forced alignment of the known script to the audio (WhisperX or faster-whisper). Do not re-transcribe text we already have. |
| Render | Remotion + FFmpeg. Compositions `ShortVertical` (1080x1920) and `LongHorizontal` (1920x1080), 30 fps. |
| Music / SFX | Only assets with an explicit commercial license, recorded in `provenance/licenses.csv`. |
| Tracking | `log.csv`, one row per video per platform (columns in blueprint R14). |
| Publishing | Manual. Agents never publish or upload. |

The planned operator workflow pauses for owner approval at idea selection, script approval, image review,
paid video generation and final-cut review. Video generation never runs without an explicit click and budget
approval.

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
.ollama/models/                                              local Ollama model cache, gitignored
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
| `scripts/generate.py` | `ideas` and `script` subcommands. OpenRouter free tier, local Ollama, then optional OpenAI paid fallback; schema validation, up to 3 attempts per provider. Writes JSON plus a `.meta.json` with provider, model and prompt id. Rotates story structure so none repeats back to back. |
| `scripts/build_render_spec.py` | Script JSON (+ narration WAV length) -> `v1/renders/{id}.spec.json`. Shorts only. |
| `scripts/review.py` | Gate A/B progress, R7 variation rules, best/worst videos from `log.csv`. Read-only. |
| `scripts/common.py`, `scripts/llm.py` | Shared helpers (env, kill switches, ids) and the provider-fallback client. Import, do not run. |

`scripts/tts.py` and `scripts/align.py` exist. Not built yet: a standalone MP4 QA command, ComfyUI driver,
full-motion video generation, operator UI/job queue, and long-form script generation. Follow the staged Roadmap.

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
- The root `LICENSE` applies PolyForm Noncommercial 1.0.0 to project code only. It does not license generated
  media, models, voices, fonts, music, SFX or dependencies; check and record their own terms.
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
