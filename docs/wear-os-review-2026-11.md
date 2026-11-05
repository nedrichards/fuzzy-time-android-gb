# Wear OS watch face review — 5 November 2026

## Recommendation

Keep the resource-only WFF architecture and current visual design. There is no
identified reason to rewrite the renderer or add executable watch code. Nick's
reported good Pixel Watch 2 performance is useful real-device evidence; this
review makes no new battery or frame-time claims.

Integrate the reviewed Gradle 9.8.2 and Android Gradle Plugin 9.5.0 PRs. These
are build-tool updates, not watch-runtime features.

## Compatibility

- `android:hasCode="false"`, no runtime dependencies or native libraries, and
  separate declarative resources match the current WFF packaging model. The
  resource-only APK has no 32-bit native-code migration to perform.
- WFF v2 and minSdk 34 match Wear OS 5. Keep this floor while no newer WFF
  feature is needed. Google's setup guide explicitly recommends the lowest
  format version supporting the required features.
- targetSdk/compileSdk 35 meet the Wear OS submission requirement effective
  August 2026. Do not apply the phone-app API 36 requirement to this face.
- WFF release notes now cover v5, including more text layout controls. V3 adds
  text auto-sizing and v4 adds ambient transitions and photos. None is needed
  for the current fixed British-English phrases; a format bump alone is not a
  performance improvement.

Sources: [WFF setup](https://developer.android.com/training/wearables/wff/setup),
[WFF versions](https://developer.android.com/training/wearables/wff),
[release notes](https://developer.android.com/training/wearables/wff/release-notes),
[Play target API requirements](https://support.google.com/googleplay/android-developer/answer/11926878).

## Recommended follow-ups

1. **Add memory and ambient-illumination validation before the next release.**
   CI currently validates XML syntax and runs lint/builds, but has no memory
   footprint evaluator or AOD illumination gate. Ambient text is smaller, dimmer,
   normal-weight, on black, with complication arcs hidden: sensible choices.
   They do not establish compliance with the 10 MB ambient / 100 MB interactive
   budgets or the 15% AOD illumination limit across the day. Run Google's tools
   over both fonts and colour settings. Preserve the quiet ambient design.
2. **Harden complication arithmetic.** `render_range_complication()` divides by
   `MAX - MIN` and by `GOAL_PROGRESS_TARGET_VALUE` without guarding zero. Range
   progress is not clamped; goal progress has only an upper bound. Guard invalid
   denominators and clamp progress to [0, 1]. Validate zero targets, equal bounds,
   negative/over-target values, empty data and provider changes on a watch.
3. **Add explicit spoken time labels and test TalkBack.** The generator labels
   font choices, but emits no `ScreenReader` elements for its time groups.
   Prefer one coherent time announcement per visible time group; verify reading
   order and complication announcements in active and ambient modes. ScreenReader
   is supported without raising the WFF version.
4. **Replace draft listing assets before Play submission.** `store_icon()` draws
   the words “Fuzzy / Time GB”, which are not displayed by the face. Since July
   2026 WO-G4 requires the actual circular face to reach the icon edges and
   prohibits unrelated text/graphics. Existing preview/screenshots are synthetic
   drafts and show only the top arc although the current face has two slots.
   Capture current output, including both font choices and complication settings;
   don't treat these draft illustrations as device-rendering evidence.
5. **Test small and large round devices before changing layout.** Check long
   phrases in both fonts, editor previews, both complication tap targets, minute
   boundaries, midnight/noon, timezone changes, and ambient transitions. No device
   was attached during this review. Lint and schema validation cannot prove text
   fit or touch/accessibility behaviour.

Sources: [quality requirements WO-P7/P8, WO-G4/G6](https://developer.android.com/docs/quality-guidelines/wear-app-quality),
[memory guidance and evaluator](https://developer.android.com/training/wearables/wff/memory-usage),
[ScreenReader](https://developer.android.com/reference/wear-os/wff/common/screen-reader).

## Optional maintenance

The generated XML is 2,053,756 bytes, below the documented 10 MB source limit,
with 936 condition expressions and 3,721 text parts. One generic system-font
branch per time bucket duplicates the explicitly selected system-font branch.
Consider removing that duplication only with output-equivalence checks and
real-device verification; XML size alone is not evidence of runtime slowness.
Moving complication nodes after time nodes follows Google's layering guidance,
but should be assessed with the memory evaluator before claiming a saving.

The build still carries AGP 9 migration compatibility switches in
`gradle.properties`. Remove these separately after checking defaults and builds;
this resource-only app does not need a Kotlin/Compose migration. Production
release signing/versioning remains a separate task: the release build currently
uses the debug signing configuration, as already documented.

## Validation scope

The bundled validator accepts the regenerated XML as WFF v2. Regenerating XML
and release assets produces no tracked changes. Both PR heads had successful
GitHub build and dependency-review checks before local integration. The integrated
Gradle 9.8.2 / AGP 9.5.0 combination passed `lintDebug`, `lintRelease`,
`assembleDebug` and `assembleRelease` locally with JDK 21. No physical
watch, emulator, TalkBack session, memory evaluation or battery benchmark was
run for this review. The recommendations above are pending work, not implemented
runtime changes or certification of Play compliance.
