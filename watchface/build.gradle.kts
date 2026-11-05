plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.nedrichards.fuzzytimegb"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.nedrichards.fuzzytimegb"
        minSdk = 34
        targetSdk = 35
        versionCode = 2
        versionName = "1.0.1"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = false
            signingConfig = signingConfigs.getByName("debug")
        }
        create("play") {
            initWith(getByName("release"))
            signingConfig = null
            matchingFallbacks += "release"
        }
        create("developer") {
            initWith(getByName("release"))
            applicationIdSuffix = ".dev"
            signingConfig = signingConfigs.getByName("debug")
            matchingFallbacks += "release"
        }
    }
}
