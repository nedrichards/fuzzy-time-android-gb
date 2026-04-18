# Fuzzy Time GB

A minimal word-based Watch Face Format face for Wear OS. It displays fuzzy
British English time phrases based on the original `fuzzy-time-gb` C logic.

The Android app module is resource-only: `android:hasCode="false"` and WFF
version 2. The helper script in `tools/` regenerates the declarative XML, but it
is not packaged into the watch face APK.

The optional Serif and Mono styles bundle Liberation Fonts, licensed under the
SIL Open Font License 1.1. See `licenses/LiberationFonts-OFL-1.1.txt`.

## Build

```sh
./gradlew :watchface:assembleDebug
```

On this machine the build currently needs JDK 17 rather than the default Java
25 runtime:

```sh
env JAVA_HOME=/var/home/nedr/.jdks/jbr-17.0.14 \
  PATH=/var/home/nedr/.jdks/jbr-17.0.14/bin:$PATH \
  ANDROID_HOME=/var/home/nedr/Android/Sdk \
  ANDROID_SDK_ROOT=/var/home/nedr/Android/Sdk \
  ./gradlew :watchface:assembleDebug
```

## Regenerate Watch Face XML

```sh
python3 tools/generate_watchface.py
```

## Regenerate Release Assets

```sh
python3 tools/generate_release_assets.py
```

## Validate WFF

```sh
java -jar tools/wff-validator.jar 2 watchface/src/main/res/raw/watchface.xml
```
