# Contributing to Framesmith

Thanks for taking an interest in Framesmith. The project is an early, local-first workbench; check the
[README](README.md), [blueprint](blueprint.md), and [roadmap](Roadmap.md) before proposing a change. The
blueprint is the source of truth for project decisions.

## Before you start

- For a substantial change, open an issue first to discuss its scope and fit with the roadmap.
- Keep changes small and aligned with the current roadmap. Do not add paid services, paid API use, GPU-heavy
  dependencies, publishing automation, or gated infrastructure without the owner's prior approval.
- Do not include secrets, `.env` files, generated media, model weights, or other large binaries in issues or
  pull requests. Keep generated work and personal data local.
- Check licenses and provenance for any model, checkpoint, voice, font, music, sound effect, or other asset.

## Make and submit a change

1. Fork the repository and create a focused branch.
2. Follow the existing Windows-first Python conventions and repository instructions in `AGENTS.md`.
3. Update `blueprint.md` first if your change alters a project decision, schema, brand rule, tracking field,
   or folder layout. Update `Roadmap.md` only when evidence shows a checkbox's done condition is met.
4. Run the checks relevant to your change. For Python changes, run `python -m pytest -q` and
   `python -m ruff check .`; for renderer changes, run `npm run lint` from `renderer/`.
5. Open a pull request with the purpose, user-visible effect, verification performed, and any limitations.

By submitting a contribution, you agree that it is provided under the repository's
[PolyForm Noncommercial 1.0.0 license](LICENSE), to the extent you hold the rights to make that grant.
The license does not grant commercial use. Keep third-party code and assets under their own terms and record
relevant provenance.

Contributions may be reviewed, declined, or left unanswered; opening a pull request does not guarantee
acceptance or a response time.
