# Remotion renderer setup (Day 2)

The Remotion project is scaffolded in `renderer/`. Its first composition is `ShortVertical` (1080x1920,
30 fps), defined in `renderer/src/Composition.tsx`. It reads the render spec and subtitle JSON from the
repo and loads media from Remotion's `public/` directory.

Before rendering a content ID, stage copies of its scene PNGs and narration WAV under
`renderer/public/{content_id}/`. Keep the originals in `v1/`; staged media and rendered MP4s are ignored
by Git.

For `lf-short-001`, from the repo root:

```powershell
New-Item -ItemType Directory -Force renderer/public/lf-short-001
Copy-Item v1/assets/lf-short-001/scene-*.png renderer/public/lf-short-001/
Copy-Item v1/audio/lf-short-001.wav renderer/public/lf-short-001/
```

Then run from `renderer/`:

```powershell
npm run lint
npx remotion render src/index.ts ShortVertical ../v1/renders/lf-short-001.mp4 --public-dir=public
```

If Remotion's default browser is unavailable, pass an installed compatible Chromium executable with
`--browser-executable`. The render should use H.264 video, AAC audio and `yuv420p`; verify the output with
`ffprobe`, decode it with FFmpeg, and inspect representative frames before considering it ready for owner
review.

The `LongHorizontal` (1920x1080) composition remains a Week 1 task before the long-form pilot. Add a
provenance row for any model, checkpoint, voice, font, music or SFX used in published work.
