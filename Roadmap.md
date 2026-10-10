# Roadmap — Framesmith / Lanternfall

Plan: [`blueprint.md`](blueprint.md) (Revision 1.2 and R14 win on conflicts) · Last updated: 2026-10-10
Stage: **V1, Day 0** — repo and tooling ready, nothing published yet.
First video published on: `____` (Gate A = day 14 from that date, Gate B = day 30).

How to use: `[x]` done, `[ ]` to do. **(you)** needs your hands, accounts or money. **(agent)** a coding agent can
do it. Tick a box only when its "done when" is true and add the date. Run `python scripts/review.py` for gate progress.

## Next actions (in order)

1. **(done 2026-10-10)** Repo pushed to GitHub; Python venv and declared dependencies installed; `python scripts/check_env.py` reports no `[FAIL]`.
2. Configure OpenRouter as the free first provider, local Ollama as second, and OpenAI as the last fallback using only the existing $5 credit.
3. **(you)** Choose and human-edit one of the three generated ideas, or write a new premise yourself.
4. **(you)** Install ComfyUI and Kokoro; fill the brand TODOs in `configs/brands/lanternfall.yaml`.
5. **(you)** Do the free platform setup in the R9 track below; it takes a month for AdSense review, so start early.

---

## Phase 0 — Planning and repo

- [x] Master blueprint, revisions 1.1 and 1.2: revenue-first gates, zero-cost stack, long-form pilot (2026-10-08)
- [x] Brand decided: Lanternfall public, Framesmith internal (R13) (2026-10-08)
- [x] Repo scaffold: AGENTS.md, CLAUDE.md, README, `.env.example`, `.gitignore`, folders (2026-10-10)
- [x] `blueprint.md` in the repo; contradictions fixed; repo conventions recorded as R14 (2026-10-10)
- [x] JSON Schemas and examples: idea, script, render spec (2026-10-10)
- [x] Prompt files: `story_idea_v1`, `story_writer_v1` (2026-10-10)
- [x] Brand config with structure, hook, narrator and visual lists (2026-10-10)
- [x] Tools: `check_env`, `validate`, `generate` (idea and script, provider fallback), `build_render_spec`, `review` (2026-10-10)
- [x] Tests and lint pass (`pytest`, `ruff`); provider calls tested against mocked HTTP only (2026-10-10)
- [x] `Roadmap.md` (2026-10-10)
- [x] Git repo initialized on `main`, first commit pushed to GitHub (2026-10-10)
- [x] Python 3.11+ venv and project/dev requirements installed (2026-10-10)
- [x] `python scripts/check_env.py` shows no `[FAIL]` (2026-10-10)

## Phase 1 — Day 1: setup, script, voice (R11)

Done when: one idea becomes one valid script JSON and one WAV.

- [x] Node LTS, FFmpeg 9.0.2 and Git on PATH (`check_env.py` confirms) (2026-10-10)
- [x] OpenRouter, local Ollama, and OpenAI (last fallback, existing credit only) configured in `.env` (2026-10-10)
- [x] Install Ollama, pull `qwen3.5:4b-q4_K_M`, and verify local inference on the RTX 3060 (2026-10-10)
- [x] Move the complete local repository to `G:\framesmith`; place Ollama models under ignored `.ollama\models` and remove old E:/C: copies after verification (2026-10-10)
- [x] `python scripts/generate.py ideas --count 3` works through OpenRouter free model and writes valid JSON (2026-10-10)
- [ ] **(you)** Edit the chosen premise yourself (R7), then `python scripts/generate.py script ...` gives a valid script
- [ ] **(you)** Brand sheet: narrator voice (audition the Kokoro candidates), image checkpoint, caption font, one character, a second narrator style and a second visual treatment
- [ ] **(you)** Install ComfyUI (Windows portable), generate one SDXL-family anime image, save the workflow JSON in `comfyui/workflows/`
- [ ] **(you)** License rows in `provenance/licenses.csv` for the checkpoint, the voice and the font
- [ ] **(you)** Install espeak-ng, then `pip install -r requirements-audio.txt`
- [ ] **(agent)** `scripts/tts.py`: script JSON to `v1/audio/{id}.wav` with Kokoro at 24 kHz on CPU, honoring the kill switch (needs Kokoro installed to test)
- [ ] One test sentence rendered to a 24 kHz WAV and listened to

## Phase 2 — Day 2: visuals and render

Done when: one complete MP4 passes the Part IX technical checks.

- [ ] 6–10 stills for one story, one image at a time; seed, checkpoint and license logged
- [ ] **(agent, optional)** `scripts/images.py` ComfyUI API driver, only if doing it by hand costs over ~2 h/week (R1)
- [ ] **(agent)** `scripts/align.py`: align the known script to the WAV (WhisperX or faster-whisper) and write `v1/subtitles/{id}.json`, 1–7 words per chunk
- [x] `python scripts/build_render_spec.py ... --audio ...` writes `v1/renders/{id}.spec.json` (2026-10-10)
- [x] **(you + agent)** Remotion project `renderer`; `ShortVertical` reads the spec with push-in and pan motion and draws the captions (2026-10-10)
- [ ] **(you)** Normalize narration, duck licensed music, final FFmpeg encode (H.264, AAC, yuv420p)
- [ ] **(agent)** `scripts/qa_check.py`: ffprobe checks from Part IX (container, codec, 1080x1920, stable fps, audio present, no black first or last frame)
- [ ] Watch on a phone; fix pacing, caption size and audio
- [ ] First complete MP4 passes the checks

