#!/usr/bin/env python3
"""Create developer-only WFF fixtures without changing the watch's clock or data.

Remove the fixture with --clear and rebuild before normal use. Release/Play
resources are never changed. The generated override is ignored by Git.
"""
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'watchface/src/developer/res/raw/watchface.xml'
COLORS = ['#FFF2F2EA', '#FFECEFF1', '#FFCFE8D6', '#FFEAD8B5']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clear', action='store_true')
    parser.add_argument('--time', default='12:25')
    parser.add_argument('--font', choices=['system', 'arvo'], default='system')
    parser.add_argument('--shade', type=int, choices=range(4), default=0)
    parser.add_argument('--range', nargs=3, type=float, metavar=('MIN', 'MAX', 'VALUE'))
    parser.add_argument('--goal', nargs=2, type=float, metavar=('TARGET', 'VALUE'))
    args = parser.parse_args()
    if args.clear:
        OUT.unlink(missing_ok=True)
        return
    hour, minute = map(int, args.time.split(':'))
    assert 0 <= hour < 24 and 0 <= minute < 60
    face = ET.parse(ROOT / 'watchface/src/main/res/raw/watchface.xml')
    for e in face.iter('Expression'):
        e.text = e.text.replace('[HOUR_0_23]', str(hour)).replace('[MINUTE]', str(minute))
        e.text = e.text.replace('[CONFIGURATION.fontStyle]', f'"{args.font}"')
    for font in face.iter('Font'):
        if font.text:
            font.text = font.text.strip()
    scene = face.find('Scene')
    for slot, values, kind in zip(list(scene.findall('ComplicationSlot')), [args.range, args.goal], ['RANGED_VALUE', 'GOAL_PROGRESS']):
        if values is None:
            continue
        group = ET.Element('Group', {'name': f'fixture_{kind}', 'x': '0', 'y': '0', 'width': '450', 'height': '450'})
        group.append(slot.find('Variant'))
        for child in slot.find(f"Complication[@type='{kind}']"):
            group.append(child)
        if kind == 'RANGED_VALUE':
            substitutions = dict(zip(['RANGED_VALUE_MIN', 'RANGED_VALUE_MAX', 'RANGED_VALUE_VALUE'], values))
        else:
            substitutions = dict(zip(['GOAL_PROGRESS_TARGET_VALUE', 'GOAL_PROGRESS_VALUE'], values))
        for e in group.iter():
            for name, value in list(e.attrib.items()):
                for key, number in substitutions.items():
                    value = value.replace(f'[COMPLICATION.{key}]', str(number))
                e.set(name, value)
        scene.remove(slot)
        scene.append(group)
    for e in face.iter():
        for key, value in list(e.attrib.items()):
            e.set(key, value.replace('[CONFIGURATION.textShade]', COLORS[args.shade]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(face, space='    ')
    face.write(OUT, encoding='utf-8', xml_declaration=True)
    print(f'Developer fixture: {args.time}, {args.font}, shade {args.shade}')


if __name__ == '__main__':
    main()
