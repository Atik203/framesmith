# Lanternfall — AI Content Automation Business (codename: Framesmith) — Master Blueprint
**Status:** Living source of truth / implementation blueprint
**Version:** 1.4 (phased Framesmith workbench + Lanternfall content business) — see Revision 1.3 / R15 below for the current project build direction.
**Blueprint date:** 2026-10-10
**Names:** Framesmith is the software project/repository name and may appear on its public source-code pages. Lanternfall is the audience-facing video brand. See R13 and R15.
**Primary objective:** Build a profitable, scalable, multi-niche, multi-platform English-language short-form content business using agentic automation, with human oversight during the early stages and progressively higher automation as the system proves itself.
**Initial constraint:** V1 must be buildable in roughly 2–3 days and must be able to produce real videos. Platform publishing can be manual at first; the first target is 5–10 published videos, not a perfect autonomous factory.
**Source-of-truth rule:** When implementation decisions conflict with this document, update this file first, then implement. Do not allow architecture, prompts, model choices, credentials, platform rules, or business assumptions to exist only in chat history.
## Revision 1.2 — Revenue-First, Budget-Gated Plan with V1.5 Long-Form Pilot (2026-10-08)
**Status:** R1–R14 govern Lanternfall content, publishing, rights, and business gates. Revision 1.3 / R15 below supersedes only conflicting software-project scope, repository identity, and source-availability decisions. Parts II–XXXVIII remain reference material; the long-form pilot (R12, Part IV.5) is a content experiment. Facts below were checked against the web on 2026-10-08; recheck before spending money.

## Revision 1.3 — Review-Gated Framesmith Workbench (2026-10-10)
**Status:** R15 below updates the software-project scope and public-source terms. It supersedes conflicting R1/R2/R13 statements about whether to build a local UI now and whether the Framesmith name may appear on software-repository pages. R1–R14 still govern Lanternfall content, human approval, rights/provenance, spending, and manual publishing unless R15 explicitly says otherwise. Framesmith is not yet a completed application; Roadmap.md records the actual state.

### R15. Project direction, generation gates, and source availability
- Build Framesmith in phases as a local-first, human-reviewed production workbench. The owner has chosen to develop the software workflow before proving the content business gates; Gate A/B and revenue gates remain business/monetization decisions, not prerequisites for the UI or workflow engine.
- Keep the current Windows-first scripts and Remotion renderer as the production foundation. A local UI and a resumable, sequential job queue are planned, not implemented. Select the UI/runtime stack in a focused design step before adding it; do not introduce a broad agent framework, database, cloud orchestration service, or publishing integration by default.
- Treat “agents” as bounded steps in one ordered pipeline. Run one model/GPU-heavy task at a time; stop/unload one local model before loading another. CPU narration, caption alignment, and deterministic rendering may follow. Persist each step's inputs, outputs, status, and errors so a failed run can resume without regenerating approved assets.
- Target workflow: (1) draft five ideas; (2) owner chooses one or more; (3) draft premise/script and owner edits/approves; (4) generate stills sequentially; (5) owner reviews, accepts, or requests replacement; (6) only after an explicit owner click, generate motion shots; (7) assemble approved clips with narration, aligned captions, and licensed sound; (8) run technical and visual QA; (9) owner reviews final cut and publishes manually.
- Make each approval a real stop in the queue: idea selection, script approval, image approval, any paid video-generation request, and final-cut approval. No agent publishes, uploads, or silently spends money.
- The owner has tested FramePack and reports excessive laptop stress and slow generation on the RTX 3060 Laptop GPU with 6 GB VRAM. Do not make local video generation the default or promise it will be usable. Revisit only after a measured, owner-approved test.
- Image-to-video APIs are optional experiments, not a default dependency. Before a paid request, show provider, shot duration/resolution, estimate including retries, and cumulative reel spend; require the owner to approve each run within a configured cap. Do not add credits, activate a subscription, or call a paid API without explicit approval. Recheck live prices and terms at test time. If no affordable option meets the motion-quality bar, stop and label the reel a draft; do not call a pan/zoom slideshow a fully animated video.
- Keep idea/script generation, local image generation, Kokoro narration, forced alignment, Remotion/FFmpeg assembly, QA, and the UI usable without video-generation API spend. Keep platform publishing manual.
- The repository may be made public by the owner as a source-available software project under PolyForm Noncommercial 1.0.0. This license is for the project code; it does not grant rights to generated stories/media, third-party dependencies, voices, models, fonts, or music. Maintain their separate terms and provenance. No generated media, model weights, secrets, or large binaries go into Git. Do not describe the project as OSI open source.
- A GitHub repository description and topics should describe an in-progress, local-first, human-reviewed video workbench and must not imply that full-motion generation, a UI, or publishing automation is already working.

### R1. Priority change
For the Lanternfall content business, the order remains (1) publish videos, (2) learn what earns, (3) earn, (4) automate content work. For the Framesmith software project, R15 authorizes phased local workbench development before those business gates.
- Avoid adding production tooling just to automate a task that has not become a demonstrated bottleneck; R15's explicitly requested local UI and resumable queue are the exception.
- The present foundation is Python scripts, one Remotion renderer, and one tracking sheet. The local UI is planned and must not be described as built.
- Content-business success is still measured in published videos and viewer behavior, not architecture.

### R2. Budget gates
| Stage | Enter when | Monthly spend | What may be built |
| --- | --- | --- | --- |
| V1 | now | $0 (hard cap $20 total in the first 60 days, only to remove one named bottleneck) | scripts, ComfyUI, Kokoro, Remotion, tracking sheet, phased local UI/serial queue per R15 |
| V1.5 | week 2, once the R12 prerequisites are met | $0 | manual long-form pilots on the V1 stack; no new infrastructure |
| V2 | net cash revenue of about $500/month (proposed: 2 consecutive months, all platforms and lanes) | $100–200 | quality upgrades first (R6), then automate the single most repetitive manual step |
| V3 | net cash revenue of about $2,000–3,000/month (proposed: 3 consecutive months) | proposed: up to 30% of trailing 3-month net revenue | robust framework, service productization, second business |

Net revenue means money received, not dashboard estimates.
R15 supersedes these revenue gates only for the requested local UI and sequential workbench. Paid video APIs, cloud services, publishing integrations, and the broader V2/V3 business stack remain gated and require owner authorization.

### R3. Monetization reality check (verified 2026-10-08)
| Platform | Current rule | Implication |
| --- | --- | --- |
| YouTube full YPP (ads) | 1,000 subs + 10M qualified Shorts views in 90 days, or 4,000 watch hours in 12 months. From 2027-02-01 new applicants need 20M Shorts views or 8,000 hours. Review takes about a month. | Plan for the stricter bar; treat ad revenue as a 6–12+ month goal |
| YouTube early tier | 500 subs + 3 public uploads in 90 days + 3M Shorts views (or 3,000 hours): fan funding, Shopping, Creator Partnerships, no ads | First YouTube money may come from brand deals, not ads |
| YouTube Shorts ads after 2027-02-01 | Shorts ad revenue requires 10M Shorts views in the trailing 90 days, checked monthly | Shorts alone is a thin revenue source |
| Shorts RPM | Published data ranges about $0.02–$1.48 per 1,000 views by niche; typically $0.03–$0.30 | Plan $50–$250 per 1M views; entertainment fiction sits at the low end |
| Facebook Content Monetization | Invite-only; Meta publishes no simple country list; register interest in Professional Dashboard | Worth applying early, but do not forecast it |
| TikTok Creator Rewards | Needs videos over 1 minute and an eligible country; published lists (US, UK, DE, FR, BR, JP, KR, AU, CA, MX, ES, IT) do not include Bangladesh | Use TikTok for distribution, not income; confirm in-app |
| Instagram | No per-view pool; brand deals and invite-only bonuses | Distribution and brand deals only |

Bangladesh specifics: Bangladesh is on YouTube's standard YPP availability list (check Studio for the 500-subscriber tier). AdSense payment options listed for Bangladesh are check and wire; EFT is not listed. Earnings are held until the payout threshold (about $100) is reached.

Revenue math:
- $500/month from Shorts ad revenue alone needs roughly 2M–10M monetized Shorts views per month (at $0.25–$0.05 RPM).
- The same $500 from long-form needs roughly 220k views per month at the $2.30 median RPM reported across established channels.
- Viewer geography drives RPM more than creator location. English audiences in the US, UK, Canada and Australia pay several times more than South Asian audiences.

Conclusion: platform ad payouts are a slow lane. The $500/month gate is reachable sooner by running several revenue lanes in parallel (R4).

### R4. Revenue lanes (run in parallel, cheapest first)
1. **Shorts as the audience funnel** on YouTube, Facebook, Instagram and TikTok. Goal: subscribers and median views, not payouts.
2. **Long-form companion / core episode** (8–12 minute target, one per week after the V1.5 pilot). Long-form is primarily a YouTube watch-hours and higher-value monetization lane; 8+ minutes can support mid-roll ads after monetization. Build it as a complete story or explainer, not a stitched compilation of Shorts. Each long-form episode should also feed 3–8 derivative Shorts. Working hypothesis: long-form becomes the main YouTube revenue track; the two pilots decide whether that holds.
3. **Facebook Content Monetization**: register interest now, keep content original and English.
4. **Affiliate links and owned digital products** once an audience exists (story packs, prompt or template packs). Do not assume TikTok Shop is available in Bangladesh.
5. **Bridge income (recommended):** sell the same pipeline output as a service (short AI story or explainer videos for clients). Cap at about 25% of time. Purpose: reach the V2 gate without waiting on platform payouts. Verify a payout method that works in Bangladesh first.

### R5. V1 zero-cost stack (supersedes "V1 Model Choices")
| Function | Choice | Cost | Notes |
| --- | --- | --- | --- |
| Ideas and scripts | OpenRouter `nvidia/nemotron-3-ultra-550b-a55b:free` first; local Ollama `qwen3.5:4b-q4_K_M` second; OpenAI `gpt-6-luna` last | $0 while OpenRouter or Ollama succeeds; existing $5 OpenAI API credit only if both fail | Supported V1 chain is OpenRouter → local Ollama → OpenAI. Gemini returned HTTP 402 for depleted prepay credit; OpenCode Zen free inference returned HTTP 403 outside its app. Do not add credit or auto-recharge. Set a $5 OpenAI project spend limit. Models and quotas change; recheck before use. OpenRouter's selected free model does not enforce JSON mode; app schema validation does. Ollama uses the local `/api/chat` endpoint with JSON format and 8K context. |
| Images | ComfyUI (v0.18+ has Dynamic VRAM by default) with an SDXL-family anime checkpoint (Illustrious or NoobAI) as the default; test Z-Image Turbo and FLUX.2 Klein 4B GGUF Q4 | $0 | One image at a time on 6 GB. Verify each checkpoint's commercial license and store it in the asset log. Gemini image free quotas are inconsistent across sources; treat as a bonus only. |
| Narration | Kokoro-82M (Apache-2.0, about 300 MB, real-time on CPU) | $0 | Keeps the GPU free for images. A/B test Qwen3-TTS 0.6B (Apache-2.0 upstream; a community server reports about 4 GB VRAM in use). Skip the 1.7B model. |
| Caption timing | Forced alignment of the known script to the audio (WhisperX or faster-whisper word timestamps) | $0 | Do not re-transcribe text you already have. |
| Render | Remotion + FFmpeg | $0 | Remotion is free for individuals and companies up to 3 people; a company license applies at 4+ people or when sold as a product. |
| Music and SFX | Only assets with explicit commercial licenses (for example YouTube Audio Library) | $0 | Store the license reference per track. |
| Tracking | One CSV, `log.csv` in the repo root (a Google Sheet copy is optional), one row per video per platform | $0 | Columns are defined in R14. Record metrics at 24 hours and 72 hours, then refresh `views_latest` weekly. |
| Publishing | Manual | $0 | |

Deferred until a gate and a proven manual pain: Temporal, Redis, LiteLLM server, OpenAI Agents SDK, FastAPI, Next.js dashboard, Postgres/pgvector (SQLite until it hurts). The $20 reserve may be spent only after a bottleneck is written down in the tracking sheet, on one item.

### R6. V2 upgrade order ($100–200/month)
Spend by expected retention impact:
1. Narration quality: paid voice, A/B tested against Kokoro (about 35%); a flat voice costs the most retention over 10 minutes.
2. Stronger script model and more drafts per idea (about 25%).
3. Hook and key-scene visuals: short image-to-video clips (about 25%).
4. Music, SFX or tools (about 5%).
5. Buffer (about 10%).
Check live prices on the purchase day; none are recorded here. Automate only the manual step that costs the most minutes.

### R7. Creative rules driven by YouTube's inauthentic-content policy
YouTube targets templated, mass-produced, easily replicated content, including generic AI output; AI use itself is not penalized. Reviewers assess the whole channel, and they look at what the creator added.
- Vary format every week: at least 3 story structures, 2 narrator styles, 2 visual treatments, varied lengths. No two consecutive videos with the same structure.
- Build one owned universe: recurring original characters and a human-written premise per video.
- Human pass on every script and final cut (target 5–10 minutes) and record it in the log.
- No AI persona giving finance, medical or legal advice.
- Use the platform's synthetic-media disclosure when content is realistic.
- Do not hide or delete old videos before applying for YPP; they carry qualifying views.
- Start with one channel; several channels on one template raise enforcement risk.
- Delete or rework low-effort early uploads before applying.

### R8. Gates (starting thresholds; adjust after real data)
| Gate | When | Pass condition |
| --- | --- | --- |
| A | day 14 | 10 videos published; active time at most 60 minutes per video; cost within budget |
| B | day 30 | 30 Shorts published and at least 2 long-form pilots published with a scale/stop decision (R12); viewed-vs-swiped at least 65% on the top third; at least 3 videos above 10k views; one format clearly ahead; spend at most $20 |
| C (enter V2) | revenue | about $500/month net for 2 consecutive months |
| D (enter V3) | revenue | about $2,000–3,000/month net for 3 consecutive months |

If Gate B fails, change the hook family, format or niche (next vertical in Part II), not the tooling. This replaces the 5–10 video batch in the V1 Definition of Done, which is too small to validate anything.

### R9. Setup checklist (free, do first)
- Create the YouTube channel under the final brand; enable 2-step verification; link AdSense with a Bangladesh address; note that review takes about a month.
- Create a Facebook Page with Professional Mode; register interest in Content Monetization; create Instagram and TikTok accounts.
- In YouTube Studio, open the Earn tab and turn on "Get notified".
- Keep a license record for every model, checkpoint, voice and music file.

### R10. Sources checked 2026-10-08
- YouTube Partner Program guide with the 2027 thresholds: https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide
- YPP availability by country: https://support.google.com/youtube/answer/7101720
- Expanded YPP: https://support.google.com/youtube/answer/13429240
- AdSense payment options: https://support.google.com/adsense/answer/1714397
- Shorts RPM data: https://air.io/en/air-data-findings/youtube-shorts-rpm-vs-long-form-how-much-do-shorts-earn-in-2026
- Remotion license: https://www.remotion.dev/docs/license/pricing
- Facebook Content Monetization overview: https://socialbee.com/blog/monetize-facebook-reels/
- Free LLM API tiers: https://openrouter.ai/blog/tutorials/free-llm-apis-compared/
- Low-VRAM ComfyUI notes: https://eastondev.com/blog/en/posts/ai/20260721-comfyui-low-vram-acceleration/
- Kokoro-82M: https://huggingface.co/nvidia/kokoro-82M-onnx-opt

### R11. Days 1–3 build checklist (zero-cost stack)
Scope rule: if a step slips by more than half a day, cut scope rather than extend the schedule. Exact install commands change; follow each project's README. Progress is ticked in `Roadmap.md`.

**Day 1 — setup, script, voice**
- [ ] Create the repo and the folders `v1/{ideas,scripts,assets,audio,subtitles,renders,published}` plus `log.csv` (columns from R14).
- [ ] Install Python 3.11+, Node LTS, FFmpeg, Git. Confirm each with `--version`.
- [ ] Install ComfyUI (Windows portable build) and generate one SDXL-family anime image. Save the workflow JSON.
- [ ] Install Kokoro (`pip install kokoro soundfile`, plus espeak-ng) and render one test sentence to a 24 kHz WAV.
- [x] Configure OpenRouter first, local Ollama second, and OpenAI `gpt-6-luna` last with only the existing $5 credit; store cloud keys in `.env`, never in git. Ollama needs no API key. (2026-10-10)
- [ ] Write one script: idea JSON, then timed script JSON (Part IV schema), with schema validation, 3 retries, and provider fallback.
- [ ] Fix the brand sheet: name, narrator voice, visual style, one character identity block.
- [ ] Done when: one idea becomes one valid script JSON and one WAV.

