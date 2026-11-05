#!/usr/bin/env python3
"""Conservative font/layout and AOD checks for this text-only face.

This is a glyph-bounds estimate, not a replacement for device rendering or Play
review. Supply a device font for SYNC_TO_DEVICE when validating a specific watch.
"""
import argparse
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--system-font', type=Path, default=ROOT / 'release-assets/fonts/liberation_sans_regular.ttf')
    args = parser.parse_args()
    face = ET.parse(ROOT / 'watchface/src/main/res/raw/watchface.xml').getroot()
    assert face.find('Scene').get('backgroundColor') == '#FF000000'
    for slot in face.iter('ComplicationSlot'):
        assert slot.find("Variant[@mode='AMBIENT'][@target='alpha']").get('value') == '0'
    worst = (0, '')
    layouts = 0
    for group in face.iter('Group'):
        ambient = group.get('name') == 'ambient_time'
        area = 0
        phrase = []
        for part in group.findall('PartText'):
            font = part.find('Text/Font')
            text = font.text.strip()
            phrase.append(text)
            family = font.get('family')
            path = ROOT / 'watchface/src/main/res/font/arvo_regular.ttf' if family == 'arvo_regular' else args.system_font
            f = ImageFont.truetype(str(path), int(font.get('size')))
            # Ink bounding rectangles deliberately overestimate lit pixels.
            left, top, right, bottom = f.getbbox(text)
            width, height = right-left+2, bottom-top+2
            if font.get('weight') == 'BOLD':
                width += 2  # Allow for system-synthesized bold in the fit check.
            assert width <= float(part.get('width')), (text, family, 'width', width)
            assert height <= float(part.get('height')), (text, family, 'height', height)
            x = float(part.get('x')) + (float(part.get('width'))-width)/2
            y = float(part.get('y'))
            # Check the entire declared text band against the circular display.
            for px in (x, x+width):
                for py in (y, y+float(part.get('height'))):
                    assert math.hypot(px-225, py-225) <= 225, (text, family, 'circle')
            if ambient:
                color = font.get('color').removeprefix('#')
                assert len(color) == 8 and color[:2] == 'FF'
                brightness = sum(int(color[i:i+2], 16) for i in (2,4,6)) / (3*255)
                area += width * height * brightness
        if ambient:
            ratio = area / (math.pi*225**2)
            assert ratio <= .15, ('AOD bound exceeded', phrase, ratio)
            if ratio > worst[0]:
                worst = (ratio, ' '.join(phrase))
        layouts += 1
    print(json.dumps({'layouts_checked': layouts, 'system_font': args.system_font.name,
                      'worst_aod_glyph_rectangle_bound_percent': round(worst[0]*100, 2),
                      'worst_phrase': worst[1], 'limit_percent': 15}, indent=2))


if __name__ == '__main__':
    main()
