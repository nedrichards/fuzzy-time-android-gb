#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WATCHFACE_PREVIEW = ROOT / "watchface/src/main/res/drawable/preview.png"
RELEASE_ASSETS = ROOT / "release-assets"
SCREENSHOTS = RELEASE_ASSETS / "screenshots"

TEXT = "#F2F2EA"
TRACK = "#33332F"
GREEN = "#CFE8D6"
BLACK = "#000000"
FONT_REGULAR = ROOT / "release-assets/fonts/liberation_sans_regular.ttf"
FONT_BOLD = ROOT / "release-assets/fonts/liberation_sans_bold.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, font_obj: ImageFont.FreeTypeFont, fill: str) -> None:
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    width = bbox[2] - bbox[0]
    draw.text(((450 - width) / 2, y), text, font=font_obj, fill=fill)


def draw_arc(draw: ImageDraw.ImageDraw, fill: str, progress: float | None = None) -> None:
    bbox = (10, 10, 440, 440)
    draw.arc(bbox, start=200, end=340, fill=TRACK, width=4)
    if progress is not None:
        end = 200 + (140 * max(0.0, min(progress, 1.0)))
        draw.arc(bbox, start=200, end=end, fill=fill, width=5)


def watchface_image(progress: float | None = None, text_fill: str = TEXT) -> Image.Image:
    image = Image.new("RGB", (450, 450), BLACK)
    draw = ImageDraw.Draw(image)
    draw_arc(draw, text_fill, progress)
    draw_centered(draw, "Twenty-five Past", 160, font(FONT_REGULAR, 42), text_fill)
    draw_centered(draw, "Twelve", 222, font(FONT_BOLD, 56), text_fill)
    return image


def store_icon() -> Image.Image:
    image = Image.new("RGB", (512, 512), BLACK)
    draw = ImageDraw.Draw(image)
    draw.ellipse((20, 20, 492, 492), outline=TEXT, width=3)
    draw.arc((42, 42, 470, 470), start=200, end=292, fill=GREEN, width=8)
    title = font(FONT_BOLD, 58)
    small = font(FONT_REGULAR, 30)
    for text, y, font_obj in [("Fuzzy", 184, title), ("Time GB", 248, small)]:
        bbox = draw.textbbox((0, 0), text, font=font_obj)
        draw.text(((512 - (bbox[2] - bbox[0])) / 2, y), text, font=font_obj, fill=TEXT)
    return image


def main() -> None:
    WATCHFACE_PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)

    default = watchface_image(progress=None)
    default.save(WATCHFACE_PREVIEW)
    default.save(SCREENSHOTS / "default.png")

    watchface_image(progress=0.66, text_fill=GREEN).save(SCREENSHOTS / "range-complication.png")
    store_icon().save(RELEASE_ASSETS / "icon-512.png")


if __name__ == "__main__":
    main()
