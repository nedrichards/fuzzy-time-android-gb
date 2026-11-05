#!/usr/bin/env python3
"""Gate on the validator's actual result (some releases exit zero on failure)."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml', nargs='?', type=Path, default=ROOT / 'watchface/src/main/res/raw/watchface.xml')
    args = parser.parse_args()
    java = str(Path(os.environ['JAVA_HOME']) / 'bin/java') if 'JAVA_HOME' in os.environ else 'java'
    result = subprocess.run([java, '-jar', str(ROOT / 'tools/wff-validator.jar'), '2', str(args.xml)], capture_output=True, text=True)
    output = result.stdout + result.stderr
    print(output, end='')
    if result.returncode or 'PASSED :' not in output or 'FAILED :' in output:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
