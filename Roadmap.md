# Roadmap — Framesmith

Plan: [`blueprint.md`](blueprint.md), Revision 1.5 / R16 · Last updated: 2026-10-10
Project status: **production scripts and Remotion renderer exist; the operator UI and full-motion generation path do not.**

This roadmap tracks software work and production readiness. A generated or technically valid MP4 is not automatically a quality-approved output. Tick a checkbox only when its stated evidence exists; add the completion date in the same change.

## Current verified state

- [x] Python scripts cover idea/script drafting, Kokoro narration, known-script caption alignment, render-spec construction, validation, environment checks, and tracking review.
- [x] Remotion composition and media were copied under `renderer/public/lf-short-001/` for local `lf-short-001` rendering; media remains ignored by Git.
- [x] `v1/renders/lf-short-001.mp4` exists: H.264 video, AAC audio, 1080×1920, 30/1 fps, 46.784 seconds. Full FFmpeg decode completed without an error on 2026-10-10.
- [ ] `lf-short-001` meets the visual quality bar. **Hold:** the owner reviewed it and said the still-image motion does not feel like a full-fledged animated reel; scenes 6–8 are byte-identical images. No owner approval or publication is recorded.
- [ ] Local operator UI, five-idea selection screen, resumable job queue, image review screen, and paid video-generation cost gate.
- [ ] Affordable full-motion video path. FramePack was tried by the owner and caused excessive laptop stress and long generation time. Do not use it as the default. No API provider is selected or authorized for spend.
- [ ] Confirm and record model/checkpoint/voice/font/music provenance before any public release or commercial use of output.

The final `lf-short-001` script was manually tightened after the local model produced invalid output. Do not claim that a model authored the final script. Its rendered video remains a technical draft, not a human-approved final cut.

## Project decisions that apply to every phase

- The application should run locally and execute bounded pipeline steps sequentially. “Agents” are task roles in an ordered queue, not concurrent autonomous workers.
- Run only one GPU-heavy model at a time on the owner's RTX 3060 laptop with 6 GB VRAM. Narration, alignment, and final composition are separate CPU/render steps.
- Keep the owner in control: select ideas; edit/approve the script; review/accept images; explicitly click to start any paid motion generation; review the finished cut.
- Paid generation stays off by default. Before an API request, show provider, duration, resolution, per-shot estimate, retry exposure, and cumulative project spend. Require explicit owner approval and an owner-set cap. Recheck live prices/terms before use.
- Still-image pans/zooms may be used as a preview or clearly labeled fallback. They do not count as full-motion generation for the owner's stated quality bar.
- No upload or publishing workflow is in the current scope. No secrets, generated media, model weights, or large binaries in Git.
- Code license: PolyForm Noncommercial 1.0.0. Generated media and third-party assets are governed by their own terms.

## Phase 0 — Public source-project readiness

Done when the source repository explains its scope and current limits, a code license is present, private/generated files remain excluded, and the owner has chosen whether/when to make the GitHub repository public.

- [x] Add project overview, planned workflow, current limitations, noncommercial code-license notice, and suggested GitHub description/topics to `README.md` (2026-10-10).
- [x] Add PolyForm Noncommercial 1.0.0 for project code only (2026-10-10).
- [x] Update blueprint and agent instructions to match the phased workbench plan (2026-10-10).
- [x] Make Framesmith the sole current project identity; rename the production profile and use `fs-*` for new IDs while preserving existing `lf-*` records (2026-10-10).
- [x] Add GitHub contribution, security, conduct, issue, and pull request guidance (2026-10-10).
- [ ] Verify the GitHub About description/topics are set; the current `gh` authentication token is invalid, so repository metadata could not be checked or changed from this session.
- [ ] Owner reviews repository contents/history and changes GitHub visibility to public when ready. Visibility stays owner-controlled.

## Phase 1 — Finish one manual-quality production loop

