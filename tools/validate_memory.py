#!/usr/bin/env python3
"""Run Google's checksum-pinned WFF memory evaluator on a resource-only APK."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://github.com/google/watchface/releases/download/release/memory-footprint.jar'
SHA256 = '98892722dcb0cf3c872776fa5ec1ba5aea1289621f04d15324e854b1cdaa3460'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk', nargs='?', type=Path, default=ROOT / 'watchface/build/outputs/apk/release/watchface-release.apk')
    args = parser.parse_args()
    with ZipFile(args.apk) as apk:
        assert not any(n.endswith('.dex') or n.startswith('lib/') for n in apk.namelist()), 'WFF distribution must contain no DEX or native code'
    jar = ROOT / '.gradle-local/wff-tools/memory-footprint.jar'
    if not jar.exists():
        jar.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(URL, timeout=60) as response:
            data = response.read()
        assert hashlib.sha256(data).hexdigest() == SHA256, 'Upstream tool checksum changed; review before updating the pin'
        jar.write_bytes(data)
    assert hashlib.sha256(jar.read_bytes()).hexdigest() == SHA256, 'Memory evaluator checksum mismatch'
    java = str(Path(os.environ['JAVA_HOME']) / 'bin/java') if 'JAVA_HOME' in os.environ else 'java'
    command = [java, '-jar', str(jar), '--watch-face', str(args.apk), '--schema-version', '2']
    subprocess.run(command + ['--ambient-limit-mb', '10', '--active-limit-mb', '100'], check=True)
    report = subprocess.check_output(command + ['--report'], text=True)
    result = json.loads(report)
    assert result['maxAmbientBytes'] <= 10_000_000
    assert result['maxActiveBytes'] <= 100_000_000
    output = ROOT / 'watchface/build/reports/wff-memory.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report)
    print(report)


if __name__ == '__main__':
    main()
