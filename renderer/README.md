# Framesmith renderer

This Remotion project assembles an approved render specification, scene media, narration, and caption timings into a video. The current implementation is a prototype and does not generate full-motion video shots.

## Local development

```powershell
npm ci
npm run lint
npm run dev
```

Render the registered composition from this directory with Remotion CLI after its content assets have been staged under `public/`. The output video belongs in the ignored `v1/renders/` working-data folder.

## Media and rights

Do not commit generated media, narration, model weights, credentials, or large binaries. This package's source is covered by the root PolyForm Noncommercial 1.0.0 license. Remotion and all other dependencies retain their own licenses; review Remotion's current terms before any business/commercial use.
