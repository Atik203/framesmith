# Remotion renderer setup (Day 2)

The `renderer/` folder does not exist yet on purpose: `create-video` wants to make it itself. Create it on Day 2
(blueprint R11) so it is scaffolded with the current Remotion version:

```powershell
# from the repo root; follow Remotion's README if flags changed
npx create-video@latest --yes --blank renderer
```

Render specs come from `python scripts/build_render_spec.py` and live in `v1/renders/{id}.spec.json`. Every path in
a spec is relative to `v1/` (`assets/{id}/scene-01.png`, `audio/{id}.wav`, `subtitles/{id}.json`), so point
Remotion's public directory at `../v1` (check Remotion's `--public-dir` option on Day 2) and load files with
`staticFile(path)`.

Required compositions, both reading the render-spec JSON (`schemas/render_spec.schema.json`):

| Composition | Size | When |
| --- | --- | --- |
| `ShortVertical` | 1080x1920, 30 fps | Day 2 |
| `LongHorizontal` | 1920x1080, 30 fps | Week 1, before the long-form pilot |

Components to build as needed: HookScene, CharacterScene, CaptionOverlay, ProgressBar, CTA, Background.
Motion presets: push_in, push_out, pan_left, pan_right, parallax, micro_shake, focus_pull, cut_on_word.
Final encode: H.264, AAC, yuv420p via FFmpeg. Run the Part IX technical checks before publishing.

Licensing: Remotion is free for individuals and companies up to 3 people; a company license applies at 4+
people or when sold as a product (R5). Add a row to `provenance/licenses.csv` for it.

Fallback if Remotion slows you down before Gate A: burn ASS captions and motion with FFmpeg only.
