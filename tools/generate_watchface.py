#!/usr/bin/env python3
from pathlib import Path


OUT = Path("watchface/src/main/res/raw/watchface.xml")
INTERACTIVE_COLOR = "[CONFIGURATION.textShade]"
AMBIENT_COLOR = "#FF777777"
FONT_OPTIONS = [
    ("system", "SYNC_TO_DEVICE"),
    ("serif", "liberation_serif_regular"),
    ("mono", "liberation_mono_regular"),
]


def render_range_complication(indent: str) -> list[str]:
    return [
        f'{indent}<ComplicationSlot slotId="0" displayName="range_complication_label" supportedTypes="RANGED_VALUE GOAL_PROGRESS WEIGHTED_ELEMENTS EMPTY" x="0" y="0" width="450" height="450">',
        f'{indent}    <Variant mode="AMBIENT" target="alpha" value="0" />',
        f'{indent}    <BoundingArc centerX="225" centerY="225" width="430" height="430" thickness="8" startAngle="-70" endAngle="70" isRoundEdge="TRUE" outlinePadding="8" />',
        f'{indent}    <Complication type="RANGED_VALUE">',
        f'{indent}        <PartDraw x="0" y="0" width="450" height="450">',
        f'{indent}            <Arc centerX="225" centerY="225" width="430" height="430" startAngle="-70" endAngle="70">',
        f'{indent}                <Stroke color="#22F2F2EA" thickness="4" cap="ROUND" />',
        f'{indent}            </Arc>',
        f'{indent}            <Arc centerX="225" centerY="225" width="430" height="430" startAngle="-70" endAngle="-70">',
        f'{indent}                <Transform target="endAngle" value="-70 + (([COMPLICATION.RANGED_VALUE_VALUE] - [COMPLICATION.RANGED_VALUE_MIN]) / ([COMPLICATION.RANGED_VALUE_MAX] - [COMPLICATION.RANGED_VALUE_MIN]) * 140)" />',
        f'{indent}                <Stroke color="[CONFIGURATION.textShade]" thickness="5" cap="ROUND" />',
        f'{indent}            </Arc>',
        f'{indent}        </PartDraw>',
        f'{indent}    </Complication>',
        f'{indent}    <Complication type="GOAL_PROGRESS">',
        f'{indent}        <PartDraw x="0" y="0" width="450" height="450">',
        f'{indent}            <Arc centerX="225" centerY="225" width="430" height="430" startAngle="-70" endAngle="70">',
        f'{indent}                <Stroke color="#22F2F2EA" thickness="4" cap="ROUND" />',
        f'{indent}            </Arc>',
        f'{indent}            <Arc centerX="225" centerY="225" width="430" height="430" startAngle="-70" endAngle="-70">',
        f'{indent}                <Transform target="endAngle" value="-70 + min(([COMPLICATION.GOAL_PROGRESS_VALUE] / [COMPLICATION.GOAL_PROGRESS_TARGET_VALUE]) * 140, 140)" />',
        f'{indent}                <Stroke color="[CONFIGURATION.textShade]" thickness="5" cap="ROUND" />',
        f'{indent}            </Arc>',
        f'{indent}        </PartDraw>',
        f'{indent}    </Complication>',
        f'{indent}    <Complication type="WEIGHTED_ELEMENTS">',
        f'{indent}        <PartDraw x="0" y="0" width="450" height="450">',
        f'{indent}            <Arc centerX="225" centerY="225" width="430" height="430" startAngle="-70" endAngle="70">',
        f'{indent}                <Stroke color="[COMPLICATION.WEIGHTED_ELEMENTS_BACKGROUND_COLOR]" thickness="4" cap="ROUND" />',
        f'{indent}            </Arc>',
        f'{indent}            <Arc centerX="225" centerY="225" width="430" height="430" startAngle="-70" endAngle="70">',
        f'{indent}                <WeightedStroke colors="[COMPLICATION.WEIGHTED_ELEMENTS_COLORS]" weights="[COMPLICATION.WEIGHTED_ELEMENTS_WEIGHTS]" thickness="5" discreteGap="2" interpolate="FALSE" cap="BUTT" />',
        f'{indent}            </Arc>',
        f'{indent}        </PartDraw>',
        f'{indent}    </Complication>',
        f'{indent}    <Complication type="EMPTY" />',
        f'{indent}</ComplicationSlot>',
    ]

