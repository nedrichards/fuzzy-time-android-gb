# Continuous integration

Actions use immutable action revisions, read-only repository permissions by
default, bounded jobs, cancellation of obsolete development runs, and grouped
Dependabot action updates. Workflow syntax and shell snippets are checked with
checksum-pinned actionlint on native x86_64 and aarch64 runners. Dependency repair
jobs retain their existing narrowly scoped write access and trusted generators.

Tested development artifacts are for review, with source provenance and checksums;
diagnostics are retained even when tests fail. Reports and captures must use
fixtures, never account credentials, personal data or hardware identifiers.
Where a release workflow is configured, it attests verified files and prepares
drafts for manual publication. Native Flatpak release packaging requires both targets. CI signing establishes
build provenance; it does not replace release signing or human acceptance.

Watch Face Format generation and exhaustive time/resource contracts run on native x86_64 and aarch64. Android builds retain lint, WFF and memory validation. Generated previews are retained for review. This resource-only watch face does not have an application instrumentation journey.

Workflow syntax and shell snippets are checked locally before publication. Hosted
execution provides the architecture and installed-artifact evidence; generated
captures still require human visual review. No release or tag is created by this
maintenance change.