**Day 2 — visuals and render**
- [ ] Generate 6–10 stills for one story, one image at a time. Log seed, checkpoint and its license.
- [ ] Get word timestamps by aligning the known script to the audio (WhisperX or faster-whisper word timestamps). Output captions as JSON or ASS.
- [ ] Create the Remotion project (`npx create-video@latest --yes --blank renderer`). Name the first composition `ShortVertical` and build one 1080x1920, 30 fps composition that reads the render-spec JSON (Part IV) with push-in and pan motion.
- [ ] Captions: 1–7 words per chunk, inside the safe zone, high contrast.
- [ ] Audio: normalize narration, duck licensed music, final FFmpeg encode (H.264, AAC, yuv420p).
- [ ] Watch on a phone and fix pacing, caption size and audio.
- [ ] Done when: one complete MP4 passes the Video QA Technical Checks in Part IX.

**Day 3 — batch and publish**
- [ ] Make 3–5 videos with different story structures (R7 variation rule).
- [ ] Human pass on each script and final cut (5–10 minutes); log active minutes.
- [ ] Complete the R9 platform setup; publish 2–3 videos manually, using the synthetic-media disclosure where offered.
- [ ] Add each video to `log.csv` with URL, date, script version and model names.
- [ ] Record metrics at 24 hours and 72 hours.

**After Day 3**
- [ ] One video per day: 10 by day 14 (Gate A), 30 by day 30 (Gate B).
- [ ] Weekly 30-minute review: best and worst three videos, then decide the next week's formats (`python scripts/review.py`, `notes/weekly-review.md`).
- [ ] Week 1 (before the pilot): add the `LongHorizontal` (1920x1080) composition using the same render-spec props, then check the R12 prerequisites.
- [ ] Weeks 2–3: run the long-form pilots (R12, Part IV.5).

**Fallbacks**
- Image generation too slow: use fewer stills per video (6) or generate manually in the Gemini app and import.
- Remotion slows you down: burn ASS captions and motion with FFmpeg only until Gate A.
- Free OpenRouter quota hit: use the existing OpenAI credit only if needed; otherwise pause generation until the free quota resets.


### R12. Long-form expansion rule — V1.5 pilot in Weeks 2–3

The long-form track is now a first-class part of the business strategy. It is **not** a replacement for Shorts and it is not a reason to build the full V2 infrastructure early.

#### Strategic decision
- Keep Shorts as the **discovery and audience-acquisition layer** across YouTube, Facebook, Instagram, and TikTok.
- Add YouTube long-form as the **watch-hours, deeper relationship, and higher-value monetization layer**.
- Working hypothesis (expert view, to be tested): long-form is the main YouTube revenue track and Shorts are the funnel. The two pilots decide whether that holds.
- Start the long-form pilot in **Week 2**, after the first short-form production loop is working.
- Produce **one 8–12 minute long-form video per week**, with **10–12 minutes as the target for story episodes** when the story naturally supports that length. Do not pad a story just to reach 10 minutes.
- Run a second pilot in **Week 3** so the decision is based on at least two long-form experiments rather than one upload.
- When the long-form pilot works, promote long-form from Shorts rather than treating the formats as separate businesses.

