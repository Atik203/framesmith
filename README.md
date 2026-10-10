# Framesmith

**A local-first, human-reviewed workbench for creating original short-form and long-form videos.** The project is
under active development: its current foundation is Python production scripts and a Remotion renderer. The planned
operator UI, resumable sequential workflow, image review screens, and full-motion video stage are not complete.

**Framesmith** is the project's only active identity. The current goal is the video-production workbench; a
separate content business, audience brand, and publishing plan are not active.

## Planned workflow

1. Draft five story ideas; the owner selects one or more.
2. Draft a premise and script; the owner edits and approves them.
3. Generate still images sequentially, then let the owner review and accept or replace them.
4. Only after an explicit owner action, generate motion shots. Local video generation is not the default because
   FramePack ran too slowly and stressed the owner's 6 GB laptop GPU. A paid image-to-video API is an optional,
   cost-visible path, not yet selected or enabled.
5. Assemble approved motion clips with narration and aligned captions, then run technical and visual QA.
6. Export the draft for owner review. Publishing integrations are outside the current project scope.

The local UI and complete workflow are roadmap goals, not current capabilities. A pan/zoom treatment over still images
is a draft/animatic and does not meet the project's full-motion quality bar. If no affordable, approved motion option
works, keep the reel marked as a draft.

## Current status

See [`Roadmap.md`](Roadmap.md) for verified progress and remaining work. [`blueprint.md`](blueprint.md) is the source
of truth; [`AGENTS.md`](AGENTS.md) contains repository instructions.

The repository contains code and small configuration/specification files. Generated images, audio, model weights,
rendered videos, secrets, and other large media are excluded from Git. A successfully rendered MP4 is not the same as
an owner-approved or publish-ready video.

## License and rights

Project code is licensed under [PolyForm Noncommercial 1.0.0](LICENSE). It permits the noncommercial and personal
uses described in that license; **commercial use is not granted**. This is a source-available license, not an OSI
open-source license. The license covers project code only. Dependencies, model weights, voices, fonts, music, sound
effects, and generated story/media outputs have separate terms; consult their own licenses and the records in
[`provenance/`](provenance/).

## Contributing and project policies

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a change. Please report security issues privately
using the process in [SECURITY.md](SECURITY.md), and follow the [Code of Conduct](CODE_OF_CONDUCT.md).
GitHub issue forms and the pull request checklist are provided under [`.github/`](.github/).

## GitHub project metadata

Suggested repository description: **A work-in-progress, local-first, human-reviewed AI video production workbench.**

Suggested topics: `ai-video`, `local-first`, `remotion`, `ollama`, `video-production`, `human-in-the-loop`.

## 1. Set up (Windows, PowerShell)

When the owner has made the repository public, clone it before running the setup commands:

```powershell
git clone https://github.com/Atik203/framesmith.git
Set-Location framesmith
```

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
Copy-Item .env.example .env        # then add your free-tier keys and model names
python scripts/check_env.py
python -m pytest -q
```

Install what `check_env.py` reports as missing. Node and FFmpeg are needed for rendering; ComfyUI and espeak-ng are
needed only for the corresponding local image/narration steps. Heavy audio packages are separate:
`python -m pip install -r requirements-audio.txt`.

For the Remotion renderer, install dependencies in `renderer/` with `npm ci`, then use `npm run lint` to run ESLint and TypeScript checks. Local media is ignored by Git.

### `.env`

Put the OpenRouter key in `.env` for free-first generation. Ollama runs locally as the second
fallback; OpenAI `gpt-6-luna` is last and limited to the existing $5 credit. Do not enable auto-recharge
or add credit. Model defaults are shown in `.env.example` and configured in `.env`; recheck free availability before generation.
`FRAMESMITH_PUBLISHING_ENABLED` stays `false`; publishing is outside the current project scope.

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
`configs/brands/framesmith.yaml`. Weekly 30-minute review: copy `notes/weekly-review.md` and run `review.py`.

## 5. What is not built yet

The local operator UI, resumable sequential workflow, image review flow, and full-motion video stage are not built.
There is no selected or enabled image-to-video API. `lf-short-001` has a technically valid MP4, but it remains a
draft: its scenes 6–8 use byte-identical images, and its pan/zoom motion did not meet the owner's quality bar. See
[`Roadmap.md`](Roadmap.md) for the quality hold and build phases. [`docs/renderer-setup.md`](docs/renderer-setup.md)
contains Remotion setup notes.