Done when one reel uses distinct, approved assets, actual motion that meets the owner's bar, narration, accurate captions, and technical QA, then receives the owner's final-cut review. Publishing is not required for this software milestone.

- [ ] Review the script and final premise as the owner; record human review honestly.
- [ ] Replace or re-plan repeated stills in `lf-short-001` and record the source/checkpoint/license for each new image.
- [ ] Select and test a motion approach within an owner-approved cost/compute limit. If no option meets the motion-quality bar, keep this reel a draft.
- [ ] Render the complete approved composition with narration and captions.
- [ ] Inspect representative frames and listen to the full cut; fix pacing, visual continuity, caption timing/readability, and audio issues.
- [ ] Record technical QA and owner review. Do not mark the reel published unless the owner publishes it manually.

## Phase 2 — Local operator UI and workflow queue

Do not pick a UI framework before a short design and feasibility step. Prefer a small local interface and local state until requirements show they are insufficient.

- [ ] Define the minimum screen flow and local project state format.
- [ ] Generate a batch of five idea cards and let the owner select one or more.
- [ ] Generate a premise/script draft, show provider/model/prompt metadata, and require owner edit/approval before visual work.
- [ ] Persist each job's state, inputs, outputs, logs, and retry status; support pause/resume/cancel without losing accepted assets.
- [ ] Serialize GPU-heavy jobs; show which model is active and do not overlap image/video model workloads.
- [ ] Add clear errors and a preview before replacing an approved image or output.

## Phase 3 — Local image generation and approval

- [ ] Generate scene images one at a time from an approved script and shot plan.
- [ ] Show all proposed images with the matching scene/narration beat.
- [ ] Let the owner accept, reject, or regenerate individual images; do not continue to motion until required images are accepted.
- [ ] Save prompts, seeds, model/checkpoint identifiers, license source, and review status with each asset.
- [ ] Detect exact or near-duplicate scene images and warn before rendering.

## Phase 4 — Motion generation decision

Done when at least one selected approach has been tested on this machine or by an explicitly approved API request, its actual quality/time/cost are recorded, and the owner has chosen whether to use it.

- [x] Exclude FramePack from the routine local path based on the owner's observed heat/stress and latency (2026-10-10).
- [ ] Compare current image-to-video services and their shot-duration constraints, prices, data terms, and output rights immediately before any test; the October 2026 estimates are not a price commitment.
- [ ] Choose one representative approved still and request only one short sample first.
- [ ] Display and enforce a user-set spend cap; include retries and discarded outputs in the cost record.
- [ ] If no option is affordable and visually acceptable, stop at the image-review stage or label a still-motion export as an animatic. Do not present it as a full-motion reel.
- [ ] Keep generated clips out of Git and document each provider's rights separately from the project-code license.

## Phase 5 — Assembly, QA, and owner review

- [ ] Join approved motion shots deterministically from the render spec.
- [ ] Add Kokoro narration and align the known script to the audio; do not re-transcribe to invent script text.
- [ ] Add caption-safe layout, licensed audio only when rights are recorded, and output H.264/AAC MP4.
- [ ] Run ffprobe checks for codec, 1080×1920 dimensions, 30 fps, audio stream, duration, and expected output file.
- [ ] Decode the full MP4 and inspect representative frames for missing assets, black frames, repeated scenes, visual continuity, and caption clipping.
- [ ] Present the final render to the owner for a human pass; keep that approval distinct from automated QA.
- [ ] Record technical QA and owner review in the production log.

Publishing, channel operations, and content monetization are outside the current project scope.

## GitHub project metadata

Suggested description: **A work-in-progress, local-first, human-reviewed AI video production workbench.**

Suggested topics: `ai-video`, `local-first`, `remotion`, `ollama`, `video-production`, `human-in-the-loop`.

The source-code repository may be public under PolyForm Noncommercial 1.0.0. The owner chooses when to change its visibility. Public source availability does not authorize commercial use under this license and does not clear the separate rights of model weights, generated media, or dependencies.
