# Fuzzy Time GB

A minimal word-based Watch Face Format face for Wear OS. It displays fuzzy
British English time phrases based on the C logic from the Pebble watchface [fuzzy-time-gb](https://github.com/nedrichards/fuzzy-time-gb).

The Android app module is resource-only: `android:hasCode="false"` and WFF
version 2. The helper script in `tools/` regenerates the declarative XML, but it
is not packaged into the watch face APK.

The optional Arvo style bundles the Arvo typeface, licensed under the SIL Open
Font License 1.1. See `licenses/Arvo-OFL.txt`. Release asset generation also
vendors Liberation Sans under the same license; see
`licenses/LiberationFonts-OFL-1.1.txt`.

![The watchface, showing the current time and a range complication](release-assets/screenshots/default.png "Watchface screenshot")

## Build

The project uses Gradle 9, Android Gradle Plugin 9, and Watch Face Format v2.
Gradle is configured to run the build daemon with a JetBrains JDK 21 toolchain
from `gradle/gradle-daemon-jvm.properties`; if a matching JDK is not available
locally, Gradle can provision one via the Foojay resolver configured in
`settings.gradle.kts`.

```sh
./gradlew :watchface:assembleRelease
```

On local machines that do not have `ANDROID_HOME` configured globally, point the
wrapper at your Android SDK:

```sh
env ANDROID_HOME=/var/home/nedr/Android/Sdk \
  ANDROID_SDK_ROOT=/var/home/nedr/Android/Sdk \
  ./gradlew :watchface:assembleRelease
```

Release APKs deliberately use the Android debug/test key for developer installs.
For an isolated installation alongside a differently signed existing copy, use
`:watchface:assembleDeveloper` (package suffix `.dev`). An unsigned App Bundle
for future Play signing is available with `:watchface:bundlePlay`; it is never
published automatically.

## Regenerate Watch Face XML

```sh
python3 tools/generate_watchface.py
```

## Regenerate Release Assets

```sh
python3 tools/generate_release_assets.py
```

## Check watch face behaviour and resource budgets

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/check_watchface.py
python3 tools/validate_memory.py
```

The memory command checks the release APK and downloads Google's evaluator with
a pinned SHA-256. `check_watchface.py` estimates a conservative ambient glyph
bound and checks circular text fit; pass `--system-font /path/to/device-font.ttf`
to check a particular watch. Neither check replaces on-device testing.

For reproducible device tests without changing the watch clock, use
`python3 tools/device_fixture.py --time 12:25 --font arvo --range 0 100 66`, then
build/install the developer variant. Run `python3 tools/device_fixture.py --clear`
and rebuild afterward. Fixtures affect only the developer variant.

## Validate WFF

```sh
python3 tools/validate_wff.py
```

---
*Co-authored with a bunch of different AIs*