#!/usr/bin/env python3
"""Derive picker/store images from committed, device-rendered screenshots."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / 'release-assets/screenshots'


def main():
    # Screenshots are captured sources, never redrawn with substitute fonts.
    with Image.open(SCREENSHOTS / 'default.png') as source:
        assert source.width == source.height, 'Use a square watch-face capture'
        face = source.convert('RGB')
    face.resize((450, 450), Image.Resampling.LANCZOS).save(
        ROOT / 'watchface/src/main/res/drawable/preview.png')
    # The actual circular face fills the icon; no branding or device frame.
    icon = face.resize((512, 512), Image.Resampling.LANCZOS).convert('RGBA')
    mask = Image.new('L', (512, 512))
    ImageDraw.Draw(mask).ellipse((0, 0, 511, 511), fill=255)
    icon.putalpha(mask)
    icon.save(ROOT / 'release-assets/icon-512.png')
    for name in ('range-complication.png', 'arvo.png'):
        with Image.open(SCREENSHOTS / name) as source:
            assert source.width == source.height


if __name__ == '__main__':
    main()