Render note (2026-10-10): `v1/renders/lf-short-001.mp4` was rendered and passed MP4 stream inspection and
full decode. Representative frames showed readable captions, but `scene-06.png`, `scene-07.png` and
`scene-08.png` are byte-identical, repeating one sunrise image across three beats. Replace or re-plan those
scenes and inspect the final cut (including on a phone) before checking off visual QA. No human approval or
publication is recorded.

## Phase 3 — Day 3: batch and publish

- [ ] 3–5 videos with different story structures (R7)
- [ ] Human pass on each script and final cut (5–10 min each); active minutes logged
- [ ] R9 platform setup done (see track below)
- [ ] 2–3 videos published manually, with the synthetic-media disclosure where offered
- [ ] Each video added to `log.csv` (URL, date, structure, hook family, narrator, visual, script version, models)
- [ ] Metrics recorded at 24 hours and 72 hours

## Phase 4 — Days 4–14: Gate A

- [ ] One video per day, 10 published by day 14
- [ ] Weekly 30-minute review: copy `notes/weekly-review.md`, run `python scripts/review.py`
- [ ] **Gate A** (day 14): 10 videos, every video has recorded active time ≤ 60 min, spend within budget
- [ ] Gate A outcome written into `blueprint.md`

## Week 1–2: before the long-form pilot (R12 prerequisites)

- [ ] 5–10 Shorts completed through the pipeline
- [ ] One stable narrator and one visual brand style
- [ ] `LongHorizontal` (1920x1080) composition using the same render-spec props
- [ ] One story premise that supports 1,300–1,800 spoken words without filler
- [ ] **(agent)** Long-form script flow: outline, section drafts, polish (new prompt files and a `longform` command; build only when the first premise is ready)
- [ ] Thumbnail and title packaging step (manual, three concepts and four titles per episode)

## Weeks 2–3: V1.5 long-form pilots

- [ ] Pilot 1 published (8–12 min, human-written premise, 3+ derivative Shorts)
- [ ] Pilot 2 published, different structure and packaging
- [ ] Pilot metrics logged: CTR, first-30-second retention, average view duration, % viewed, subscribers gained, production hours
- [ ] Scale or stop decision recorded in the blueprint (R12 decision matrix)

## Gate B (day 30)

- [ ] 30 Shorts published
- [ ] 2 long-form pilots published with a decision
- [ ] Viewed-vs-swiped ≥ 65% on the top third
- [ ] At least 3 videos above 10k views
- [ ] One format clearly ahead (see `review.py` medians)
- [ ] Spend ≤ $20
- [ ] If it fails: change hook family, format or niche (Part II), not the tooling

---

## Parallel tracks

### Platform setup (R9, free, start early)

- [ ] **(you)** YouTube channel under the final brand, 2-step verification on
- [ ] **(you)** Link AdSense with a Bangladesh address (review takes about a month)
- [ ] **(you)** YouTube Studio: Earn tab, turn on "Get notified"
- [ ] **(you)** Facebook Page in Professional Mode; register interest in Content Monetization
- [ ] **(you)** Instagram and TikTok accounts

### Naming and brand checks (R13)

- [x] Brand and codename decided (2026-10-08)
- [x] TikTok handle reported available (owner check, 2026-10-08)
- [ ] **(you)** YouTube handle: `@lanternfall` is taken by an empty channel; pick one variant and use it everywhere
- [ ] **(you)** Instagram and Facebook Page names
- [ ] **(you)** Domain (.com plus one backup), checked at a registrar
- [ ] **(you)** Trademark search: USPTO, WIPO Global Brand Database, home-country registry (entertainment and video classes)
- [ ] No money on a domain, ads or merchandise until the checks above pass

### Bridge income (R4.5, cap about 25% of time)

- [ ] **(you)** Decide whether to offer short AI story videos as a service
- [ ] **(you)** Verify a payout method that works in Bangladesh before taking a client

### Standing hygiene

- [ ] Add a `provenance/licenses.csv` row for every model, voice, font and track before using it
- [ ] Re-check platform rules, free-tier limits and prices before spending money (facts dated 2026-10-08)
- [ ] Note in `blueprint.md` the first time the stricter YouTube bar (from 2027-02-01) changes a plan

---

## Locked: V2 (opens at Gate C, about $500/month net for 2 consecutive months)

Do not start. When Gate C passes, spend $100–200/month in this order (R6), and automate only the manual step that costs the most minutes.

- [ ] Narration quality (paid voice, A/B tested against Kokoro)
- [ ] Stronger script model and more drafts per idea
- [ ] Hook and key-scene visuals (short image-to-video clips)
- [ ] Music, SFX or tools
- [ ] Automate the single most repetitive manual step, picked from `log.csv` active minutes

## Locked: V3 (opens at Gate D, about $2,000–3,000/month net for 3 consecutive months)

Do not start. Reference list only (Parts V, VI, Appendix C): durable workflows, database, dashboard, model gateway, platform adapters, multiple brands, service productization.

## Watch list

- Free-tier quotas and model names change often; the provider fallback exists for that reason.
- YouTube's inauthentic-content enforcement targets templated AI output; the variation rules (R7) are the defense.
- Long-form is capped at 1 per week (never more than 2); retention matters more than length.
- Remotion needs a company license at 4+ people or when sold as a product.
- 6 GB GPU: one model loaded at a time; narration stays on CPU.
