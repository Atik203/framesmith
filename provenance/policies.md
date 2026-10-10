# Asset rights and provenance policy

Source: blueprint Parts VIII, XV and XX, R5, R9. Update the blueprint first if this changes.

1. **Record before use.** Every model, checkpoint, LoRA, voice, font, music track and sound effect that ends up in
   a published video gets a row in `licenses.csv` *before* it is used: source URL, license name, whether
   commercial use is allowed, and the date checked.
2. **"Open source" is not "commercially free".** Read the model card and license for use restrictions and
   derivative rules. If the answer is unclear, do not use it in monetized work; hold for human review.
3. **Music and SFX:** only assets with an explicit commercial license (for example the YouTube Audio Library).
   No audio taken from random uploads. Store the license reference per track.
4. **Generated images:** keep the ComfyUI workflow JSON in `comfyui/workflows/` with checkpoint name, seed and
   prompt. No logos, no readable text, no copyrighted characters, no real people's likeness.
5. **Voices:** use only voices with a license that permits commercial output. No cloning a person's voice
   without permission.
6. **Disclosure:** use the platform's synthetic-media disclosure when content is realistic and answer YouTube
   Studio's synthetic-content question honestly. Record it in `log.csv` (`disclosure`).
7. **Originality:** no re-uploads and no cosmetic edits of other people's content.
