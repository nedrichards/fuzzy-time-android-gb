plugins {
    alias(libs.plugins.android.application) apply false
}

// Patch AGP's build-only transitive dependencies until upstream carries the fixes.
// Keep the Bouncy Castle family aligned; none of these libraries ship in the face.
buildscript {
    configurations.classpath {
        resolutionStrategy.eachDependency {
            when {
                requested.group == "com.google.guava" && requested.name == "guava" ->
                    useVersion("33.7.2-jre")
                requested.group == "org.bouncycastle" -> useVersion("1.85")
                requested.group == "org.jetbrains.kotlin" -> useVersion("2.4.21")
            }
        }
    }
}
