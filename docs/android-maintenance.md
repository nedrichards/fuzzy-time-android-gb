# Android maintenance

Weekly Dependabot pull requests report obsolete Gradle dependencies and GitHub Actions. Kotlin/KSP and AndroidX updates are grouped for coherent review; upgrades still require passing checks. A dedicated main-branch workflow submits resolved dependencies to GitHub for vulnerability alerts. Dependency review blocks high-severity runtime vulnerabilities. The Watch Face Format validator and generated-asset checks cover this resource-only app.

Run the same verification locally with the project wrapper:

```sh
./gradlew --no-daemon :watchface:lintDebug :watchface:lintRelease :watchface:assembleDebug :watchface:assembleRelease
```

Pull requests, main pushes and manual runs retain test/lint reports and debug/release APKs for 14 days. Debug APKs are installable. Release APKs exercise the release configuration and shrinking; they may be unsigned or debug-signed, as determined by the app's existing signing configuration. They are not production distribution artifacts.

Pushing a `v*` tag runs verification and creates a **draft development release** with explicitly labelled debug APKs and SHA-256 checksums. CI uses a disposable debug key, so installing over another build may require uninstalling it first. Review the draft before publishing. Production releases require the existing app-specific version code/name and production keystore procedure; never publish debug APKs as production-signed builds. No keystore or service credentials are needed by these workflows.

Reports upload even when verification fails. Device interaction still requires device/emulator testing when relevant; JVM tests and lint do not establish device behavior.
