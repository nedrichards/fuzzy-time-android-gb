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
                requested.group == "org.bouncycastle" && requested.name.endsWith("-jdk18on") ->
                    useVersion("1.85")
                requested.group == "org.bitbucket.b_c" && requested.name == "jose4j" ->
                    useVersion("0.9.6")
                requested.group == "org.jdom" && requested.name == "jdom2" ->
                    useVersion("2.0.6.1")
                requested.group == "org.apache.commons" && requested.name == "commons-lang3" ->
                    useVersion("3.18.0")
                requested.group == "org.apache.httpcomponents" && requested.name == "httpclient" ->
                    useVersion("4.5.14")
                requested.group == "org.jetbrains.kotlin" -> useVersion("2.4.21")
            }
        }
    }
}

// Lint resolves its own tool classpath independently of the AGP plugin classpath.
// This resource-only face has no runtime library dependencies.
allprojects {
    configurations.configureEach {
        resolutionStrategy.eachDependency {
            when {
                requested.group == "com.google.guava" && requested.name == "guava" ->
                    useVersion("33.7.2-jre")
                requested.group == "org.bouncycastle" && requested.name.endsWith("-jdk18on") ->
                    useVersion("1.85")
                requested.group == "org.bitbucket.b_c" && requested.name == "jose4j" ->
                    useVersion("0.9.6")
                requested.group == "org.jdom" && requested.name == "jdom2" ->
                    useVersion("2.0.6.1")
                requested.group == "org.apache.commons" && requested.name == "commons-lang3" ->
                    useVersion("3.18.0")
                requested.group == "org.apache.httpcomponents" && requested.name == "httpclient" ->
                    useVersion("4.5.14")
            }
        }
    }
}
