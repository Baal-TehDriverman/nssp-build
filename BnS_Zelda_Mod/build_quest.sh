#!/bin/bash
# B&S Quest Mod Build Pipeline for Zelda Campaign
# Requires Unity 2021.3 LTS with Android Build Support (ARM64)

set -e

MOD_DIR="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign"
UNITY_PROJECT="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/UnityProject"
UNITY_EXECUTABLE="${UNITY_EXECUTABLE:-/opt/unity/editor/Unity}"  # Set via env or install
BUILD_DIR="$MOD_DIR/Build"
BUNDLES_DIR="$MOD_DIR/bundles"

echo "=== Building Zelda Campaign for Quest (Android ARM64) ==="
echo "Mod dir: $MOD_DIR"
echo "Unity: $UNITY_EXECUTABLE"

# Verify Unity exists
if [ ! -f "$UNITY_EXECUTABLE" ]; then
    echo "ERROR: Unity not found at $UNITY_EXECUTABLE"
    echo "Install Unity Hub + Unity 2021.3 LTS with Android Build Support"
    echo "Then set UNITY_EXECUTABLE=/path/to/Unity"
    exit 1
fi

# Create Unity project if not exists
if [ ! -d "$UNITY_PROJECT" ]; then
    echo "Creating Unity project at $UNITY_PROJECT..."
    "$UNITY_EXECUTABLE" -batchmode -createProject "$UNITY_PROJECT" -projectVersion 2021.3.28f1 -quit
fi

# Copy mod scripts to Unity project
mkdir -p "$UNITY_PROJECT/Assets/ZeldaCampaign/Scripts"
cp "$MOD_DIR/ZeldaCampaign.cs" "$UNITY_PROJECT/Assets/ZeldaCampaign/Scripts/"
cp "$MOD_DIR/id.modio" "$UNITY_PROJECT/Assets/ZeldaCampaign/"

# Copy any asset bundles from mod directory
if [ -d "$BUNDLES_DIR" ] && [ "$(ls -A $BUNDLES_DIR)" ]; then
    mkdir -p "$UNITY_PROJECT/Assets/StreamingAssets/Bundles"
    cp -r "$BUNDLES_DIR/"* "$UNITY_PROJECT/Assets/StreamingAssets/Bundles/"
fi

# Build for Android (Quest ARM64)
echo "Building for Android ARM64 (Quest)..."
mkdir -p "$BUILD_DIR"

"$UNITY_EXECUTABLE" \
    -batchmode \
    -projectPath "$UNITY_PROJECT" \
    -buildTarget Android \
    -executeMethod ZeldaCampaign.BuildPipeline.BuildQuestMod \
    -outputPath "$BUILD_DIR/ZeldaCampaign_Quest.apk" \
    -quit \
    -logFile - \
    -stackTraceLogType Full

if [ $? -eq 0 ]; then
    echo "=== Build successful ==="
    echo "APK: $BUILD_DIR/ZeldaCampaign_Quest.apk"
    echo "Deploying to Quest..."
    adb -s 340YC10GC70GST install -r "$BUILD_DIR/ZeldaCampaign_Quest.apk"
    echo "=== Deployed to Quest ==="
else
    echo "=== Build failed ==="
    exit 1
fi