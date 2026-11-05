# Release assets

`screenshots/default.png`, `screenshots/range-complication.png` and
`screenshots/arvo.png` are Wear OS emulator captures of the actual WFF renderer,
using fixed time and sample complication values through the developer-only
fixture. The default uses the system font; Arvo shows the bundled alternative.
There are no device frames, branding overlays or personal health data.

Capture replacements with `android screen capture --device <serial> -o <path>`
after activating the developer fixture. Inspect the images for system overlays
before committing them. Clear the fixture and rebuild after capturing.

Run `python3 tools/generate_release_assets.py` to derive the picker preview and
512px store icon from `screenshots/default.png`. The generator does not redraw
the face or synthesize screenshots. The icon uses only the face experience,
without extra text, and scales the circular face to the asset edges.

The older vendored Liberation Sans fonts and their OFL license remain available
for the portable layout/ambient checker; they are not used to draw screenshots.
