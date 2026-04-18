# Release Assets

Generated assets for store and release prep.

Run:

```sh
python3 tools/generate_release_assets.py
```

Generated files:

- `watchface/src/main/res/drawable/preview.png`: watch face picker preview.
- `release-assets/screenshots/default.png`: default austere word face.
- `release-assets/screenshots/range-complication.png`: sample range arc.
- `release-assets/icon-512.png`: square release icon draft.

The generator uses vendored Liberation Sans font files in `release-assets/fonts`
so CI and local output stay byte-for-byte consistent. Liberation Fonts are
licensed under the SIL Open Font License 1.1; see
`../licenses/LiberationFonts-OFL-1.1.txt`.

These are draft assets for packaging and store listing work, not final marketing
copy or screenshots captured from a physical device.