#### Why the long-form track matters (verified 2026-10-08)
- Watch-hour route: 1,000 subscribers plus qualified public long-form watch hours. The bar is 4,000 hours today and **8,000 hours for new applicants from 2027-02-01**; plan for 8,000. Watch time from the Shorts Feed does not count. The Shorts route needs 10 million views (20 million from 2027-02-01).
- Views needed for 8,000 hours: about 60,000 at an 8-minute average view duration, about 120,000 at a 4-minute average.
- Monetized videos of 8 minutes or longer can use mid-roll ads.
- RPM: Shorts about $0.05–0.20 per 1,000 views; faceless long-form estimates run $2–12 (vendor estimates; AIR's median across established channels is $2.30). Plan with $2–6, about $200–600 per 100,000 views once monetized. None of this is guaranteed: revenue depends on audience, niche, retention, geography, advertiser demand and eligibility.
- Before YPP approval ad revenue is $0, so the bridge lane in R4 stays. Recheck current YouTube policies before monetization decisions.

#### Risks
- Long-form AI slideshows are the pattern YouTube's inauthentic-content enforcement targets most. Reports describe multiple long-form uploads per day as a red flag, and a large faceless story channel was fully demonetized. Cap at 1 long-form video per week (never more than 2).
- Ten minutes of stills with flat narration loses viewers. Retention is the product.
- Production time is higher: budget 3–5 active hours per video for the first pilots.
- Apply R7 to every episode: human-written premise and point of view, a human edit pass, a distinct structure and packaging each time, and an honest answer to the Studio synthetic-content disclosure question. Recording your own narration is the strongest authenticity signal; optional.

#### Important economics rule
Do not assume:

`1 long video = 10–15 Shorts` in either reach or revenue.

Instead use:

`1 strong long-form story -> 3–8 derivative Shorts -> cross-platform distribution -> traffic back to the long-form episode where appropriate.`

The long-form episode becomes the **primary IP asset**, while Shorts become discovery clips, hooks, scenes, questions, alternate openings, and standalone micro-stories derived from the same creative universe.

#### V1.5 gate
The long-form pilot can begin **before the formal V2 revenue gate** because it is a content experiment, not a framework build.

Required before Week 2:
- At least 5–10 Shorts completed through the V1 pipeline.
- One stable narrator and one visual brand style.
- One reusable 16:9 render template (`LongHorizontal`).
- One story premise strong enough to support 1,300–1,800 spoken words without filler.

#### V1.5 target
- Week 2: Long-form Pilot #1, 8–12 minutes.
- Week 3: Long-form Pilot #2, 8–12 minutes.
- Each long-form episode should generate at least 3 candidate Shorts.
- Track production hours, render time, cost, CTR, first-30-second retention, average view duration, average percentage viewed, subscribers gained, and downstream Shorts performance.

#### Scale / stop rule
After two pilots:
- If long-form shows materially stronger watch time, subscriber conversion, or business economics than Shorts, increase to one long-form episode per week.
- If the stories perform but production is too expensive, reduce visual complexity rather than abandoning long-form.
- If viewers consistently leave early, fix the opening, narrative structure, thumbnail/title, and pacing before adding more volume.
- If long-form adds little audience value and consumes excessive production time, keep it as an occasional premium format and return capacity to Shorts.

#### V2 long-form objective
Once the content model is proven and the V2 gate is reached, automate the long-form pipeline using the same content objects, research agents, story agents, visual planning, TTS, rendering, QA, analytics, and platform adapters. Do not create a separate application for long-form.

### R13. Naming and brand (decided 2026-10-08)
| Item | Decision |
| --- | --- |
| Public brand | **Lanternfall** (display name on every platform) |
| Software project/repo name | **Framesmith**. May be used on GitHub/source-code project pages. It must not appear in Lanternfall videos, captions, titles, descriptions, handles, or audience-facing brand pages. |
| First brand config | `configs/brands/lanternfall.yaml`, `brand_id: lanternfall` |
| Naming conventions | repo `framesmith`; env prefix `FRAMESMITH_`; bucket `framesmith`; Remotion project `renderer` |

Handle rule: YouTube display names do not need to be unique, but handles do. Use `@lanternfall` where free; otherwise use one variant (`@lanternfallstories`, `@lanternfalltales` or `@lanternfallofficial`) and keep the display name "Lanternfall". Prefer the same handle on every platform.

Availability status (owner checks plus web search, 2026-10-08):
| Check | Status |
| --- | --- |
| TikTok handle | reported available (owner check) |
| YouTube | a channel named Lanternfall exists but is empty; use a handle variant |
| Instagram, Facebook Page | pending |
| Domain (.com plus one backup) | pending |
| Trademark: USPTO, WIPO Global Brand Database, home-country registry | pending; check entertainment and video classes |
| Web search for existing brands | no exact-name conflict found for Lanternfall; "Lantern/Lanterns" is a busy term (for example an HBO Max series); Frameo.ai is a similar-looking name in the AI story-video category, so recheck Framesmith before ever selling it as a tool |

Rules:
- Do not spend money on a custom domain, ads or merchandise until the pending checks pass.
- Web search cannot confirm handle or domain availability; only the platforms and registrars can.
- If the trademark check turns up a conflict, rename before the channel has an audience.

### R14. Repo and tooling conventions (decided 2026-10-10)
Building the repo scaffold turned several open details into decisions. They bind code and agents; change them here first.
| Item | Decision |
| --- | --- |
| Agent entry points | `AGENTS.md` (rules for coding agents), `CLAUDE.md` (imports AGENTS.md) and `Roadmap.md` (checkbox progress tracker; tick a box and add the date in the same change that finishes the task). |
| Content IDs | `lf-short-001`, `lf-long-001`, and so on. Derivative Shorts set `parent_content_id` to the long-form episode. Pattern `^[a-z0-9][a-z0-9-]{2,40}$`. |
| Schemas | `schemas/{idea,script,render_spec}.schema.json` are strict (`additionalProperties: false`) so model drift fails validation and triggers a retry. Idea scores are integers 1–5: 5 is best for `visual_potential` and `novelty`; 5 is worst for `production_difficulty` and `policy_risk`. |
| LLM calls | Providers in `FRAMESMITH_LLM_PROVIDERS` order (default openrouter, ollama, openai). OpenRouter is the free attempt; local Ollama is the no-cost second fallback; OpenAI is last and may spend only the existing $5 credit. Up to `FRAMESMITH_LLM_MAX_RETRIES` (3) attempts per provider; invalid output is fed back to the model; then the next provider. Model names are configured in `.env` and recorded per video. Code sets `content_id`, `niche`, `language`, `content_type`, segment `index` and `estimated_duration_seconds`. |
| Prompts | `prompts/niches/ai_stories/*_v1.md`; the `id` in each file's front matter is the prompt version. `scripts/generate.py` writes `{content_id}.meta.json` next to each script with provider, model, prompt id and story structure. |
| Render spec | Paths are relative to `v1/`: `assets/{id}/scene-01.png`, `audio/{id}.wav`, `subtitles/{id}.json` (Remotion draws the captions; `.ass` only for the FFmpeg-only fallback). Specs are saved as `v1/renders/{id}.spec.json` and committed, so a render can be reproduced. Shorts are 1080x1920, long-form 1920x1080, both 30 fps. |
| Tracking log | `log.csv` columns: `content_id, content_type, parent_content_id, title, date, platform, url, story_structure, hook_family, narrator_style, visual_treatment, duration_seconds, script_version, model_names, active_minutes, cost_usd, human_pass, disclosure, views_24h, views_72h, views_latest, viewed_vs_swiped, avg_pct_viewed, followers_gained, ctr, first30_retention, avg_view_duration_s, notes`. Repeat the production fields on every platform row of a video. `scripts/review.py` takes the maximum of `active_minutes` and `cost_usd`, sums views and averages percentages per video. |
| Kill switches | `FRAMESMITH_PUBLISHING_ENABLED` (default `false`) and `FRAMESMITH_GENERATION_ENABLED`; scripts call `common.require_generation_enabled()` before any generation. |
| Tooling | Current scripts are `check_env`, `validate`, `generate`, `build_render_spec`, `review`, `tts`, and `align`. A standalone MP4 QA command, ComfyUI driver, operator UI/job queue, full-motion video generation, and long-form script generation are not built. See R15 and Roadmap.md for the build phases. |
| Brand lists | `configs/brands/lanternfall.yaml` holds the allowed `story_structures`, `hook_families`, `narrator_styles` and `visual_treatments`. Use exactly those values in `log.csv` so the R7 variation check can count them. |
## Executive Summary
The business is a content operating system rather than a collection of one-off automation scripts. It will use a shared pipeline for ideation, research, scripting, asset generation, voice, subtitles, editing, quality assurance, publishing, analytics, and experimentation. Niche-specific agents will specialize the research and writing logic without creating entirely separate applications.
The system is deliberately staged. V1 optimizes for speed to first output and learning. A V1.5 long-form pilot is introduced in Weeks 2–3 so the business can test the economics and audience value of 8–12 minute YouTube videos without waiting for the full V2 engineering stack. V2 introduces structured orchestration, reusable templates, automated research, batch processing, analytics ingestion, and semi-automatic publishing across both Shorts and long-form. V3 turns the system into a production-grade media company with multiple brands, durable workflows, automatic experiment allocation, asset provenance, cost controls, platform adapters, and a feedback loop that improves creative decisions from real performance data.
The central business thesis is not that AI can create large numbers of videos. That is already becoming commoditized. The moat is the combination of original content IP, a specialized production engine, high-quality brand templates, platform distribution, performance data, and a feedback system that learns which hooks, subjects, formats, durations, visuals, and narratives actually produce durable audience behavior.
## Non-Negotiable Principles
- Originality over volume: do not build the business around re-uploading anime, TV, movies, or other creators content with only subtitles, crops, borders, speed changes, or superficial edits.
- Human-in-the-loop first: every difficult decision can be reviewed manually in V1 and V2; automation is increased only after quality is demonstrated.
- Deterministic infrastructure, probabilistic creativity: code/orchestration controls state, retries, schemas, permissions, and publishing; models make creative/research judgments inside bounded interfaces.
- Every important output is structured data: idea, research packet, claims, script, scene plan, assets, render, platform variants, publication record, metrics, costs, and experiment metadata.
- Model routing by task: use the cheapest model that reliably solves the task, reserving premium reasoning for research synthesis, difficult fact checking, quality judgment, and exceptional creative work.
- Use APIs for scarce/expensive capabilities and local models for high-volume cheap capabilities whenever the economics justify it.
- Multi-platform from one canonical creative asset: render one master video and create platform-specific metadata/adaptations rather than maintaining four unrelated editing pipelines.
- Data-driven iteration: every batch is an experiment. The system must learn from watch time, retention, shares, comments, follows, and qualified monetizable views where available.
- Compliance is a feature: maintain asset provenance, source records, permissions, model license notes, and platform-policy checks as first-class data.
- Version everything: prompts, model aliases, templates, workflows, niche configurations, scoring rules, and platform adapters must be versioned.
## Current Strategic Position
The recommended initial audience is global English-speaking viewers, prioritizing markets with strong advertiser demand while keeping the creative broad enough to reach audiences outside one country. The first content portfolio should center on curiosity-driven entertainment and information rather than narrow local topics.
| Vertical | Role | Core format | Automation level target |
| --- | --- | --- | --- |
| Original AI cinematic stories | Mass-reach entertainment + owned IP | 30–60s Shorts + 8–12m core episodes | Very high |
| Mystery + science + what-if | Mass reach + credibility | 30–75s Shorts + 8–12m explainers | High |
| AI + technology + future | Commercial-value niche | 20–60s Shorts + 8–12m deep dives | High |
| Psychology / human behavior | Shareability + sponsorship potential | 20–50s Shorts + 8–12m explainers | High |
| History / dark history | Evergreen archive | 30–90s Shorts + 8–12m documentaries | High |
The first production implementation should use only one vertical: **Original AI cinematic stories**. The second vertical should be added after the V1 pipeline is stable. This avoids building five specialized agents before proving that one complete content loop works.
## Business Model
The long-term business can have several revenue layers, in this order of operational maturity: platform monetization; sponsorships; affiliate offers; owned digital products; licensing; and eventually software or managed content services built on the same internal tooling.
| Revenue layer | When to pursue | Main dependency | Risk |
| --- | --- | --- | --- |
| Platform monetization | After sustained original audience traction | Eligible accounts + qualified performance | Platform policy / RPM variability |
| Sponsorships | After a niche has measurable audience quality | Brand-safe niche + audience fit | Brand demand |
| Affiliate | After audience intent becomes clear | Trackable offers + trust | Low conversion if mismatched |
| Owned products | After repeated audience pain points emerge | Product-market fit | Development distraction |
| Licensing / IP | After original characters or formats have traction | Strong IP + rights management | Longer sales cycle |
| Content SaaS / agency | V3 only | Reliable internal production system | Higher support burden |
Business rule: never assume that high raw views automatically equal high revenue. Track views, qualified views where available, watch time, audience geography, sponsorship suitability, click behavior, and contribution margin separately.
## Platform Policy Position
The system is designed around original, transformed, or fully owned content. Meta states that Facebook is prioritizing original content and reducing the reach of unoriginal content; minor changes such as captions, borders, or speed changes to someone else’s content are not treated as sufficient creative value. Facebook Content Monetization also emphasizes qualified views, longer watch time, deeper engagement, and an earnings rate metric, and the program is invite-only as of the blueprint date.
For YouTube, design around meaningful original value and avoid mass-produced repetitive videos that differ only superficially. For TikTok and other platforms, use official publishing APIs where possible instead of browser automation.
Policy links are maintained in the Sources section and must be checked before each major production or platform integration change.
# Part I — System Goals, Scope, and Success Criteria
## V1 Definition of Done
> **Revision 1.2:** Item 6 (transcribing the narration) is replaced by forced alignment of the known script (R5), and item 9 (5–10 posts) by the R8 gates: 10 videos by day 14 and 30 Shorts plus 2 long-form pilots by day 30.

V1 is not an autonomous business. V1 is the smallest complete content factory that can reliably create a publishable vertical short from an idea.
1. Choose one niche and one English-language brand concept.
2. Generate or manually select a content idea.
3. Generate a structured script with hook, body, payoff, CTA, and estimated timing.
4. Generate visual assets for the required scenes using an image generator or a manual asset pack.
5. Generate narration using local or cloud TTS.
6. Generate subtitles from final audio using speech recognition.
7. Render a 9:16 MP4 with clean captions and audio.
8. Perform a manual quality check.
9. Export a final file and publish manually to 5–10 posts across one or more platforms.
10. Record the publication date, title, script version, model versions, and basic performance metrics in a simple log.
## V1 Success Criteria
> **Revision 1.2:** The "Manual publish batch" row is superseded by R8 (Gates A and B).

| Metric | Target | Why |
| --- | --- | --- |
| Time to first video | ≤ 3 days from project start | Protect speed to learning |
| Manual end-to-end success rate | ≥ 80% of attempts reach renderable output | Pipeline reliability |
| Video generation time | ≤ 30–60 minutes of active work/video initially | Feasible solo operation |
| Manual publish batch | 5–10 videos | Enough data to validate the workflow |
| Critical failures | 0 on final published videos | Brand protection |
| Reproducibility | Same JSON spec can re-render the same creative | Engineering discipline |
## V2 Definition of Done
1. Ideas are collected into a queue automatically.
2. Research packets are generated with source links and claims.
3. Scripts are produced using structured JSON schemas.
4. Reusable visual and editing templates are applied automatically.
5. Voice, transcription, subtitles, and rendering are batched.
6. You review only selected checkpoints rather than every technical step.
7. Analytics are ingested automatically.
8. Publishing is semi-automatic with platform adapters where approved APIs are available.
9. Costs are tracked per asset and per published video.
10. Prompt/model/template versions are stored for every generated artifact.
11. A shared long-form workflow can produce 8–12 minute episodes from the same content registry used by Shorts.
12. A long-form episode can automatically produce derivative Shorts without duplicating research or story-development work.
## V3 Definition of Done
1. Multiple niches share one production platform.
2. Multiple channels/accounts use configurable brand profiles.
3. Workflow orchestration survives retries and machine restarts.
4. Ideas are ranked by performance-aware scoring.
5. Low-risk content can flow from idea to publication with sampling-based human QA.
6. Premium model calls are used selectively based on value and confidence.
7. Experiment agents allocate more production capacity to high-performing formats while preserving exploration.
8. Copyright/licensing/provenance is auditable.
9. Platform adapters schedule and publish content through approved APIs.
10. Business dashboards show output, reach, retention, cost, and contribution margin.
## Out of Scope for V1
- Fully autonomous publishing.
- Five niches simultaneously.
- Training custom foundation models.
- Large local video-generation models on a 6 GB GPU.
- Browser automation for social platforms.
- Complex Kubernetes deployment.
- Fully automated long-form production. V1.5 long-form is intentionally semi-manual and template-driven.
- Custom mobile applications.
- Automated comment spam or engagement manipulation.
- Buying views, followers, likes, or other artificial engagement.
# Part II — Content Portfolio Strategy
## Niche Selection Framework
| Dimension | Weight | Question |
| --- | --- | --- |
| Mass appeal | 20% | Can a broad viewer understand the premise instantly? |
| Scroll-stop potential | 15% | Can the concept create a strong first 1–2 seconds? |
| Repeatability | 15% | Can 500+ distinct episodes be produced without obvious repetition? |
| Visual potential | 10% | Can the subject be shown compellingly? |
| Monetization | 15% | Can the audience support ads, sponsorships, affiliates, or products? |
| Originality | 10% | Can we own or meaningfully create the content? |
| Research cost | 5% | How expensive is reliable sourcing? |
| Production cost | 5% | How expensive are assets, voices, and rendering? |
| Policy risk | 5% | How easy is it to stay compliant? |
## Vertical A — Original AI Cinematic Stories
Primary objective: maximize entertainment reach while creating original intellectual property.
Recommended formats: psychological twist; mystery; emotional reveal; speculative what-if; short horror without graphic gore; sci-fi premise; relationship dilemma; time-travel consequence; future message; alternate reality.
| Property | Default |
| --- | --- |
| Language | English |
| Duration | 30–55s |
| Narration | Single narrator or 2 character voices |
| Visual style | Cinematic anime / stylized 3D / illustrated realism |
| Scenes | 6–12 |
| Hook | Question, contradiction, impossible event, or immediate stakes |
| CTA | Soft; only when appropriate |
### Content Formula
1. 0–2s: visual + verbal hook.
2. 2–8s: establish the unusual situation.
3. 8–20s: create a curiosity gap.
4. 20–35s: escalate stakes.
5. 35–48s: reveal or twist.
6. 48–55s: payoff or emotional aftershock.
### Example Story Seeds
- A boy receives a message every night from a version of himself living ten years in the future.
- Every person in a city forgets one person, and nobody can remember whom they forgot.
- A woman hears a doorbell at exactly 3:17 AM; opening the door changes tomorrow.
- An AI predicts one small accident correctly, then predicts something impossible.
- Every photograph of one family has a different person standing in the background.
## Vertical B — Mystery + Science + What-If
Primary objective: combine curiosity with credible information. Research discipline is mandatory.
| Format | Example |
| --- | --- |
| Real mystery | An unexplained event with documented evidence |
| Science what-if | What would happen if Earth stopped rotating for 10 seconds? |
| Space | What would happen to the oceans if the Moon disappeared? |
| Technology paradox | Why a seemingly simple engineering problem is difficult |
| Hidden history of science | A forgotten experiment or invention |
Rule: distinguish fact, plausible inference, uncertainty, and fiction. Never present an invented scenario as a real event.
## Vertical C — AI + Technology + Future
Primary objective: capture commercially valuable technology audiences and time-sensitive attention.
- AI model releases and capability changes.
- Robotics and hardware breakthroughs.
- AI applications that solve a concrete problem.
- Computer science concepts explained visually.
- Future-of-work concepts.
- Interesting engineering failures and design trade-offs.
Rule: prioritize primary sources for current technology. For company announcements, prefer official documentation, research papers, release notes, model cards, and first-party blog posts, then use reputable secondary reporting for context.
## Vertical D — Psychology / Human Behavior
Primary objective: maximize relatability and sharing.
This vertical has high misinformation risk. Every scientific claim should have a research packet and a conservative writing style. Avoid diagnosing people, claiming that a behavior proves a mental disorder, or using fabricated “psychology hacks.”
## Vertical E — History / Dark History
Primary objective: build an evergreen content library that can accumulate over time.
Research must distinguish primary historical records, academic sources, reputable secondary references, legends, folklore, and uncertain claims.
# Part III — Shared Technical Architecture
> **Revision 1.2:** This part is the long-term reference architecture. V1 is a folder of plain scripts (R1, R14); nothing here is built until its gate is passed (R2).

## Architecture Overview
```text

                     +-----------------------------+
                     |        Web Dashboard        |
                     |     Next.js / TypeScript    |
                     +--------------+--------------+
                                    |
                                    v
                     +-----------------------------+
                     |          FastAPI API         |
                     +--------------+--------------+
                                    |
                 +------------------+------------------+
                 |                                     |
                 v                                     v
       +-------------------+                   +-------------------+
       |   Task / Workflow |                   |  PostgreSQL       |
       | Temporal           |                   |  + pgvector       |
       +---------+---------+                   +-------------------+
                 |
                 v
       +--------------------------+
       | Agent / Model Gateway    |
       | OpenAI Agents SDK        |
       | LiteLLM                  |
       +------------+-------------+
                    |
          +---------+----------+
          |                    |
          v                    v
   +-------------+      +---------------+
   | Local Models|      | Cloud Models  |
   | Qwen / etc. |      | OpenAI / etc. |
   +-------------+      +---------------+
                    
                    v
       +--------------------------+
       | Media Generation         |
       | ComfyUI / Image APIs     |
       | Qwen3-TTS / TTS API      |
       | faster-whisper           |
       +------------+-------------+
                    |
                    v
       +--------------------------+
       | Render Engine            |
       | Remotion + FFmpeg        |
       +------------+-------------+
                    |
                    v
       +--------------------------+
       | Object Storage           |
       | Local / R2 / S3 / MinIO  |
       +------------+-------------+
                    |
                    v
       +--------------------------+
       | Platform Adapters        |
       | YouTube / Meta / TikTok  |
       +------------+-------------+
                    |
                    v
       +--------------------------+
       | Analytics + Experiments  |
       +--------------------------+
```
## Core Components
> **Revision 1.2:** The V1 column is superseded by R5 and R14: a free-tier cloud LLM (local Ollama as fallback), Kokoro narration, forced-alignment captions, `log.csv` instead of a database, and no API or dashboard.

| Component | V1 | V2 | V3 |
| --- | --- | --- | --- |
| Dashboard | Optional/simple | Next.js queue UI | Full operations console |
| API | Simple FastAPI endpoints | Typed API + auth | Production API + RBAC |
| Workflow | Python scripts | Temporal workflows | Temporal + multi-queue workers |
| Database | SQLite/Postgres | Postgres + pgvector | Managed Postgres + backups + replicas as needed |
| Model gateway | Direct SDK calls | LiteLLM | LiteLLM with routing, budgets, fallbacks |
| LLM | Local + GPT-5.6 Luna/Terra/Sol | Task routing | Portfolio routing + premium escalation |
| Image | API or ComfyUI | ComfyUI/API hybrid | GPU workers + provider fallback |
| Video | Image motion + FFmpeg | Remotion + selective video gen | Dedicated video workers |
| TTS | Qwen3-TTS / API | Batch TTS | Multi-voice service |
| STT | faster-whisper | Batch GPU/CPU | Worker pool |
| Publishing | Manual | Semi-auto | API-driven |
| Analytics | Spreadsheet/DB | API ingestion | Automated experiments |
## Repository Architecture
> **Revision 1.2:** This is the long-term target layout. V1 uses the flat layout in Part IV "V1 Folder Layout" (R14).

```text
framesmith/
├── apps/
│   ├── api/
│   ├── dashboard/
│   └── worker-admin/
├── agents/
│   ├── core/
│   ├── story/
│   ├── mystery/
│   ├── tech/
│   ├── psychology/
│   └── history/
├── workflows/
│   ├── content.py
│   ├── research.py
│   ├── render.py
│   ├── publish.py
│   └── analytics.py
├── media/
│   ├── image/
│   ├── video/
│   ├── tts/
│   ├── stt/
│   └── render/
├── publishers/
│   ├── youtube/
│   ├── facebook/
│   ├── instagram/
│   └── tiktok/
├── prompts/
│   ├── shared/
│   └── niches/
├── configs/
│   ├── niches/
│   ├── brands/
│   └── platforms/
├── db/
│   ├── migrations/
│   └── seeds/
├── infra/
│   ├── docker/
│   └── temporal/
├── tests/
└── docs/
```
## Environment Separation
- local: development on Windows with RTX 3060 6 GB
- dev: reproducible Docker services plus local GPU worker
- stage: publishing disabled or private/unlisted where supported
- prod: separate credentials, storage bucket, database, and platform tokens
- analytics: production metrics must never be written to development datasets
# Part IV — V1: Build in 2–3 Days
## V1 Philosophy
V1 intentionally avoids the most time-consuming parts: full agent orchestration, multi-platform APIs, autonomous scheduling, large local video models, complex analytics, and cloud deployment. The target is one reliable pipeline that turns a structured idea into a polished MP4.
## V1 Recommended Content
Use original AI cinematic stories because they require less research infrastructure than science, psychology, or current technology content. You can create the first videos using a simple story agent, a few high-quality images, local TTS, local speech recognition, and deterministic rendering.
## V1 Hardware Assumption
| Item | Assumption |
| --- | --- |
| Laptop | Lenovo Legion 5 |
| CPU | AMD Ryzen 7 5800H |
| GPU | RTX 3060 6 GB |
| RAM | 32 GB |
| OS | Windows initially; Linux/WSL2 optional later |
| CPU | Modern 6–8 core CPU is enough for V1 |
| Storage | Keep at least 50–100 GB free for models and media |
## V1 Model Choices

> **Revision 1.2:** This table is superseded by R5 (zero-cost stack). Use R5 for V1 decisions.
| Task | Primary | Fallback / Alternative | Local? |
| --- | --- | --- | --- |
| Idea generation | Qwen3.5-4B or GPT-5.6 Luna | GPT-5.6 Terra | Yes |
| Script polish | GPT-5.6 Luna | GPT-5.6 Terra/Sol | Cloud |
| Image generation | ComfyUI with a lightweight supported image model or API | OpenAI image API / another provider | Hybrid |
| TTS | Qwen3-TTS 0.6B/1.7B | Cloud TTS | Yes |
| Transcription | faster-whisper | Whisper API | Yes |
| Rendering | Remotion + FFmpeg | FFmpeg-only templates | Yes |
Qwen3.5-4B is Apache-2.0 on Hugging Face, but its full-precision repository is substantially larger than 6 GB. For the RTX 3060, use a quantized GGUF build via llama.cpp/Ollama or run the model on CPU/partial GPU depending on the build. The 4B model is selected because it is a practical local assistant rather than because it is the strongest model available.
Current official Qwen3.5 model pages: https://huggingface.co/Qwen/Qwen3.5-4B and https://huggingface.co/Qwen/Qwen3.5-9B
## V1 Local LLM Runtime
> **Revision 1.2:** R5 makes a free-tier cloud LLM the default and local Qwen via Ollama or llama.cpp the last-resort fallback. The setup below is still valid for that fallback.

Preferred V1 runtime: llama.cpp when you want explicit control and OpenAI-compatible endpoints; Ollama when you want the easiest Windows developer experience. Both can expose a local model to your application. llama.cpp provides an OpenAI-compatible server and supports schema-constrained JSON on its server endpoint.
```bash
# Example llama.cpp style
llama-server -hf ggml-org/Qwen3.5-0.8B-GGUF

# Example client base URL
http://127.0.0.1:8080/v1
```
For your first implementation, use Ollama if the primary goal is getting started quickly. Switch to llama.cpp if you need more control over quantization, batching, schema-constrained outputs, or GPU/CPU placement.
## V1 LLM Prompting Strategy
Do not give the local model long, free-form instructions for the whole application. Give it one bounded task and demand structured JSON.
```text
SYSTEM
You are the StoryIdeaAgent for an English short-form video brand.
Return JSON only.
Do not use copyrighted characters, franchises, or existing stories.
Prefer simple concepts that can be visually generated in 6-10 scenes.

USER
Generate 10 original short-form story ideas.
Audience: global English-speaking adults.
Emotion: curiosity + surprise.
Duration: 35-55 seconds.

Schema:
{
  "ideas": [
    {
      "title": "string",
      "one_sentence_premise": "string",
      "hook": "string",
      "twist": "string",
      "visual_potential": 1,
      "novelty": 1,
      "production_difficulty": 1,
      "policy_risk": 1
    }
  ]
}
```
## V1 Story Schema
```json
{
  "content_id": "short unique id",
  "niche": "ai_stories",
  "language": "en",
  "working_title": "...",
  "hook": "...",
  "script": [
    {
      "index": 1,
      "text": "...",
      "duration_seconds": 3.0,
      "emotion": "tense",
      "visual": "..."
    }
  ],
  "cta": "optional",
  "estimated_duration_seconds": 43
}
```
## V1 Image Generation Strategy
For V1, do not generate every frame of a scene. Generate 6–10 high-quality still images and create motion with pans, zooms, cuts, overlays, light effects, and sound design. This reduces cost and makes rendering deterministic.
Use consistent character references. A character sheet should define hair, face shape, clothing, color palette, age range, and distinguishing props. Every scene prompt should include a compact identity block rather than relying on the model to rediscover the character.
### V1 Visual Prompt Template
```text
SUBJECT:
Character: [identity block]
Action: [what the character is doing]

ENVIRONMENT:
[place, time of day, weather]

COMPOSITION:
[close-up / medium / wide]
[foreground / midground / background]

LIGHTING:
[cinematic / neon / moonlight / warm interior]

STYLE:
[brand style]

CONSTRAINTS:
No logos, no text, no copyrighted characters, no watermarks, no extra limbs, no malformed hands.
```
## V1 TTS

> **Revision 1.2:** Default to Kokoro-82M on CPU (R5); keep Qwen3-TTS 0.6B as an A/B candidate. The 1.7B model does not fit alongside other GPU work on 6 GB.
Use Qwen3-TTS as the default local narration engine. The project currently publishes 0.6B and 1.7B model variants and supports English, Japanese, and other major languages, plus voice design and cloning capabilities. For V1, use one stable narrator voice and do not overcomplicate multi-speaker dialogue.
Official repository: https://github.com/QwenLM/Qwen3-TTS
## V1 Speech-to-Text / Subtitles

> **Revision 1.2:** Prefer forced alignment of the known script over re-transcribing it (R5).
Use faster-whisper to transcribe the final narration and create timestamped captions. It is a CTranslate2 implementation designed for efficient Whisper inference and supports CPU/GPU execution plus quantization. The repository reports meaningful speed/memory improvements relative to the original Whisper implementation.
Official repository: https://github.com/SYSTRAN/faster-whisper
## V1 Subtitle Style
- Use one primary font family across a channel.
- Keep text inside a platform-safe region.
- Use short caption chunks rather than paragraph blocks.
- Prefer 1–7 words per caption chunk when the narration allows it.
- Highlight a small number of words only when it adds meaning.
- Keep contrast high and avoid covering faces.
- Validate that punctuation and line breaks do not create accidental meanings.
## V1 Remotion Renderer
Remotion is recommended for repeatable React/TypeScript-based video templates. Maintain two canonical compositions from the beginning: `ShortVertical` (1080x1920) and `LongHorizontal` (1920x1080). The two compositions should consume the same content/render specification model, but should not force the same scene layout. The current documentation provides command-line scaffolding, local development, and rendering workflows. Use it to define reusable components such as HookScene, CharacterScene, CaptionOverlay, ProgressBar, CTA, and Background.
Official docs: https://www.remotion.dev/docs
```bash
# Create a blank Remotion project
npx create-video@latest --yes --blank renderer
cd renderer
npm run dev
```
## V1 FFmpeg Layer
FFmpeg is the deterministic media-processing layer beneath the renderer. Use it for audio normalization, muxing, scaling, frame extraction, subtitle burning when needed, codec normalization, file inspection, and final packaging.
```bash
# Example final encode
ffmpeg -i input.mp4 -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k output.mp4
```
## V1 Minimal Render Specification
> **Revision 1.2:** Asset paths in a real spec are relative to `v1/` and the spec is saved as `v1/renders/{content_id}.spec.json` (R14). The example below keeps bare file names for readability; `scripts/build_render_spec.py` writes the full form and `schemas/examples/render_spec.example.json` shows it.

```json
{
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "duration_seconds": 45,
  "scenes": [
    {"asset":"scene-01.png","start":0,"duration":3.5,"motion":"push_in"},
    {"asset":"scene-02.png","start":3.5,"duration":5.0,"motion":"pan_left"}
  ],
  "voice":"voice-01.wav",
  "subtitles":"captions.ass",
  "music":"bgm-01.mp3",
  "sfx":[]
}
```
## V1 Manual Workflow
```text
1. Pick or generate 10 ideas.
2. Select 3.
3. Generate scripts.
4. Review scripts manually.
5. Generate 6-10 visuals per approved script.
6. Generate narration.
7. Run faster-whisper.
8. Render with Remotion.
9. Watch the final MP4.
10. Fix any obvious issue.
11. Export final master.
12. Create a platform caption/title manually.
13. Upload manually.
14. Record URL + publication date + initial metrics.
```
## V1 Folder Layout
> **Revision 1.2:** Replaced 2026-10-10 (R14). The repo needs homes for config, schemas, prompts, scripts, license records and saved ComfyUI workflows (R9 and R11 require them).

```text
framesmith/
├── AGENTS.md  CLAUDE.md  README.md  Roadmap.md  blueprint.md  log.csv
├── configs/brands/lanternfall.yaml
├── schemas/             JSON Schemas (idea, script, render spec) + examples
├── prompts/             versioned prompt files
├── scripts/             plain Python scripts (no package)
├── tests/
├── provenance/          policies.md + licenses.csv
├── comfyui/workflows/   saved workflow JSON
├── v1/{ideas,scripts,assets,audio,subtitles,renders,published}/
├── renderer/            Remotion project (created on Day 2)
├── notes/
└── docs/
```
## V1 Day 1 Checklist
> **Revision 1.2:** The Day 1, Day 2 and Day 3 checklists below are superseded by R11 (zero-cost stack, forced alignment, Kokoro, free-tier LLMs) and by `Roadmap.md`, which tracks progress.

1. Create repository and environment file.
2. Install Python, Node.js, FFmpeg.
3. Install Ollama or llama.cpp.
4. Install a small local Qwen3.5 model or quantized GGUF.
5. Create a script that generates structured JSON ideas.
6. Create a script that turns one selected idea into a timed script.
7. Install Qwen3-TTS and successfully generate a test sentence.
8. Install faster-whisper and transcribe the test audio.
## V1 Day 2 Checklist
1. Create 6–10 visual assets for one story.
2. Build one Remotion vertical template.
3. Implement caption rendering.
4. Combine voice + visuals + music.
5. Produce one complete MP4.
6. Watch it on a phone, not only on desktop.
7. Fix subtitle size, safe zones, pacing, and audio.
## V1 Day 3 Checklist
1. Produce 3–5 variants.
2. Publish the best 2–3.
3. Generate the next 5–10 using the same pipeline.
4. Record every output in the content log.
5. Create a one-page performance sheet.
6. Decide whether the niche and format deserve V2 investment.

# Part IV.5 — V1.5: Long-Form Pilot (Weeks 2–3)

## Objective
V1.5 tests whether the same content engine can produce one high-quality 8–12 minute YouTube episode per week without forcing the project into full automation. The pilot is designed to answer a business question, not an engineering question:

> **Does a strong long-form episode create enough watch time, subscribers, and monetization potential to justify the extra production effort?**

## Recommended Role of Long-Form

Long-form should be the **core episode** for the channel once the story concept has enough depth. Shorts should act as the discovery layer.

```text
             CORE STORY / RESEARCH
                     |
          +----------+----------+
          |                     |
          v                     v
     8–12 MIN EPISODE       3–8 SHORTS
          |                     |
          v                     v
      YouTube             YT / FB / IG / TikTok
          |                     |
          +----------+----------+
                     |
                     v
              Audience growth
```

## Episode Length

- Default target: **10–12 minutes** for the initial story format.
- Acceptable range: **8–12 minutes**.
- Minimum practical length: long enough to tell the complete story without filler.
- Do not repeat scenes, stretch pauses, or add generic narration just to reach 10 minutes.
- For factual explainers, use whatever length the subject needs; an excellent 8-minute explanation is better than a padded 12-minute video.

YouTube permits mid-roll ads on monetized videos that are 8 minutes or longer. This is a monetization capability, not a guarantee of ad delivery or higher RPM. 

## Long-Form Story Word Count

For normal English narration, use approximately 130–160 spoken words per minute as the initial planning range.

| Target | Approximate narration |
| --- | ---: |
| 8 min | 1,040–1,280 words |
| 10 min | 1,300–1,600 words |
| 12 min | 1,560–1,920 words |

For cinematic story episodes, start around **1,400–1,800 words** and adjust after measuring the actual TTS speaking rate.

## Long-Form Narrative Structure — Story

```text
0:00–0:20      Cold open / strongest unanswered question
0:20–0:50      Setup and stakes
0:50–2:00      Character + world establishment
2:00–4:00      First escalation
4:00–6:30      Complication / discovery
6:30–8:30      Major reversal
8:30–10:30     Resolution / consequence
10:30–12:00    Emotional payoff / final hook / next-episode bridge
```

Treat this as a starting template, not a fixed formula. The script critic should be able to modify the structure for different story types.

## Long-Form Narrative Structure — Explainer / Mystery

```text
0:00–0:30      Strong claim/question
0:30–1:30      Why this matters
1:30–3:00      Context
3:00–6:00      Main evidence / story
6:00–8:30      Complication / competing explanation
8:30–10:30     Best-supported conclusion
10:30–12:00    What remains unknown + next question
```

## Visual Density

Do not try to generate AI video for every second.

Recommended V1.5 visual strategy:

- 18–35 story beats for a 10–12 minute episode. Give each beat 3–5 shots (reframes, push-ins, crops, overlays, maps or diagrams) so the screen changes every 4–8 seconds. That is roughly 60–150 shots built from about 40–90 unique generated images. Treat these numbers as hypotheses and measure them in the pilot.
- Use still images with cinematic motion for most beats. A single static image held for 20–40 seconds is the slideshow pattern to avoid.
- Use image-to-video or generated motion only for hero moments.
- Reuse establishing environments when it improves continuity and does not make the episode feel repetitive.
- Change framing, camera movement, visual scale, lighting, overlays, maps, diagrams, or environmental details to maintain attention.
- Add original sound design at major narrative beats.

## Long-Form Compute and Pipeline Notes
- Generate stills at about 1344x768 and keep the subject in the center third so vertical derivative Shorts can be cropped without re-generating.
- Queue image generation overnight, checkpoint per scene, resume on failure, and keep one model loaded at a time on the 6 GB GPU.
- Script stage: outline, then section drafts, then polish, then human edit (opening 60 seconds first).
- Estimates to measure in the first pilot, not verified: 40–90 images at 20–40 seconds each is about 15–60 minutes; a 10-minute 1080p render about 15–40 minutes on the laptop.

## 16:9 Long-Form Master

The canonical long-form render is:

```json
{
  "content_type": "long_form",
  "width": 1920,
  "height": 1080,
  "fps": 30,
  "target_duration_seconds": 660,
  "scenes": [],
  "voice": "...",
  "music": "...",
  "sfx": [],
  "subtitles": "..."
}
```

Create the long-form video in 16:9 first. Do not upscale a vertical Reel into a fake long-form video.

## Long-Form Derivative Shorts

From each completed long-form episode, create **3–8 Shorts candidates**:

1. The cold open.
2. The most surprising reveal.
3. A standalone unanswered question.
4. A character dilemma.
5. A high-emotion moment.
6. A visual explanation.
7. A counterintuitive fact, if factual.
8. A teaser for the full episode.

Each derivative Short must stand on its own. Do not publish an unfinished clip whose only purpose is to force the viewer to leave the platform.

## Long-Form Thumbnail Agent

Create a dedicated thumbnail stage because long-form discovery depends heavily on packaging.

Input:
- final story premise
- strongest conflict
- 2–3 candidate frames
- channel brand

Output:
- three thumbnail concepts
- one primary title
- three alternative titles
- one sentence explaining the curiosity gap

Human selects the final package during V1.5.

## Long-Form Manual V1.5 Workflow

```text
1. Select one proven short-form topic / story universe.
2. Expand the concept into a 1,400–1,800 word long-form outline.
3. Manually review the outline.
4. Generate full script with act/section timestamps.
5. Human-edit the opening 60 seconds first.
6. Generate a 16:9 scene plan.
7. Generate about 40–90 still/hero visual assets (18–35 story beats, 3–5 shots each; measure in the pilot).
8. Generate narration.
9. Generate captions from final audio.
10. Assemble in Remotion.
11. Add music/SFX and chapter-like visual transitions where useful.
12. Generate 3–8 Short derivatives from the episode.
13. Human review the long-form final cut.
14. Upload long-form to YouTube manually.
15. Publish selected Shorts across platforms.
16. Track all metrics against one shared content_id.
```

## Long-Form Metrics

Primary:
- impressions
- click-through rate
- first 30-second retention
- average view duration
- average percentage viewed
- watch hours
- subscribers gained
- returning viewers
- likes/comments/shares
- revenue after monetization

Secondary:
- production hours
- visual-generation cost
- TTS cost
- render time
- thumbnail iterations
- number of manual corrections
- average shot length and unique images per episode
- number of derivative Shorts produced
- Shorts-to-long-form traffic where measurable

## Long-Form Pilot Decision Matrix

| Outcome | Decision |
| --- | --- |
| High CTR + strong retention + acceptable production effort | Scale to 1/week |
| High CTR + weak retention | Fix story opening/pacing before adding volume |
| Low CTR + strong retention | Fix thumbnail/title/packaging |
| Strong views but poor subscriber conversion | Improve channel positioning and series identity |
| Strong audience but high production cost | Simplify visuals and automate the slowest step |
| Weak audience + high production cost | Pause long-form and return to Shorts testing |

## Long-Form Business Rule

The long-form lane is **not automatically a replacement for Shorts**. A healthy portfolio at maturity is likely to be:

```text
Shorts = discovery / experiments / distribution
Long-form = depth / watch hours / stronger monetization potential / IP
```

The exact ratio must be learned from the channel's actual data.

# Part V — V2: Semi-Automatic Production System

> **Revision 1.2:** Do not start V2 until Gate C (about $500/month net for 2 months). Even then, build only the step that costs the most manual minutes; the full stack below is a reference, not a to-do list (R2, R6).
## V2 Objective
V2 removes repetitive manual tasks while intentionally keeping human approval at high-value checkpoints. You should feel that you are operating a small media studio rather than manually editing videos.
## V2 Service Stack
| Service | Recommendation | Reason |
| --- | --- | --- |
| API | FastAPI | Fits your Python background |
| Dashboard | Next.js + TypeScript | Fits your existing stack |
| DB | PostgreSQL | Structured content and metrics |
| Vector search | pgvector | Similarity and deduplication |
| Queue/cache | Redis | Fast job coordination |
| Workflow | Temporal | Durable multi-step execution |
| Model gateway | LiteLLM | Unified provider routing + spend controls |
| Agent layer | OpenAI Agents SDK or thin custom agent wrapper | Tool use, handoffs, structured outputs |
| Storage | Cloudflare R2 / S3 / MinIO | Video and image assets |
## Why Temporal in V2
Temporal is unnecessary for a three-script V1. It becomes valuable when a video pipeline can remain blocked for a long time, needs retries, waits for human approval, or spans several external APIs. Temporal provides durable workflow execution that preserves state through failures and restarts.
Official docs: https://docs.temporal.io/temporal
## V2 Workflow
```text
IdeaIntakeWorkflow
  -> ScoreIdeasActivity
  -> ResearchActivity
  -> FactCheckActivity
  -> ScriptActivity
  -> HumanApprovalGate
  -> AssetPlanActivity
  -> GenerateAssetsActivity
  -> TTSActivity
  -> SubtitleActivity
  -> RenderActivity
  -> QAActivity
  -> HumanPublishGate
  -> PublishActivity
  -> AnalyticsIngestActivity
```
## V2 Long-Form Workflow

```text
LongFormIdeaWorkflow
  -> SourceShortOrTopicActivity
  -> OutlineActivity
  -> ResearchActivity (when factual)
  -> ScriptActivity
  -> ScriptCriticActivity
  -> HumanApprovalGate
  -> LongFormScenePlanActivity
  -> VisualGenerationActivity
  -> TTSActivity
  -> SubtitleActivity
  -> ThumbnailActivity
  -> 16x9RenderActivity
  -> QAActivity
  -> PublishActivity
  -> DerivativeShortActivity
  -> ShortRenderActivity
  -> AnalyticsIngestActivity
```

### V2 Long-Form Reuse Principle

Long-form must reuse the same:
- content_id
- research packet
- brand config
- narrator profile
- character registry
- asset registry
- provenance records
- analytics schema
- model routing layer
- prompt/version registry

Do not build a separate long-form application.

### Shared Content Object Extension

```json
{
  "content_id": "story-2026-001",
  "content_type": "long_form",
  "parent_content_id": null,
  "source_story_id": "universe-001",
  "duration_seconds": 684,
  "aspect_ratio": "16:9",
  "derivatives": [
    {"content_id": "short-001", "type": "short"},
    {"content_id": "short-002", "type": "short"}
  ]
}
```

### V2 Weekly Editorial Cadence

Initial recommended operating target once the long-form pilot is validated:

- 1 long-form YouTube episode/week.
- 3–8 Shorts derived from the episode.
- Additional standalone Shorts only when they support discovery experiments.
- One weekly analytics review comparing long-form and Shorts economics.

This is a starting allocation, not a permanent ratio.

## V2 Agent Registry
| Agent | Inputs | Outputs | Model class |
| --- | --- | --- | --- |
| TrendScout | sources + date | candidate topics | Local fast |
| IdeaGenerator | trend + niche config | idea list | Local fast |
| IdeaJudge | idea list + historical metrics | ranked ideas | Luna/Terra |
| Researcher | approved idea | research packet | Terra/Sol + web |
| FactChecker | research packet | claim verdicts | Sol for difficult cases |
| ScriptWriter | research + brand | timed script JSON | Luna/Terra |
| ScriptCritic | script + rubric | score + revisions | Terra/Sol |
| VisualDirector | script + brand | scene prompts | Luna/Terra |
| MetadataWriter | script + platform | title/caption/hashtags | Local/Luna |
| QAJudge | render + metadata | pass/fail + reasons | Terra/Sol |
| AnalyticsAnalyst | metrics | insights | Terra/Sol |
## V2 Research Packet Schema
```json
{
  "topic": "...",
  "research_date": "2026-10-08",
  "sources": [
    {
      "url": "https://...",
      "title": "...",
      "publisher": "...",
      "published_at": "...",
      "source_type": "primary",
      "reliability": 0.95
    }
  ],
  "claims": [
    {
      "id": "claim-001",
      "text": "...",
      "supporting_sources": ["source-001"],
      "confidence": 0.96,
      "allowed_wording": "..."
    }
  ],
  "uncertainties": ["..."],
  "do_not_claim": ["..."]
}
```
## V2 Model Routing
Use a routing layer so the application chooses the model by task, not by developer habit. The current GPT-5.6 family includes Luna for cost-sensitive workloads, Terra for balanced intelligence/cost, and Sol for more complex professional work. Current official pricing and capabilities should be checked at implementation time; the blueprint records the architecture, not a permanent price guarantee.
| Task class | Default model | Escalate when |
| --- | --- | --- |
| Cheap classification | Qwen local | Confidence low |
| Bulk ideation | GPT-5.6 Luna or local Qwen | Creative diversity poor |
| Normal research synthesis | GPT-5.6 Terra | Conflicting evidence |
| Hard fact check | GPT-5.6 Sol | Material risk / legal / scientific ambiguity |
| Final script judge | GPT-5.6 Terra | Low score or high-risk claim |
| Analytics synthesis | GPT-5.6 Terra | Complex multi-channel causal analysis |
## V2 OpenAI Integration Notes
Use the Responses API for new OpenAI integrations where appropriate. GPT-5.6 Luna supports structured outputs, function calling, web search, file search, code interpreter, and MCP through the Responses API according to the current model documentation. GPT-5.6 Sol provides the higher-quality tier for difficult reasoning tasks.
Current references: https://developers.openai.com/api/docs/models/gpt-5.6-luna and https://developers.openai.com/api/docs/models/gpt-5.6-sol
## V2 Model Gateway — LiteLLM
Use LiteLLM to expose a normalized model interface, track spend, apply routing, and configure fallbacks. This is especially useful once you mix local models, OpenAI, and potentially other providers such as Gemini, Claude, DeepSeek, or open-model inference providers.
Official repository: https://github.com/BerriAI/litellm
```text
# conceptual configuration
content_fast -> local-qwen
content_balanced -> gpt-5.6-luna
content_reasoning -> gpt-5.6-terra
content_critical -> gpt-5.6-sol
```
## V2 Analytics Data Model
```text
content_metrics
----------------
id
content_id
platform
platform_video_id
observed_at
views
likes
comments
shares
saves
avg_watch_seconds
completion_rate
followers_gained
revenue
qualified_views
earnings_rate
source_snapshot
```
## V2 Content Scoring Model
Do not rank content purely by a predicted viral score. Combine creative potential with business and production economics.
```text
score =
  0.20 * mass_appeal +
  0.15 * scroll_stop +
  0.15 * retention_potential +
  0.10 * shareability +
  0.10 * originality +
  0.10 * visual_potential +
  0.10 * monetization_fit +
  0.05 * freshness +
  0.05 * production_efficiency
```
Each subscore should be 0–100. Store the rubric version so historical scores remain interpretable after the rubric changes.
## V2 Human Gates
| Gate | Automatic behavior | Human responsibility |
| --- | --- | --- |
| Idea gate | Agent ranks 20 ideas | Approve 5–10 |
| Research gate | Research packet + confidence | Inspect high-risk claims |
| Script gate | Auto score + optional rewrite | Approve scripts below threshold |
| Visual gate | Generate + QA | Spot-check characters and artifacts |
| Publish gate | Prepare metadata + upload draft | Final publication decision |
## V2 Cost Controls
- Cache research packets by URL and topic.
- Cache embeddings for unchanged text.
- Use local models for repetitive classification.
- Batch low-value generation.
- Use premium reasoning only for escalation cases.
- Reuse background music, reusable motion templates, and non-character assets where licensing allows.
- Limit regeneration loops to a fixed maximum.
- Log token counts, API calls, image generations, video seconds, TTS duration, storage bytes, and render time.
# Part VI — V3: Fully Automated Production Business

> **Revision 1.2:** Do not start V3 until Gate D (about $2,000–3,000/month net for 3 months) (R2, R8).
## V3 Objective
V3 is not simply “remove the human.” It is a controlled autonomous production system with sampling-based human supervision. The automation engine should decide what to make, how to make it, when to publish it, and when to stop or regenerate, while humans remain responsible for brand, legal, financial, and strategic oversight.
## V3 Production Topology
```text

                     CONTROL PLANE
       +-----------------------------------------+
       | Dashboard | Rules | Budgets | Policies |
       +--------------------+--------------------+
                            |
                            v
                 +--------------------+
                 | Workflow Scheduler |
                 | Temporal            |
                 +---------+----------+
                           |
       +----------------+--+----------------+
       |                |                   |
       v                v                   v
  Research Pool    Creative Pool       Analytics Pool
       |                |                   |
       +----------------+-------------------+
                        |
                        v
                 Media Worker Pool
          +-------------+-------------+
          |             |             |
       Image GPU     Video GPU     CPU Render
          |             |             |
          +-------------+-------------+
                        |
                        v
                 Publish Adapters
                        |
             +----------+----------+
             |          |          |
          YouTube    Meta       TikTok
                        |
                        v
                  Metrics Stream
                        |
                        v
                 Experiment Agent
```
## V3 Multiple Brands
Each channel becomes configuration, not a new codebase.
```yaml
brands/
  lanternfall.yaml        # first brand: original AI cinematic stories
  story-dark.yaml
  story-wholesome.yaml
  mystery-science.yaml
  ai-future.yaml
  psychology.yaml
```
## Brand Configuration
```yaml
brand_id: lanternfall
name: Lanternfall
language: en
formats:
  - short
  - long_form
audience: global_english
visual_style: cinematic_anime
narration: deep_neutral
max_duration_seconds:
  short: 55
  long_form: 720
cta_policy: soft
forbidden_topics:
  - graphic violence
  - sexual content
  - copyrighted franchise characters
caption_style: kinetic_white
watermark: none
```
The canonical, fuller file is `configs/brands/lanternfall.yaml` (R14).
## V3 Automated Experimentation
Use an explore/exploit allocation. Production should not become a machine that copies the last viral format forever.
```text
Daily content allocation example:

70% proven formats
20% controlled variations
10% new experiments

If a format shows sustained decline:
- reduce allocation
- test new hook families
- test new scene structures
- test new topic clusters

If a format beats the account baseline by a large margin:
- increase allocation gradually
- create adjacent concepts
- do not duplicate the same script
```
## V3 Causal Discipline
Do not claim that one creative change caused higher views unless the experiment design supports the claim. Correlated changes such as hook, topic, thumbnail, narration, and posting time can move together. Record experiment IDs and the exact variants so later analysis can be credible.
## V3 Portfolio Management
| Portfolio state | Meaning | Action |
| --- | --- | --- |
| Explore | Unknown format | Small test batch |
| Promising | Above baseline | Expand cautiously |
| Winner | Consistent superior performance | Increase allocation |
| Mature | Stable but declining | Refresh |
| Dead | Persistent poor performance | Retire |
| Risk | Policy / copyright / factual issue | Block and review |
# Part VII — Agent Specifications
## Common Agent Contract
Every agent should have a strict input/output contract. Agents do not directly write arbitrary files, mutate production state, or publish content unless the agent is specifically designed for that capability.
```text
AgentContract
- name
- version
- input_schema
- output_schema
- allowed_tools
- model_policy
- timeout_seconds
- retry_policy
- max_cost
- safety_policy
- observability_fields
```
## Trend Scout Agent
Purpose: identify topics with fresh attention potential.
- Inputs: date, niche, target audience, previous winning topics.
- Tools: search, RSS/news APIs, social trend sources where legally and technically permitted.
- Output: ranked topics with evidence and freshness score.
- Guardrail: never use a trend signal as proof of factual truth.
## Idea Generator Agent
Purpose: create multiple original concepts from a topic or content pillar.
```json
Input:
{
  "niche": "ai_stories",
  "seed_topic": "future messages",
  "avoid_similar_to": ["..."]
}

Output:
{
  "ideas": [...]
}
```
## Researcher Agent
Purpose: collect evidence and context. This is the main research agent for Mystery, Science, Tech, Psychology, and History.
- Prefer first-party and primary sources.
- Capture source publication date.
- Capture exact supporting passages or structured evidence where permitted.
- Flag conflicting sources.
- Never fabricate sources.
## Fact Checker Agent
Purpose: evaluate each factual claim against the research packet. A claim with missing support should be rewritten, softened, or removed.
```text
Verdict values:
SUPPORT
PARTIAL
UNSUPPORTED
CONTRADICTED
UNCERTAIN
```
## Script Writer Agent
Purpose: transform research or a fictional premise into a high-retention short-form script while preserving truth boundaries or story originality.
## Script Critic Agent
Purpose: simulate a strict editor. It should score hook clarity, pacing, clarity, novelty, emotional payoff, language naturalness, and policy risk.
## Visual Director Agent
Purpose: convert script paragraphs into scene specifications suitable for image/video generation. It owns composition instructions, recurring characters, continuity, and visual style.
## Asset Agent
Purpose: generate or retrieve approved assets. It must attach source/licensing metadata to every non-original asset.
## Narration Agent
Purpose: convert script to spoken audio, selecting voice and delivery parameters based on brand configuration.
## Subtitle Agent
Purpose: turn final audio into accurate captions and ensure caption timing does not exceed safe reading density.
## Render Agent
Purpose: execute a deterministic render specification. It is primarily code, not an autonomous LLM. A small model may review errors, but rendering itself is deterministic.
## QA Agent
Purpose: evaluate the assembled artifact against a rule set. It should produce reasons, not only a score.
## Metadata Agent
Purpose: generate titles, captions, keywords, descriptions, hashtags, and platform-specific metadata. It must not promise outcomes or make unsupported claims.
## Publisher Agent
Purpose: use official APIs or a human handoff to publish. It must be permission-scoped, idempotent, and auditable.
## Analytics Agent
Purpose: normalize platform metrics into a common schema and produce actionable insights.
## Experiment Agent
Purpose: propose the next creative tests based on past performance. It should not blindly maximize the highest-view topic; it should maintain portfolio diversity and explore uncertainty.
# Part VIII — Media Generation Stack
## Image Generation Strategy
Use a two-tier model. Tier 1 is the default bulk generator, optimized for cost and speed. Tier 2 is the hero generator used only for thumbnails, hero scenes, and high-value concepts.
ComfyUI is the recommended control layer because it exposes node-based workflows and a local API, supports many current open visual models, and can run locally. The project currently lists support for multiple image/video families including Flux, Qwen Image, Wan 2.2, LTX-2, HunyuanVideo, and others.
Official: https://github.com/Comfy-Org/ComfyUI
## Open Image / Video Models to Track
| Family | Use | V1 | V2/V3 |
| --- | --- | --- | --- |
| Qwen Image family | Image generation/editing | Optional API | ComfyUI/local |
| Flux family | High-quality images | API if convenient | ComfyUI/local |
| Wan 2.x | Video generation | No | Selective local/cloud |
| LTX-2 | Audio+video generation | No | Selective video generation |
| HunyuanVideo | Video generation | No | Track for future GPU upgrades |
| Stable Diffusion family | Broad ecosystem | Possible | Useful fallback |
## LTX-2 Position
LTX-2 is a strong V2/V3 candidate for local audio+video workflows. The official repository describes synchronized audio/video generation, keyframes, LoRA support, and ComfyUI integration. It should not be treated as a V1 requirement on the RTX 3060.
Official: https://github.com/Lightricks/LTX-Video
## Wan Position
Wan 2.2 is a strong open-model family to monitor for V2/V3 video generation. Use it selectively because local requirements and generation cost can be materially higher than still-image pipelines, especially for a 6 GB GPU.
Official model family references should be checked on the Wan-AI organization on Hugging Face before deployment.
## ComfyUI Integration Pattern
```text
Python Orchestrator
        |
        | HTTP / local API
        v
   ComfyUI workflow
        |
        v
    output assets
        |
        v
  content asset registry
```
Save every successful ComfyUI workflow JSON with model names, versions, seeds, LoRAs, and input references. This makes a visual output reproducible and allows later migration to stronger hardware.
## Video Generation Economics Strategy
- Do not generate every second as AI video in V1.
- Use still images + deterministic motion for the majority of videos.
- Use image-to-video only where motion adds substantial value.
- Create premium hero clips for high-scoring ideas.
- Cache generated assets for reuse where licensing/model terms permit.
- Log generated seconds and provider/model for every clip.
## Voice Strategy
> **Revision 1.2:** The default narration engine is Kokoro-82M on CPU (R5); Qwen3-TTS 0.6B is an A/B candidate. A paid cloud voice is a V2 spend item (R6), not a V1 default.

Default voice stack: Qwen3-TTS for cheap local narration, plus one cloud TTS provider as a quality fallback. Maintain voice IDs and pronunciation dictionaries by brand.
```yaml
voice_profile:
  id: narrator_en_01
  locale: en-US
  style: calm_cinematic
  rate: 0.97
  pitch: 0
  pronunciation:
    AI: "A-I"
    GPU: "G-P-U"
```
## Music and SFX
Use only assets with explicit commercial-use rights appropriate to your intended platforms. Maintain a small licensed or self-generated library. Avoid relying on “found” audio from random uploads unless you have clear rights.
# Part IX — Rendering and Editing Framework
## Renderer Architecture
```text
Content JSON
    |
    +--> Scene parser
    |
    +--> Asset resolver
    |
    +--> Audio resolver
    |
    +--> Subtitle resolver
    |
    +--> Motion calculator
    |
    +--> Remotion composition
    |
    +--> FFmpeg post-process
    |
    +--> final MP4
```
## Reusable Scene Types
- HookScene
- CharacterCloseup
- CharacterTwoShot
- EnvironmentReveal
- FastFactCard
- QuoteCard
- WhatIfTimeline
- MysteryEvidenceBoard
- ChatMessageScene
- FinalReveal
- CTA
## Motion Presets
| Preset | Use case |
| --- | --- |
| push_in | emotional close-up |
| push_out | reveal context |
| pan_left | wide scene |
| pan_right | wide scene |
| parallax | layered still images |
| micro_shake | shock or impact |
| focus_pull | reveal a hidden object |
| cut_on_word | emphasis |
## Subtitle Presets
| Preset | Use case |
| --- | --- |
| kinetic_white | general storytelling |
| keyword_highlight | science / facts |
| minimal_lower | documentary style |
| dialogue_bubble | character stories |
## Audio Chain
```text
Narration
  -> loudness normalization
  -> gentle compression
  -> EQ / cleanup if required
  -> duck background music
  -> add SFX
  -> final loudness check
```
## Video QA Technical Checks
- Container is valid MP4.
- Codec is H.264 or another platform-supported format.
- Audio stream exists and is synchronized.
- Frame rate is stable.
- Resolution is 1080x1920 for the canonical vertical master unless a platform-specific requirement dictates otherwise.
- No black first/last frame.
- No missing media placeholders.
- No subtitle overflow beyond safe region.
- No silent sections caused by TTS failure.
- No accidental debug text.
# Part X — Data Model and Storage
## Entities
| Entity | Purpose |
| --- | --- |
| Brand | Channel identity and creative rules |
| Niche | Content specialization |
| Idea | Candidate content concept |
| ResearchRun | Evidence collection session |
| Source | External source metadata |
| Claim | Atomic factual statement |
| Script | Versioned script |
| Scene | Scene specification |
| Asset | Image/audio/video file |
| Render | Rendered output |
| Publication | Platform-specific published post |
| MetricSnapshot | Point-in-time metrics |
| Experiment | Controlled creative test |
| CostEvent | Model/media/infrastructure spend |
| PolicyCheck | Platform/copyright/safety result |
## PostgreSQL Core Schema
```sql
brands(
  id uuid primary key,
  name text,
  config jsonb,
  created_at timestamptz
)

niches(
  id uuid primary key,
  brand_id uuid references brands(id),
  slug text,
  config jsonb
)

ideas(
  id uuid primary key,
  niche_id uuid references niches(id),
  title text,
  premise text,
  score jsonb,
  status text,
  embedding vector,
  created_at timestamptz
)

scripts(
  id uuid primary key,
  idea_id uuid references ideas(id),
  version int,
  body jsonb,
  model_id text,
  prompt_version text,
  created_at timestamptz
)

assets(
  id uuid primary key,
  content_id uuid,
  type text,
  uri text,
  checksum text,
  provenance jsonb,
  created_at timestamptz
)
```
## Provenance Schema
```json
{
  "asset_type": "image",
  "generator": "comfyui",
  "model": "...",
  "model_version": "...",
  "prompt_hash": "...",
  "workflow_hash": "...",
  "seed": 12345,
  "source_asset_ids": [],
  "commercial_use": true,
  "license_notes": "...",
  "generated_at": "2026-10-08T..."
}
```
## Object Storage Convention
```text
s3://framesmith/
  brands/{brand_id}/
    content/{content_id}/
      research/
      script/
      assets/
      audio/
      subtitles/
      renders/
      platform/
      metrics/
```
## Deduplication
Use a combination of exact hashes, perceptual hashes, embeddings, and semantic similarity. A new script should not be considered “original” merely because the wording is slightly different. Compare premise, sequence of events, characters, and key narrative beats.
# Part XI — Prompt System
## Prompt Repository Rules
- Every prompt gets a version ID.
- Do not store production prompts only in code strings.
- Keep system instructions separate from niche configuration.
- Use structured output schemas whenever possible.
- Write explicit rejection conditions.
- Include examples for the desired format.
- Add regression tests for critical prompts.
## Prompt Version Format
```text
story_writer_v1
story_writer_v2
story_writer_v3
```
## Researcher System Prompt Skeleton
```text
You are a research agent for a short-form media company.

Objectives:
- find reliable evidence
- separate facts from inference
- preserve uncertainty
- return sources and claims

Rules:
- do not invent sources
- do not silently resolve conflicting evidence
- prefer primary sources
- record publication dates
- flag outdated information

Output JSON only matching the provided schema.
```
## Script Writer Skeleton
```text
You are a short-form video writer.
Audience: global English-speaking viewers.
Goal: high retention without deception.

The first 2 seconds must contain a concrete curiosity trigger.
Every sentence must either advance the story or increase curiosity.
Avoid filler.
Avoid generic motivational language.
Do not exaggerate factual claims beyond the evidence packet.

Return timed segments as JSON.
```
## QA Judge Skeleton
```text
Evaluate the final creative against these dimensions:
1. Hook
2. Clarity
3. Pacing
4. Originality
5. Visual continuity
6. Audio clarity
7. Subtitle readability
8. Factual correctness if applicable
9. Platform safety
10. Brand consistency

Return:
- score 0-100
- pass/fail
- blocking_reasons[]
- recommended_fixes[]
```
# Part XII — Platform Strategy
## YouTube Shorts
Use YouTube as a core distribution channel, not as an afterthought. The official Data API provides `videos.insert` for uploads and metadata. New/unverified API projects can have uploads restricted to private viewing until the project passes audit, so API setup should begin before full automation is expected.
Official: https://developers.google.com/youtube/v3/docs/videos/insert
### YouTube Adapter Responsibilities
- Authenticate via OAuth.
- Validate channel/account configuration.
- Prepare title/description/tags as appropriate.
- Upload MP4.
- Store returned video ID.
- Store publish state.
- Fetch analytics through the appropriate reporting/API mechanisms where available.
- Handle retries idempotently.
## Facebook Reels
Facebook should be one of the main destinations because original Reels are a core part of Meta’s current creator monetization and recommendation strategy. Content Monetization is invite-only as of the blueprint date; do not build the financial model assuming immediate monetization.
Meta creator guidance: https://about.fb.com/news/2026/03/creator-fast-track-grow-your-audience-earn-money-on-facebook/
Originality guidance: https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/
### Facebook Adapter
```text
publish_facebook_reel(
  page_id,
  video_uri,
  caption,
  scheduled_time=None
)
 -> platform_video_id
```
## Instagram Reels
Use an Instagram Professional account and Meta’s official content publishing capabilities. Do not design around browser-driven login automation.
## TikTok
Use the official Content Posting API. Current TikTok developer documentation describes direct posting and upload flows, including verified-domain URL or local upload pathways, and OAuth scopes such as `video.publish` or `video.upload` depending on the flow. Current restrictions and audit requirements must be rechecked before production.
Official: https://developers.tiktok.com/docs/en/content-posting-api-get-started
Upload flow: https://developers.tiktok.com/docs/en/content-posting-api-get-started-upload-content
## Cross-Platform Adaptation
| Element | Master | Platform-specific |
| --- | --- | --- |
| Video | 1080x1920 master | Potential crop/trim only if required |
| Audio | Clean master | No unnecessary re-encoding |
| Captions | Canonical subtitle file | Optional style variation |
| Title | Canonical idea/title | Platform rewrite |
| Caption | Base description | Platform-specific CTA |
| Hashtags | Topic set | Platform-specific subset |
| Thumbnail/cover | Hero frame | Platform-specific cover if supported |
# Part XIII — Analytics and Growth System
## Metrics Hierarchy
Use a funnel instead of one number.
```text
Reach
  -> view start
  -> 3-second hold
  -> 25%
  -> 50%
  -> 75%
  -> completion
  -> replay
  -> like/comment/share/save
  -> follow
  -> return viewer
  -> monetization
```
## Core Creative Metrics
| Metric | Use |
| --- | --- |
| Hook hold | Measures first-second effectiveness |
| Average watch duration | Measures attention |
| Completion rate | Measures full-story delivery |
| Rewatch rate | Measures replay value |
| Share rate | Measures social value |
| Follow conversion | Measures account relevance |
| Save rate | Measures reference value |
## Business Metrics
| Metric | Definition |
| --- | --- |
| Cost per published video | Total production cost / published videos |
| Cost per 1,000 views | Total allocated cost / views * 1000 |
| Revenue per 1,000 qualified views | Platform-provided where available |
| Contribution margin | Revenue - variable content costs |
| Revenue per production hour | Business revenue / human production hours |
| Followers per 1,000 views | Audience conversion |
## Analytics Data Retention
- Keep raw snapshots for auditability.
- Keep daily/weekly aggregates for dashboard speed.
- Never overwrite the raw metric capture.
- Store the timestamp and timezone of each snapshot.
- Store platform API version if available.
## Winning Pattern Detection
The analytics agent should compare content against a baseline within the same account, not against unrelated channels. A video with 20,000 views on a new account might be a major success even if another channel has 2 million-view videos.
## Experiment Matrix
| Variable | Example levels |
| --- | --- |
| Hook | question / contradiction / surprise / direct promise |
| Length | 25 / 35 / 45 / 55 seconds |
| Narrator | male / female / neutral / character |
| Visual | anime / cinematic / illustrated / photoreal stylized |
| Pacing | fast / medium / dramatic |
| Twist timing | 20% / 50% / 75% |
| CTA | none / follow / comment question |
# Part XIV — Cost Engineering
## Cost Buckets
- LLM inference
- Web/search usage
- Image generation
- Video generation
- TTS
- STT / subtitle processing
- Rendering compute
- Storage
- Bandwidth
- Database / orchestration
- Human time
- Platform/API operational overhead
## Current OpenAI Model Cost Reference
As checked on 2026-10-08, official OpenAI documentation lists GPT-5.6 Luna at $0.20 per 1M input tokens and $1.20 per 1M output tokens; GPT-5.6 Terra at $2.00 input and $12.00 output; GPT-5.6 Sol at $4.00 input and $20.00 output. These prices can change and should be rechecked before budgeting.
Official pricing/model references: https://developers.openai.com/api/docs/models/gpt-5.6-luna, https://developers.openai.com/api/docs/models/gpt-5.6-terra, https://developers.openai.com/api/docs/models/gpt-5.6-sol
## Cost Allocation Rule
The expensive part of the system should be visual generation, not routine text generation. Therefore, build the system so many candidate concepts are filtered before image/video generation is invoked.
```text
100 ideas
  -> 30 scored
  -> 10 researched / scripted
  -> 6 approved
  -> 6 visualized
  -> 5 rendered
  -> 5 published
```
## V1 Budget Philosophy
A reasonable V1 budget can be close to zero for software licensing if local/open-source tools are used, with spend concentrated on a small number of cloud image/LLM generations. Do not commit to monthly infrastructure contracts before the first 10–30 videos reveal what the actual cost drivers are.
## V2 Unit Economics
Track cost per video before trying to optimize revenue. A good early target is not a specific dollar number; it is a measurable downward curve in cost per publishable video without a corresponding decline in quality or retention.
## V3 Contribution Margin
```text
Contribution Margin
= Platform + sponsorship + affiliate + product revenue
  - LLM costs
  - image/video generation
  - TTS
  - infrastructure
  - storage/bandwidth
  - paid contractors directly tied to production
```
# Part XV — Quality, Safety, Copyright, and Brand Controls
## Originality Policy
- Create original stories, characters, scripts, narration, and visuals whenever possible.
- Do not use recognizable copyrighted characters as the core attraction unless you have appropriate rights.
- Do not scrape other creators’ videos and apply cosmetic edits.
- Do not use “translation” as a substitute for creative transformation.
- Keep a provenance record for every externally sourced asset.
## Factual Content Policy
- Every material factual statement must map to one or more sources.
- Use language such as “may”, “researchers suggest”, or “evidence is mixed” where appropriate.
- Distinguish established fact from hypothesis and scenario.
- Never invent direct quotations.
- Never invent source citations.
- Use dates explicitly for current events.
## Synthetic Media Policy
Maintain a record of generation models and inputs. If a platform asks for disclosure of altered or synthetic media, support the platform’s disclosure workflow. The exact disclosure requirements can change, so treat each platform’s current documentation as authoritative.
## Brand Safety
| Risk | Default action |
| --- | --- |
| Graphic violence | Reject or reduce |
| Sexual content | Reject |
| Hate / protected groups | Reject |
| Defamation | Reject or require verified reporting |
| Medical claims | Strict evidence gate |
| Financial advice | Strict evidence + disclaimer policy |
| Political persuasion | Separate high-risk vertical; do not launch initially |
| Copyright ambiguity | Hold for human review |
## QA Blockers
- Missing audio.
- Broken subtitles.
- Unintended visual artifacts that materially damage quality.
- Unverified factual claim in a factual channel.
- Copyright/provenance uncertainty.
- Generated logo or brand misuse.
- Dangerous or policy-sensitive content.
- Duplicate/recycled script detected.
# Part XVI — Operations and Human Workflow
## Daily V1 Routine
1. Generate 10–20 ideas.
2. Select 3–5.
3. Generate scripts.
4. Approve the strongest scripts.
5. Generate visuals and voice.
6. Render.
7. Watch final videos on phone.
8. Publish 1–3 per day initially.
9. Record metrics.
## Daily V2 Routine
1. Review morning dashboard.
2. Approve idea queue.
3. Review only high-risk research items.
4. Approve batch of scripts.
5. Let workers render.
6. Spot-check videos.
7. Publish/schedule approved batch.
8. Review previous-day metrics.
9. Create one experiment plan for the next batch.
## Weekly V3 Routine
1. Review brand-level performance.
2. Review niche-level performance.
3. Review cost per published video.
4. Review top and bottom 20 assets.
5. Retire weak formats.
6. Promote high-performing formats.
7. Review policy/copyright exceptions.
8. Review infrastructure failures.
9. Review monetization pipeline.
10. Update roadmap based on evidence.
## Human Tasks That Should Remain Longest
- Brand positioning.
- Portfolio selection.
- High-risk topic approval.
- Copyright disputes.
- Major monetization decisions.
- Partnership and sponsorship decisions.
- Final strategy for a new niche.
# Part XVII — Monitoring, Logging, and Observability
## Every Workflow Run Must Log
- workflow_id
- content_id
- agent_name
- agent_version
- model_id
- prompt_version
- start_time
- end_time
- latency
- input_tokens if applicable
- output_tokens if applicable
- provider_cost if available
- retry_count
- final_status
- error_type
## Failure Taxonomy
| Code | Meaning |
| --- | --- |
| E_MODEL_TIMEOUT | Model call timeout |
| E_MODEL_OUTPUT | Invalid structured output |
| E_ASSET | Asset generation failure |
| E_RENDER | Render failure |
| E_QA | QA rejection |
| E_PUBLISH_AUTH | Platform credential error |
| E_PUBLISH_RATE | Platform rate limit |
| E_PUBLISH_POLICY | Platform rejected content |
| E_SOURCE | Research source unavailable |
| E_INTERNAL | Internal software error |
## Alerting
- Immediate alert for repeated publishing failures.
- Alert if cost per video exceeds threshold.
- Alert if QA rejection rate spikes.
- Alert if one provider fails repeatedly.
- Alert if storage capacity falls below threshold.
# Part XVIII — Security and Credentials
## Credential Storage
- Use environment variables for local development.
- Use a secret manager in production.
- Never commit API keys.
- Use separate keys for dev/stage/prod.
- Use the minimum OAuth scopes required.
- Revoke unused tokens.
## Publishing Security
Publishing is a privileged operation. The publisher must require a valid content ID, approved QA status, approved brand, correct platform account, and a non-expired credential. It should be impossible for an arbitrary LLM response to trigger publication directly.
## Idempotency
Every publish operation requires an idempotency key such as `content_id + platform + target_account + scheduled_time`. If the worker retries, it must not publish duplicates.
# Part XIX — Infrastructure Roadmap
## V1 Infrastructure
> **Revision 1.2:** The model runtime is a free-tier cloud LLM with Ollama as the last resort, and storage is local folders plus `log.csv` (R5, R14). The table below predates that.

| Component | Choice |
| --- | --- |
| Machine | Local Windows laptop |
| Model runtime | Ollama or llama.cpp |
| Storage | Local folders |
| DB | SQLite or local PostgreSQL |
| Renderer | Remotion + FFmpeg |
| Orchestration | Python scripts |
| Publishing | Manual |
## V2 Infrastructure
| Component | Choice |
| --- | --- |
| Compute | Local GPU + small cloud VM |
| DB | PostgreSQL |
| Object storage | R2/S3/MinIO |
| Queue | Redis |
| Workflow | Temporal |
| LLM gateway | LiteLLM |
| Dashboard | Next.js |
| Publishing | Approved API adapters + manual gate |
## V3 Infrastructure
| Component | Choice |
| --- | --- |
| Compute | Dedicated workers + optional GPU cloud |
| DB | Managed PostgreSQL |
| Storage | Object storage with lifecycle rules |
| Workflow | Temporal cluster/cloud |
| LLM gateway | LiteLLM or equivalent model gateway |
| Observability | Structured logs + metrics + traces |
| Deployment | Docker; Kubernetes only when justified |
| Publishing | Platform API adapters |
# Part XX — Recommended Software and Model Inventory
| Tool / Model | Category | Role | Stage | License / access note |
| --- | --- | --- | --- | --- |
| Python | Runtime | Agents, APIs, workers | V1+ | Open source |
| FastAPI | Web/API | Backend service | V2+ | Open source |
| Next.js | Frontend | Ops dashboard | V2+ | Open source |
| PostgreSQL | Database | State and analytics | V2+ | Open source |
| pgvector | Vector DB extension | Similarity search | V2+ | Open source |
| Redis | Cache/queue | Fast transient state | V2+ | Open source |
| Temporal | Workflow engine | Durable orchestration | V2+ | Open source/self-host or cloud |
| OpenAI Agents SDK | Agent framework | Tool-using agents | V2+ | Open source SDK; API usage billed |
| LiteLLM | Model gateway | Routing/cost tracking | V2+ | Open source |
| Gemini AI Studio / Groq / OpenRouter free tiers | Cloud LLM APIs | Default V1 ideas and scripts (R5) | V1+ | Free tiers; limits and model names change, check each console |
| Ollama | Local LLM runtime | Easy local models | V1+ | Open source runtime |
| llama.cpp | Local LLM runtime | Controlled local inference | V1+ | MIT |
| Qwen3.5-4B | Local LLM | Cheap bulk reasoning | V1+ | Apache-2.0 model page |
| Kokoro-82M | TTS | Default V1 narration on CPU (R5) | V1+ | Apache-2.0; verify the model card before commercial use |
| Qwen3-TTS | TTS | Local English/Japanese voice; A/B candidate | V1+ | Open model repository; verify model-specific license before commercial use |
| faster-whisper | STT | Local subtitles/transcription | V1+ | Open source |
| ComfyUI | Media workflow | Image/video generation orchestration | V1/V2+ | GPL-3.0; model licenses vary |
| Remotion | Video renderer | React-based deterministic video | V1+ | Check current license/pricing for commercial use |
| FFmpeg | Media engine | Encoding/audio/subtitles | V1+ | LGPL/GPL depending on build/configuration |
| LTX-2 | Video model | Open video generation candidate | V2/V3 | Check model-specific license |
| Wan 2.x | Video model family | Open video generation candidate | V2/V3 | Check model-specific license |
## Model License Policy
Never assume that “open source” means “commercially unrestricted.” Check the exact model card, license, model-specific use restrictions, derivative rules, and provider terms before using a model in monetized production. Store the license reference in the asset/model registry (`provenance/licenses.csv` in V1).
# Part XXI — Platform and API Rollout
## Phase 1 — Manual Publishing
- No API integration required.
- Export final MP4 and metadata package.
- Upload manually.
- Copy platform URL/ID into the content record.
- Capture metrics manually once per day or per week.
## Phase 2 — Private/Test API Workflows
- Create developer apps.
- Implement OAuth.
- Test with non-public/private or draft flows where supported.
- Implement idempotency.
- Log platform responses.
- Handle rate limits.
- Get audited/approved where the platform requires it.
## Phase 3 — Public Scheduling
- Publish low-risk content automatically.
- Route high-risk content to human review.
- Use platform-specific scheduling where supported.
- Capture publication results automatically.
# Part XXII — Testing Strategy
## Unit Tests
- JSON schema validation.
- Prompt parser output.
- Asset resolver.
- Subtitle timing conversion.
- Video duration calculation.
- File naming.
- Platform payload builders.
- Idempotency key generation.
## Integration Tests
- LLM → JSON schema.
- TTS → audio file.
- STT → captions.
- Assets → renderer.
- Renderer → MP4.
- Publisher → test account/draft.
- Analytics → DB.
## Golden Content Tests
Keep 5–10 reference stories with expected structural properties. When prompts or models change, render them again and compare output quality. This catches regressions that code tests cannot.
## Prompt Regression Test
```text
For each prompt version:
- run 10 fixed inputs
- validate schema
- check banned phrases
- check output length
- check factual claim handling
- compare rubric score to baseline
```
# Part XXIII — Research and Source Policy
## Source Hierarchy
| Tier | Examples | Use |
| --- | --- | --- |
| Tier 1 | Official docs, regulators, primary papers, first-party announcements | Core claims |
| Tier 2 | Established journalism, academic summaries, reputable institutions | Context |
| Tier 3 | Specialist blogs, forums, community discussion | Lead generation / hypotheses |
| Tier 4 | Unverified social posts | Trend signal only |
## Current Events Rule
For current events, store exact publication dates and retrieve current evidence at generation time. Do not rely on the model’s static knowledge for a “today/latest/current” claim.
## Research Freshness
| Content type | Suggested freshness window |
| --- | --- |
| News / AI releases | Hours to days |
| Platform policy | Always check current official docs |
| Science overview | Months to years unless fast-moving |
| History | Long-lived; still verify sources |
| Evergreen psychology | Prefer current review literature where possible |
# Part XXIV — Content Quality Framework
## Creative Scorecard
| Dimension | 0–100 question |
| --- | --- |
| Hook | Would a viewer stop within 1–2 seconds? |
| Curiosity | Is there an unresolved question? |
| Pacing | Does every sentence move the piece? |
| Clarity | Can the viewer follow without rewinding? |
| Payoff | Does the ending satisfy or surprise? |
| Originality | Does the concept feel distinct? |
| Visual quality | Are visuals meaningful and coherent? |
| Audio | Is narration clean and natural? |
| Captions | Are captions readable and accurate? |
| Shareability | Would a viewer send it to someone? |
## Minimum Publish Thresholds
| Content type | Minimum score |
| --- | --- |
| Original story | 80 |
| Science / mystery | 85 |
| Technology / current | 88 |
| Psychology | 88 |
| High-risk claim content | 92 + human approval |
# Part XXV — Business Scaling Plan
## Stage A — Proof of Content
> **Revision 1.2:** Use the R8 gates instead of the 5–10 video target below: 10 videos by day 14, then 30 Shorts plus 2 long-form pilots by day 30.

Goal: prove that strangers watch the content.
- 1 niche
- 1 brand
- 5–10 videos
- Manual publishing
- No expensive infrastructure
## Stage B — Proof of Repeatability
Goal: prove that the process can produce a repeatable result.
- 30–100 videos
- 2–3 formats
- Analytics dashboard
- Semi-automated creation
- Clear cost per video
## Stage C — Proof of Audience-Market Fit
Goal: prove that one niche can sustain recurring audience growth.
- 100–500 videos
- Consistent viewer retention
- Follower growth
- Clear audience profile
- One or more monetization paths
## Stage D — Portfolio Scaling
Goal: add niches and channels without multiplying engineering complexity.
- 2–5 niches
- Shared production engine
- Brand configurations
- Model routing
- Automated analytics
## Stage E — Media Company
Goal: treat content generation as a managed operating system.
- Multiple channels
- Multi-platform distribution
- Sponsorship pipeline
- Affiliate system
- Original IP library
- Potential SaaS/agency product
# Part XXVI — Failure Modes to Avoid
| Failure | Why it happens | Prevention |
| --- | --- | --- |
| 500 low-quality videos/day | Volume mistaken for strategy | Quality threshold + analytics |
| Copyright dependence | Reuploads are easy | Original content policy |
| Too many agents | Architecture before product validation | Build one pipeline first |
| Too many APIs | Every task outsourced | Local/cloud routing |
| One giant prompt | Hard to debug | Specialized agents |
| No structured data | Workflow state lives in files/chat | Postgres schemas |
| No metrics | Optimizing by intuition | Analytics ingestion |
| No cost tracking | Revenue appears good until bills arrive | Cost events |
| No provenance | Cannot explain asset origin | Asset registry |
| Browser automation | Platform breaks or account risk | Official APIs |
| Model lock-in | One provider becomes a dependency | Model gateway |
| Premature Kubernetes | Operational overhead | Docker + simple workers |
# Part XXVII — Recommended V1 Implementation Commands
## Core Tools
```bash
# Python
python --version

# Node
node --version
npm --version

# FFmpeg
ffmpeg -version

# Git
git --version
```
## Ollama Option
```powershell
# Windows PowerShell
irm https://ollama.com/install.ps1 | iex

# Then pull a small model available in the library
ollama run qwen3
```
The exact model tag available in the Ollama registry should be checked at installation time. Keep the runtime abstracted behind an OpenAI-compatible or provider adapter interface.
## llama.cpp Option
```bash
# Example current llama.cpp usage pattern
llama-server -hf ggml-org/Qwen3.5-0.8B-GGUF
```
Official llama.cpp: https://github.com/ggml-org/llama.cpp
## Remotion V1
```bash
npx create-video@latest --yes --blank renderer
cd renderer
npm install
npm run dev
```
# Part XXVIII — V1 Minimal Python Interfaces
## Idea Generator Interface
```python
from dataclasses import dataclass
from typing import List


@dataclass
class Idea:
    title: str
    premise: str
    hook: str
    twist: str
    score: float


def generate_ideas(niche: str, count: int = 10) -> List[Idea]: ...
```
## TTS Interface
```python
def synthesize_speech(
    text: str,
    voice_id: str,
    output_path: str,
) -> str: ...
```
## Renderer Interface
```python
def render_video(
    render_spec_path: str,
    output_path: str,
) -> str: ...
```
## Content Pipeline Interface
```python
def create_video(idea_id: str) -> str:
    script = write_script(idea_id)
    assets = generate_assets(script)
    audio = generate_voice(script)
    subtitles = transcribe(audio)
    render_spec = build_render_spec(script, assets, audio, subtitles)
    return render_video(render_spec)
```
# Part XXIX — V2 Configuration Examples
## Niche Config
```yaml
niche_id: ai_stories
brand_id: lanternfall
language: en
audience: global_english
content_type: fiction
research_required: false
default_duration_seconds: 45
visual_engine: comfyui
tts_engine: kokoro
caption_timing: forced_alignment
renderer: remotion
qa_threshold: 80
```
## Research Niche Config
```yaml
niche_id: mystery_science
content_type: factual_story
research_required: true
minimum_sources: 3
primary_source_preference: true
fact_check_required: true
qa_threshold: 85
human_review_on_uncertain_claim: true
```
# Part XXX — V3 Advanced Improvements
## Character Consistency
- Build a character registry.
- Keep identity embeddings/reference images where the chosen model supports them.
- Use fixed wardrobe palettes per story arc.
- Store scene-to-character relationships.
- Run a visual continuity checker.
## Longitudinal Story Universes
Once a story brand has traction, create recurring characters and a lore database. This increases returning-viewer potential and creates owned IP that is more defensible than isolated generic videos.
## Localization Engine
After English is proven, reuse the underlying story/content graph for Spanish, Portuguese, Japanese, Hindi, and other markets. Localization should re-script and re-voice rather than simply machine-translating the English captions word-for-word.
## Voice Casting Engine
Assign voices by role: narrator, antagonist, child, scientist, observer. Maintain a voice library with usage rules. Avoid cloning voices without permission.
## Thumbnail / Cover Optimization
For platforms where covers materially affect discovery, generate 2–4 cover candidates and select based on a consistent brand rubric. Do not use deceptive images that are unrelated to the actual video.
## Semantic Content Graph
Represent relationships between topics, stories, characters, claims, sources, and audience performance. This lets the system find adjacent topics instead of repeating the same keyword.
```text
Topic
  -> subtopics
  -> previous videos
  -> audience metrics
  -> sources
  -> related ideas
  -> future experiments
```
# Part XXXI — Monetization Readiness
## Facebook
Monitor eligibility for Content Monetization in Professional Dashboard. Facebook states that Content Monetization is invite-only and that it is emphasizing qualified views, longer watch time, deeper engagement, and original content. Do not assume the account will monetize immediately.
## YouTube
Build the channel toward sustainable original audience and watch behavior rather than chasing threshold hacks. Monitor current YPP requirements directly from YouTube before making monetization forecasts.
## Sponsorship Readiness
- Know audience geography.
- Know average views and median views, not just top viral hits.
- Know niche and demographic fit.
- Keep examples of brand-safe content.
- Keep a rate card only after consistent performance exists.
## Affiliate Readiness
- Only promote products relevant to the audience.
- Use trackable links.
- Disclose affiliate relationships where required.
- Never invent testimonials.
# Part XXXII — Business Dashboard KPIs
| Dashboard | KPIs |
| --- | --- |
| Production | videos created, published, rejected, retry rate |
| Audience | views, retention, completion, shares, follows |
| Business | revenue, cost, contribution margin |
| Niche | median views, top formats, top topics |
| Platform | views by platform, follower growth, monetization metrics |
| Operations | worker uptime, queue length, failure rate |
| Model | cost, latency, quality score, fallback rate |
| Creative | hook families, lengths, visual styles, voice styles |
# Part XXXIII — Roadmap by Week

> **Revision 1.2:** Weeks 3–4 'V2 Foundation' is gated by Revision 1.2 (R2, R8). Until Gate B passes, weeks 2 onward are spent publishing, running the V1.5 long-form pilots (R12) and measuring, not building infrastructure. `Roadmap.md` is the working checklist.
## Week 1 — V1
1. Day 1: setup + local model + structured idea/script generation.
2. Day 2: TTS + transcription + render template.
3. Day 3: 3–5 videos + manual publishing.
4. Days 4–7: reach 10 videos and begin measuring performance.
## Week 2 — Stabilization
> **Revision 1.2:** The content registry, provenance metadata and cost logging below are already covered by `log.csv` and `provenance/licenses.csv` (R14); do not build a registry service in week 2. Week 2 is the first long-form pilot (R12).

1. Add content registry.
2. Add provenance metadata.
3. Add cost logging.
4. Improve visual consistency.
5. Create two additional templates.
6. Produce 20–30 total videos.
## Weeks 3–4 — V2 Foundation
1. PostgreSQL.
2. FastAPI.
3. Next.js queue UI.
4. LiteLLM.
5. Basic Temporal workflow.
6. Automatic analytics capture where practical.
7. Add second niche only after the first pipeline is stable.
## Month 2
1. Add research agents.
2. Add QA agents.
3. Add semi-automatic publishing.
4. Create experiment dashboard.
5. Add second and third content verticals.
## Month 3+
1. Increase output volume only when quality remains stable.
2. Introduce controlled local video generation experiments.
3. Expand channels.
4. Build sponsorship/affiliate pipeline.
5. Prepare V3 worker architecture.
# Part XXXIV — Definition of a Successful First Month
| Outcome | Target |
| --- | --- |
| Published original videos | 30–100 |
| Working automated render pipeline | Yes |
| Manual publishing process documented | Yes |
| At least one repeatable format identified | Yes |
| Cost per published video known | Yes |
| Top 10 videos analyzed | Yes |
| At least one weak format retired | Yes |
| V2 backlog created from real evidence | Yes |
# Part XXXV — Decision Rules
1. If a workflow step can be deterministic, implement it as code instead of an LLM.
2. If a model is used more than a few times per video, evaluate whether a local model can replace it.
3. If an output is hard to validate, add a schema before improving the prompt.
4. If a niche requires too much research for its return, reduce its production allocation.
5. If a platform changes an API, isolate the change to the platform adapter.
6. If one model provider becomes unreliable, route through the model gateway and use a fallback.
7. If a format gets high views but poor follows or retention, do not assume it is a business winner.
8. If production cost rises faster than audience growth, stop scaling volume.
9. If content repeatedly requires manual correction, improve the upstream template or agent instead of treating the symptom manually forever.
10. If a policy rule is unclear, pause the content and review it before publication.
# Part XXXVI — Source of Truth File Conventions
## Files That Must Exist Eventually
```text
blueprint.md                  # this document
README.md                     # concise project entry point
LICENSE                       # PolyForm Noncommercial 1.0.0 for project code only
AGENTS.md  CLAUDE.md          # instructions for coding agents
Roadmap.md                    # checkbox progress tracker
.env.example                  # required variables
log.csv                       # tracking log (columns in R14)
configs/niches/*.yaml        # niche configuration
configs/brands/*.yaml        # brand configuration
prompts/**/*.md              # versioned prompts
schemas/*.json               # structured outputs
workflows/*.py               # orchestration (V2+)
renderer/                     # Remotion project (R13); created on Day 2
provenance/policies.md        # asset rights rules
provenance/licenses.csv       # license record per model, voice, font and track
analytics/metrics.md          # metric definitions
```
## Change Log
```markdown
## 2026-10-08
- Created master blueprint.
- Established V1/V2/V3 staging.
- Selected original AI stories as V1 niche.
- Established multi-niche shared-engine architecture.
- Established model routing and platform adapter strategy.

## 2026-10-08 (Revision 1.1)
- Added revenue-first, budget-gated plan (R1–R10): V1 at $0, V2 at about $500/month net, V3 at about $2,000–3,000/month net.
- Replaced V1 model choices with a zero-cost stack (Kokoro, forced alignment, free-tier LLM APIs).
- Added verified monetization rules (YPP 2027 thresholds, Bangladesh availability, platform eligibility) and inauthentic-content creative rules.
- Changed the V1 validation batch from 5–10 to 30 videos with explicit gates.
- Fixed command typos (irm, llama-server) and cost-bucket typos.
- Added R11: Days 1–3 build checklist.

## 2026-10-08 (Revision 1.2, merged reviewer update)
- Adopted the reviewer's V1.5 long-form pilot: R12, Part IV.5 (structures, word counts, thumbnail agent, derivative Shorts, metrics, decision matrix), V2 long-form workflow, `ShortVertical`/`LongHorizontal` compositions, and updated Part II, Executive Summary and roadmap text.
- Corrected the YPP watch-hour bar: 8,000 hours for new applicants from 2027-02-01 (4,000 before), with the views-needed math and RPM planning range.
- Added long-form risks (inauthentic-content enforcement, cadence cap, retention) and restored the retention-first V2 spend order.
- Reconciled visual density (story beats versus shots versus unique images) and Gate B (30 Shorts plus 2 long-form pilots).
- Added R13: public brand Lanternfall, codename and repo Framesmith, handle rule and availability checklist; renamed repo, bucket, env prefix and Remotion project; added `lanternfall` as the first brand config.

## 2026-10-10 (Revision 1.3, repo scaffold)
- Created the framesmith repo: AGENTS.md, CLAUDE.md, Roadmap.md, README, .env.example, brand config, JSON Schemas, prompt files, provenance records, log.csv, tests, and the scripts check_env, validate, generate, build_render_spec and review.
- Added R14 (repo and tooling conventions): content IDs, strict schemas, LLM retry and fallback rules, render-spec paths, full log.csv columns, kill switches, brand lists.
- Fixed: render folder name in Part XXXVI (`renderer`), brand config durations and caption preset in Part VI, long-form image count in the V1.5 workflow (about 40–90 images, not 18–35), R5 tracking columns, `tts_engine` in Part XXIX, the V1 Folder Layout, and the Conclusion's V1 stack.
- Added "Revision 1.2" banners to V1 text that R5, R8 and R11 supersede: Part I, Part III, Part IV (local LLM runtime, minimal render spec, checklists), Part VIII voice strategy, Part XIX, Part XXV stage A, Part XXXIII week 2, Part XXXVIII, Appendix A and I; corrected the Appendix F rows for narration and captions. Added Kokoro and the free-tier LLM APIs to the Part XX inventory.

## 2026-10-10 (V1 audit corrections)
- Gate A means every published video has a recorded active time of at most 60 minutes; missing times or any video over 60 minutes fail the gate.
- Short render specs must contain 6–10 scenes at 30 fps, with scenes contiguous and covering the full duration. Invalid render specs fail validation.
- R7 variation reporting counts only values in the Lanternfall brand lists and reports when the configured lists cannot meet the required variety.
- Updated the V1 hardware record to the owner's Ryzen 7 5800H, 32 GB RAM and RTX 3060 6 GB laptop.
- Selected Gemini `gemini-3.8-flash` and OpenRouter `qwen/qwen3.8-27b:free` as the free-first provider chain, with OpenAI `gpt-6-luna` as a third fallback limited to the already available $5 credit. Removed Groq from active V1 configuration; no additional credit or paid service is authorized.
- Live smoke tests: OpenAI `gpt-6-luna` passed one JSON request. Gemini returned HTTP 402 because its project has depleted prepay credits; Google advises not retrying until billing is fixed. OpenRouter returned HTTP 404 that the pinned Qwen free endpoint was unavailable, so replaced it with `nvidia/nemotron-3-ultra-550b-a55b:free`, which returned HTTP 200 on a one-request check. OpenRouter's selected model does not support `response_format`; rely on the existing strict JSON/schema validation and retry path.
- Put the working, verified free OpenRouter endpoint first while Gemini's prepay billing is depleted; restore Gemini to first position only after its project has free API access again.

## 2026-10-10 (Gemini disabled; OpenCode Zen API evaluated)
- Disabled Gemini in the active provider order after its live request returned HTTP 402 for depleted prepay credit. OpenRouter remains first; OpenAI remains the last fallback using only the existing credit.
- Reviewed OpenRouter's live free-model catalog and OpenCode Zen's official model/API documentation. OpenCode lists `nemotron-3-ultra-free` at a zero model price, but a live request from Framesmith returned HTTP 403 `FreeTierError`: free inference is limited to the OpenCode app. Do not add it as a Framesmith provider or spend money to bypass this restriction. Keep its model ID as an OpenCode-app option only.

## 2026-10-10 (V1 providers simplified)
- Removed Gemini and Ollama from the supported provider implementation, environment check and tests. Framesmith V1 supports only OpenRouter then OpenAI; OpenCode Zen's free endpoint remains app-only and is not configured or used.
- Removed Gemini and OpenCode credentials/model settings from the local `.env` and kept `.env.example` limited to the two supported providers.

## 2026-10-10 (Revision 1.4, review-gated workbench direction)
- Added R15: develop the local-first Framesmith workbench in phases now, without waiting on audience/revenue gates; keep Lanternfall publishing, business spend, and quality approvals governed by R1–R14.
- Set the intended workflow to sequential generation with explicit owner checkpoints for ideas, scripts, images, paid motion generation, and final cut. Do not run GPU-heavy models concurrently.
- Recorded the owner's FramePack experience (slow and stressful on the 6 GB laptop GPU); local video generation is not the default. Image-to-video APIs remain opt-in, budget-capped and subject to live price review and explicit approval.
- Clarified that pan/zoom over stills is not a substitute for full-motion video when the quality bar calls for animation; a reel that misses that bar stays a draft.
- Permitted the Framesmith name on software-repository pages, while keeping Lanternfall branding in audience-facing video content. Specified PolyForm Noncommercial 1.0.0 for project code only; generated media and dependencies retain separate rights.
- Audit correction: the current source still includes the Ollama fallback between OpenRouter and OpenAI; the earlier provider-removal note is historical and does not describe the current implementation.
```
# Part XXXVII — Current Tool References
## Official References
- Gemini 3.8 Flash: https://ai.google.dev/gemini-api/docs/models
- Gemini API pricing and free-tier details: https://ai.google.dev/gemini-api/docs/pricing
- OpenRouter Qwen 3.8 27B free model: https://openrouter.ai/qwen/qwen3.8-27b:free
- OpenRouter Nemotron 3 Ultra free model: https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b%3Afree
- OpenAI GPT-6 Luna: https://developers.openai.com/api/docs/models/gpt-6-luna
- OpenAI API pricing: https://developers.openai.com/api/docs/pricing
- OpenAI GPT-5.6 Luna (historical reference): https://developers.openai.com/api/docs/models/gpt-5.6-luna
- OpenAI GPT-5.6 Terra: https://developers.openai.com/api/docs/models/gpt-5.6-terra
- OpenAI GPT-5.6 Sol: https://developers.openai.com/api/docs/models/gpt-5.6-sol
- OpenAI model list: https://developers.openai.com/api/docs/models/all
- OpenAI deprecations: https://developers.openai.com/api/docs/deprecations
- Qwen3.5-4B: https://huggingface.co/Qwen/Qwen3.5-4B
- Qwen3.5-9B: https://huggingface.co/Qwen/Qwen3.5-9B
- Qwen3-TTS: https://github.com/QwenLM/Qwen3-TTS
- Faster-Whisper: https://github.com/SYSTRAN/faster-whisper
- ComfyUI: https://github.com/Comfy-Org/ComfyUI
- Ollama: https://github.com/ollama/ollama

## 2026-10-10 (Ollama restored as the local second fallback)
- Owner clarified that Ollama should remain alongside OpenRouter and OpenAI. Prior removal reflected the literal earlier instruction to keep only OpenRouter and OpenAI; Ollama was not found broken.
- Current V1 order: OpenRouter free endpoint → local Ollama `qwen3.5:4b-q4_K_M` → OpenAI `gpt-6-luna` using only existing $5 credit. Gemini and OpenCode remain excluded. Ollama uses `FRAMESMITH_OLLAMA_URL` and requires no key.
- Laptop has Ryzen 7 5800H, 32 GB RAM, RTX 3060 Laptop GPU with 6 GB VRAM. Use the ~3.3 GB Q4_K_M model and 8K context. Keep only one GPU-heavy model active; stop/unload ComfyUI image models before Ollama inference.
- Model registry and API references checked 2026-10-10: https://registry.ollama.com/library/qwen3.5:4b-q4_K_M ; https://docs.ollama.com/api/chat ; Windows installer: https://ollama.com/download/windows . The model registry lists Apache 2.0 licensing.
- Installed Ollama 0.40.2 and pulled `qwen3.5:4b-q4_K_M`; a local JSON API smoke test passed and `ollama ps` reported 100% GPU at 8K context on the RTX 3060.
- Repository moved from `E:\PROJECT\framesmith` to `G:\framesmith`, including Git history, `.env`, and local project files. Ollama model cache moved to `G:\framesmith\.ollama\models`; `OLLAMA_MODELS` is set at Windows user scope and `.ollama/` is Git-ignored. The G: checkout, provider call, API, and GPU placement were verified before deleting the E: duplicate and C: model cache.
- llama.cpp: https://github.com/ggml-org/llama.cpp
- LiteLLM: https://github.com/BerriAI/litellm
- Temporal: https://docs.temporal.io/temporal
- Remotion: https://www.remotion.dev/docs
- LTX-Video / LTX-2: https://github.com/Lightricks/LTX-Video
- YouTube Data API upload: https://developers.google.com/youtube/v3/docs/videos/insert
- TikTok Content Posting API: https://developers.tiktok.com/docs/en/content-posting-api-get-started
- TikTok Upload flow: https://developers.tiktok.com/docs/en/content-posting-api-get-started-upload-content
- Facebook creator monetization update: https://about.fb.com/news/2026/03/creator-fast-track-grow-your-audience-earn-money-on-facebook/
- Facebook originality update: https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/
## Model/Tool Verification Rule
The URLs above are the baseline references checked for this blueprint on 2026-10-08. Before implementing a later-stage component, re-check the current vendor documentation for model availability, licensing, pricing, API scopes, upload requirements, and platform policies. Do not treat a 2026 reference as permanently stable.
# Part XXXVIII — Final Implementation Order

> **Revision 1.2:** Steps 14–22 are gated by R2 and R8. Do not start step 14 before Gate C. Steps 5, 6 and 13 are superseded by R5 (Kokoro narration, forced-alignment captions) and R8 (10 videos by day 14, 30 Shorts plus 2 long-form pilots by day 30).
1. Freeze the V1 scope.
2. Build the idea JSON generator.
3. Build the timed script generator.
4. Build one visual generation workflow.
5. Build Qwen3-TTS narration.
6. Build faster-whisper captions.
7. Build one Remotion template.
8. Add FFmpeg validation.
9. Generate the first three videos.
10. Publish manually.
11. Record metrics.
12. Fix obvious quality problems.
13. Produce 5–10 videos.
14. Only then start V2 infrastructure.
15. Add PostgreSQL + FastAPI + content registry.
16. Add LiteLLM routing.
17. Add Temporal workflow for the content pipeline.
18. Add research agents for the second niche.
19. Add analytics ingestion.
20. Add semi-automatic publishing.
21. Add experiment allocation.
22. Expand to multiple brands and platforms only after repeatability is demonstrated.
# Appendix A — V1 Minimal Checklist
> **Revision 1.2:** Superseded by R11 and `Roadmap.md` (Kokoro instead of Qwen3-TTS, forced alignment instead of transcription, free-tier LLMs instead of a local Qwen runtime, 30 videos instead of 10).

[ ] Git repository created
[ ] .env.example created
[ ] Python environment created
[ ] Node.js available
[ ] FFmpeg installed
[ ] Local Qwen runtime working
[ ] One structured JSON idea call working
[ ] One structured JSON script call working
[ ] Qwen3-TTS working
[ ] faster-whisper working
[ ] One ComfyUI or image API workflow working
[ ] Remotion project created
[ ] Subtitle style implemented
[ ] First complete MP4 rendered
[ ] Phone review completed
[ ] First video manually uploaded
[ ] Content ID and URL stored
[ ] Metrics sheet/database created
[ ] Second video generated
[ ] Five-video batch completed
[ ] Ten-video batch completed
# Appendix B — V2 Minimal Checklist
[ ] PostgreSQL running
[ ] Content schema migrated
[ ] FastAPI service running
[ ] Next.js dashboard running
[ ] LiteLLM gateway running
[ ] Local + cloud model routes configured
[ ] Prompt versions stored
[ ] Asset provenance stored
[ ] Research packet schema implemented
[ ] QA rubric implemented
[ ] Temporal local service running
[ ] Content workflow implemented
[ ] Analytics snapshot ingestion implemented
[ ] Human approval gate implemented
[ ] One platform API tested
# Appendix C — V3 Minimal Checklist
[ ] Multi-niche configuration
[ ] Multi-brand configuration
[ ] Object storage lifecycle rules
[ ] Production secrets management
[ ] Worker pool
[ ] Durable workflows
[ ] Platform adapters
[ ] Automatic QA sampling
[ ] Experiment agent
[ ] Cost budgets
[ ] Business dashboard
[ ] Revenue tracking
[ ] Sponsorship pipeline
[ ] Copyright/provenance audit trail
[ ] Automated rollback / disable switch
[ ] Disaster recovery procedure
# Appendix D — Emergency Kill Switch
The system must have a global kill switch that stops all publishing and asset generation workflows without deleting state. The kill switch should be accessible from the dashboard and via a CLI or environment variable.
```text
FRAMESMITH_PUBLISHING_ENABLED=false
FRAMESMITH_GENERATION_ENABLED=false
```
Use this when a platform policy changes, a model produces unsafe content, a credential is compromised, or a production bug causes duplicate publishing.
# Appendix E — Core North-Star Metrics
1. Original videos published per week.
2. Median views per video by niche.
3. Median completion rate.
4. Shares per 1,000 views.
5. Followers per 1,000 views.
6. Cost per published video.
7. Contribution margin per 1,000 qualified views where available.
8. Human minutes per published video.
9. Percentage of pipeline completed without human intervention.
10. Percentage of content rejected by QA.
11. Percentage of assets with complete provenance.
# Conclusion
The software goal is a local-first, review-gated workbench that carries a story from idea selection through approved assets, motion, narration, captions, deterministic assembly and technical QA. Build it sequentially, keep its GPU workload within the owner's 6 GB laptop, and never treat an unapproved output as a finished video. This application work can proceed before the Lanternfall business passes its audience and revenue gates.

The production quality bar includes actual animated shots when the owner asks for full motion. Still-image pans and zooms may be useful previews, but they do not satisfy that bar. Since local FramePack was too slow and stressful on this machine and paid video APIs may not be sustainable, the workbench must make motion generation optional and cost-visible; if no approved option fits, stop at a clearly labeled draft. Audio, captions, assembly, provenance, final review and manual publishing remain separate, explicit steps.

The current implementation is a set of Python scripts and a Remotion renderer, not the planned UI. Roadmap.md distinguishes working pieces from missing application features. The repository may be source-available under PolyForm Noncommercial 1.0.0; this license applies to project code only and does not replace third-party or generated-media terms.
# Appendix F — Quick Decision Matrix
| Question | Use this decision |
| --- | --- |
| Need cheap text classification? | Local Qwen |
| Need high-volume content drafts? | GPT-5.6 Luna or local Qwen (V2; V1 uses free-tier LLMs, R5) |
| Need balanced research synthesis? | GPT-5.6 Terra |
| Need difficult factual reasoning? | GPT-5.6 Sol |
| Need local speech? | Kokoro-82M (default, R5); Qwen3-TTS 0.6B as an A/B candidate |
| Need captions? | Forced alignment of the known script with faster-whisper or WhisperX |
| Need controllable image/video workflows? | ComfyUI |
| Need local LLM API? | Ollama or llama.cpp |
| Need provider routing? | LiteLLM |
| Need durable multi-step orchestration? | Temporal |
| Need deterministic React video templates? | Remotion |
| Need media encoding? | FFmpeg |
| Need current platform upload? | Official platform API |
# Appendix G — Practical V1 Content Pack
To minimize setup time, create one content pack with the following reusable assets: one narrator voice, three background music tracks with clear commercial rights, five sound effects, one caption preset, three scene transitions, one intro style, one ending style, one visual style guide, one brand config file, and ten prompt examples. This is enough to begin production without building a huge asset library.
# Appendix H — Recommended First Brand Direction
```text
Brand concept:
Original short cinematic stories about impossible situations.

Tone:
Mysterious, emotional, cinematic, intelligent.

Audience:
Global English-speaking viewers, approximately 18-34.

Core promises:
- every video has a clear premise
- every video has a payoff
- no franchise characters
- no fake “true story” framing
- no generic motivational filler

Primary recurring hooks:
- “He received a message from…”
- “Nobody noticed that…”
- “Every night at…”
- “What happened next…”
- “If this happened to you…”
```
# Appendix I — Build Order Summary for the Next 72 Hours
> **Revision 1.2:** Superseded by R11 (zero-cost stack and the Day 1–3 checklist); keep it only as a rough time budget.

```text
T+0h
Create repo + environment.
Install Python, Node, FFmpeg.
Install Ollama/llama.cpp.

T+4h
Implement idea + script JSON generation.

T+8h
Set up image generation workflow.

T+12h
Set up Qwen3-TTS.

T+16h
Set up faster-whisper.

T+20h
Build Remotion template.

T+26h
Render first complete video.

T+32h
Create 3-5 videos.

T+40h
Fix quality issues.

T+48h
Publish first batch manually.

T+72h
Reach 5-10 videos and freeze V1 lessons in this blueprint.
```
