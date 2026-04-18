plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.nedrichards.fuzzytimegb"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.nedrichards.fuzzytimegb"
        minSdk = 33
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = false
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}
