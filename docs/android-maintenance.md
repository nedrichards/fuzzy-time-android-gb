# Android maintenance

Weekly Dependabot pull requests report obsolete Gradle dependencies and GitHub Actions. Kotlin/KSP and AndroidX updates are grouped for coherent review; upgrades still require passing checks. A dedicated main-branch workflow submits resolved dependencies to GitHub for vulnerability alerts. Dependency review blocks high-severity runtime vulnerabilities. The Watch Face Format validator and generated-asset checks cover this resource-only app.

Run the same verification locally with the project wrapper:

```sh
./gradlew --no-daemon :watchface:lintDebug :watchface:lintRelease :watchface:assembleDebug :watchface:assembleRelease
```

Pull requests, main pushes and manual runs retain test/lint reports and debug/release APKs for 14 days. Debug APKs are installable. Release APKs exercise the release configuration and shrinking; they use the Android debug/test signing key by design. They are not production distribution artifacts.

Pushing a `v*` tag runs verification and creates a **draft development release** with explicitly labelled debug APKs and SHA-256 checksums. CI uses a disposable debug key, so installing over another build may require uninstalling it first. Review the draft before publishing. Production releases require the existing app-specific version code/name and production keystore procedure; never publish debug APKs as production-signed builds. No keystore or service credentials are needed by these workflows.

Reports upload even when verification fails. Device interaction still requires device/emulator testing when relevant; JVM tests and lint do not establish device behavior.

GitHub dependency review and CodeQL run on public repositories. Private repositories require GitHub Code Security; after enabling it, set repository variable `GH_CODE_SECURITY_ENABLED=true`. Otherwise CI explicitly reports the unavailable checks while Dependabot version updates, vulnerability alerts, dependency submission, tests and lint remain active.


The `release` variant remains test-key signed for developer installation.
`developer` uses the same signing convention with a `.dev` application ID so it
can coexist with another signing key. `play` produces an unsigned App Bundle for
external production signing; building it does not publish anything. Before a
Play submission, assign a new version code/name, sign the bundle with the upload
key, and complete the Play Console listing and device review.

CI also checks all minute/font selections, complication arithmetic, text bounds,
ambient illumination estimates and Google's memory budget. The evaluator is
checksum-pinned in `tools/validate_memory.py`; review the upstream artifact and
license when changing its pin. Build-classpath constraints patch AGP's Guava,
Bouncy Castle and Kotlin dependencies until upstream includes their fixes.
