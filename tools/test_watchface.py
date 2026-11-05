"""Behavioural checks for the generated WFF, run with unittest discovery."""
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

import generate_watchface as generator

ROOT = Path(__file__).resolve().parents[1]


def evaluate(expression, values):
    """Evaluate the numeric subset emitted for complication transforms."""
    for name, value in values.items():
        expression = expression.replace(f'[COMPLICATION.{name}]', str(value))
    # Translate the one guarded WFF conditional while retaining surrounding math.
    question = expression.find('?')
    if question >= 0:
        depth = 0
        start = question - 1
        while start >= 0:
            if expression[start] == ')':
                depth += 1
            elif expression[start] == '(':
                if depth == 0:
                    break
                depth -= 1
            start -= 1
        depth = 0
        end = question + 1
        while end < len(expression):
            if expression[end] == '(':
                depth += 1
            elif expression[end] == ')':
                if depth == 0:
                    break
                depth -= 1
            end += 1
        condition = expression[start + 1:question]
        yes, no = expression[question + 1:end].split(':')
        expression = expression[:start] + f'({yes} if {condition} else {no})' + expression[end + 1:]
    return eval(expression, {'__builtins__': {}}, {'max': max, 'clamp': lambda n, a, b: max(a, min(n, b))})


class WatchFaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.face = ET.parse(ROOT / generator.OUT).getroot()
        cls.expressions = {}
        for e in cls.face.iter('Expression'):
            expression = e.text.strip().replace('[HOUR_0_23]', 'hour').replace('[MINUTE]', 'minute')
            expression = expression.replace('[CONFIGURATION.fontStyle]', 'style').replace('&&', ' and ')
            cls.expressions[e.get('name')] = compile(expression, '<WFF condition>', 'eval')
        cls.compares = {e.get('expression'): e for e in cls.face.iter('Compare')}
        cls.spoken = {e.get('name'): e.text.replace("\\'", "'") for e in ET.parse(ROOT / 'watchface/src/main/res/values/spoken_times.xml').getroot()}

    def test_every_minute_selects_one_layout_and_spoken_phrase(self):
        # Exhaustive coverage, including saved unknown font choices and midnight rollover.
        for hour in range(24):
            for minute in range(60):
                for style in ('system', 'arvo', 'unknown'):
                    selected = []
                    for name, expression in self.expressions.items():
                        if eval(expression, {'__builtins__': {}}, {'hour': hour, 'minute': minute, 'style': style}):
                            selected.append(self.compares[name])
                    self.assertEqual(len(selected), 1, (hour, minute, style))
                    groups = selected[0].findall('Group')
                    expected = generator.fuzzy_lines(hour, minute)
                    for group in groups:
                        words = [font.text.strip() for font in group.iter('Font')]
                        self.assertEqual(words, expected)
                        reader = group.find('ScreenReader')
                        spoken = ' '.join(expected).replace('Half ', 'Half past ', 1)
                        self.assertEqual(self.spoken[reader.get('stringId')], spoken)

    def test_time_boundaries(self):
        for hour, minute, expected in [(23, 58, 'Midnight'), (11, 58, 'Noon'), (0, 3, 'Five Past Midnight'), (12, 33, 'Twenty-five To One'), (1, 30, 'Half One')]:
            self.assertEqual(generator.fuzzy_words(hour, minute), expected)

    def test_complication_edges(self):
        for slot in self.face.iter('ComplicationSlot'):
            arc = slot.find('BoundingArc')
            self.assertGreaterEqual(float(arc.get('thickness')) * 192 / 450, 48)
            self.assertEqual(float(arc.get('width')), 450)
            self.assertEqual(float(arc.get('height')), 450)
            start, end = float(arc.get('startAngle')), float(arc.get('endAngle'))
            ranged = slot.find("Complication[@type='RANGED_VALUE']//Transform").get('value')
            goal = slot.find("Complication[@type='GOAL_PROGRESS']//Transform").get('value')
            for expression in (ranged, goal):
                self.assertNotRegex(expression, r'\b(min|max)\(')
            for low, high, value, fraction in [(0, 100, -5, 0), (0, 100, 50, .5), (0, 100, 150, 1), (10, 10, 50, 0), (10, 0, 5, 0), (-100, 100, 0, .5)]:
                self.assertAlmostEqual(evaluate(ranged, {'RANGED_VALUE_MIN': low, 'RANGED_VALUE_MAX': high, 'RANGED_VALUE_VALUE': value}), start + (end-start)*fraction)
            for target, value, fraction in [(0, 5, 0), (-10, 5, 0), (100, -5, 0), (100, 50, .5), (100, 150, 1)]:
                self.assertAlmostEqual(evaluate(goal, {'GOAL_PROGRESS_TARGET_VALUE': target, 'GOAL_PROGRESS_VALUE': value}), start + (end-start)*fraction)
            self.assertIsNotNone(slot.find("Complication[@type='EMPTY']"))
            self.assertEqual(slot.find('Variant').get('value'), '0')


if __name__ == '__main__':
    unittest.main()