MINUTE_BUCKETS = [
    (0, 2),
    (3, 7),
    (8, 12),
    (13, 17),
    (18, 22),
    (23, 27),
    (28, 32),
    (33, 37),
    (38, 42),
    (43, 47),
    (48, 52),
    (53, 57),
    (58, 59),
]

HOURS = {
    0: "Midnight",
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Eleven",
    12: "Noon",
    13: "One",
    14: "Two",
    15: "Three",
    16: "Four",
    17: "Five",
    18: "Six",
    19: "Seven",
    20: "Eight",
    21: "Nine",
    22: "Ten",
    23: "Eleven",
}


def fuzzy_words(hour: int, minute: int) -> str:
    return " ".join(fuzzy_lines(hour, minute))


def fuzzy_lines(hour: int, minute: int) -> list[str]:
    fuzzy_hour = hour
    fuzzy_minute = ((minute + 2) // 5) * 5

    if fuzzy_minute > 55:
        fuzzy_minute = 0
        fuzzy_hour = (fuzzy_hour + 1) % 24

    prefix = ""
    target_hour = fuzzy_hour
    if fuzzy_minute != 0 and (
        fuzzy_minute >= 10 or fuzzy_minute == 5 or fuzzy_hour == 0 or fuzzy_hour == 12
    ):
        if fuzzy_minute == 15:
            prefix = "Quarter Past"
        elif fuzzy_minute == 45:
            prefix = "Quarter To"
            target_hour = (fuzzy_hour + 1) % 24
        elif fuzzy_minute == 30:
            prefix = "Half Past"
        elif fuzzy_minute < 30:
            prefix = f"{number_words(fuzzy_minute)} Past"
        else:
            prefix = f"{number_words(60 - fuzzy_minute)} To"
            target_hour = (fuzzy_hour + 1) % 24

    hour_words = HOURS[target_hour]
    if fuzzy_minute == 0 and target_hour not in (0, 12):
        return [hour_words, "O'Clock"]
    if prefix:
        return [prefix, hour_words]
    return [hour_words]


def number_words(num: int) -> str:
    ones = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    tens_val = (num // 10) % 10
    ones_val = num % 10
    parts = []
    if tens_val > 0:
        if tens_val == 1 and num != 10:
            return teens[ones_val]
        if ones_val > 0:
            return f"{tens[tens_val]}-{ones[ones_val].lower()}"
        parts.append(tens[tens_val])
    if ones_val > 0 or num == 0:
        parts.append(ones[ones_val])
    return " ".join(parts)


def expression_for(hour: int, start: int, end: int) -> str:
    if start == end:
        minute_expr = f"[MINUTE] == {start}"
    else:
        minute_expr = f"[MINUTE] >= {start} && [MINUTE] <= {end}"
    return f"[HOUR_0_23] == {hour} && {minute_expr}"


def render_text_parts(
    text_lines: list[str],
    indent: str,
    font_family: str,
    color: str,
    ambient: bool = False,
) -> list[str]:
    if len(text_lines) == 1:
        layout = [(text_lines[0], 194, 82, 58, "BOLD")]
    elif text_lines[1] == "O'Clock":
        layout = [(text_lines[0], 165, 72, 60, "BOLD"), (text_lines[1], 227, 50, 38, "NORMAL")]
    else:
        layout = [(text_lines[0], 160, 58, 42, "NORMAL"), (text_lines[1], 222, 72, 56, "BOLD")]

    rendered = []
    for text, y, height, size, weight in layout:
        if ambient:
            size = max(28, size - 8)
            weight = "NORMAL"
        rendered.extend(
            [
                f'{indent}<PartText x="24" y="{y}" width="402" height="{height}">',
                f'{indent}    <Text align="CENTER" maxLines="1">',
                f'{indent}        <Font color="{color}" family="{font_family}" size="{size}" weight="{weight}">',
                f'{indent}            <![CDATA[{text}]]>',
                f'{indent}        </Font>',
                f'{indent}    </Text>',
                f'{indent}</PartText>',
            ]
        )
    return rendered


def main() -> None:
    cases = []
    for hour in range(24):
        for start, end in MINUTE_BUCKETS:
            cases.append((hour, start, end, fuzzy_lines(hour, start)))

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<WatchFace width="450" height="450">',
        '    <Metadata key="CLOCK_TYPE" value="DIGITAL" />',
        '    <Metadata key="PREVIEW_TIME" value="10:08:32" />',
        '',
        '    <UserConfigurations>',
        '        <ColorConfiguration id="textShade" displayName="text_shade_label" defaultValue="0">',
        '            <ColorOption id="0" displayName="shade_warm_white_label" colors="#FFF2F2EA" />',
        '            <ColorOption id="1" displayName="shade_cool_white_label" colors="#FFECEFF1" />',
        '            <ColorOption id="2" displayName="shade_soft_green_label" colors="#FFCFE8D6" />',
        '            <ColorOption id="3" displayName="shade_dim_amber_label" colors="#FFEAD8B5" />',
        '        </ColorConfiguration>',
        '        <ListConfiguration id="fontStyle" displayName="font_style_label" screenReaderText="font_style_label" defaultValue="system">',
        '            <ListOption id="system" displayName="font_system_label" screenReaderText="font_system_label" />',
        '            <ListOption id="serif" displayName="font_serif_label" screenReaderText="font_serif_label" />',
        '            <ListOption id="mono" displayName="font_mono_label" screenReaderText="font_mono_label" />',
        '        </ListConfiguration>',
        '    </UserConfigurations>',
        '',
        '    <Scene backgroundColor="#FF000000">',
        *render_range_complication("        "),
        '        <Condition>',
        '            <Expressions>',
    ]

    for index, (hour, start, end, _) in enumerate(cases):
        lines.extend(
            [
                f'                <Expression name="case_{index:03d}">',
                f'                    <![CDATA[{expression_for(hour, start, end)}]]>',
                '                </Expression>',
            ]
        )
        for option_id, _ in FONT_OPTIONS:
            lines.extend(
                [
                    f'                <Expression name="case_{index:03d}_{option_id}">',
                    f'                    <![CDATA[{expression_for(hour, start, end)} && [CONFIGURATION.fontStyle] == "{option_id}"]]>',
                    '                </Expression>',
                ]
            )

    lines.extend(
        [
            '            </Expressions>',
        ]
    )

    for index, (_, _, _, text_lines) in enumerate(cases):
        for option_id, font_family in FONT_OPTIONS:
            lines.append(f'            <Compare expression="case_{index:03d}_{option_id}">')
            lines.append('                <Group name="interactive_time" x="0" y="0" width="450" height="450">')
            lines.append('                    <Variant mode="AMBIENT" target="alpha" value="0" />')
            lines.extend(render_text_parts(text_lines, "                    ", font_family, INTERACTIVE_COLOR))
            lines.append('                </Group>')
            lines.append('                <Group name="ambient_time" x="0" y="0" width="450" height="450" alpha="0">')
            lines.append('                    <Variant mode="AMBIENT" target="alpha" value="255" />')
            lines.extend(render_text_parts(text_lines, "                    ", font_family, AMBIENT_COLOR, ambient=True))
            lines.append('                </Group>')
            lines.append('            </Compare>')
        lines.append(f'            <Compare expression="case_{index:03d}">')
        lines.append('                <Group name="interactive_time" x="0" y="0" width="450" height="450">')
        lines.append('                    <Variant mode="AMBIENT" target="alpha" value="0" />')
        lines.extend(render_text_parts(text_lines, "                    ", "SYNC_TO_DEVICE", INTERACTIVE_COLOR))
        lines.append('                </Group>')
        lines.append('                <Group name="ambient_time" x="0" y="0" width="450" height="450" alpha="0">')
        lines.append('                    <Variant mode="AMBIENT" target="alpha" value="255" />')
        lines.extend(render_text_parts(text_lines, "                    ", "SYNC_TO_DEVICE", AMBIENT_COLOR, ambient=True))
        lines.append('                </Group>')
        lines.append('            </Compare>')

    lines.extend(
        [
            '            <Default>',
        ]
    )
    lines.extend(render_text_parts(["Time"], "                ", "SYNC_TO_DEVICE", INTERACTIVE_COLOR))
    lines.extend(
        [
            '            </Default>',
            '        </Condition>',
            '    </Scene>',
            '</WatchFace>',
            '',
        ]
    )

    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
