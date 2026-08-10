#!/bin/bash
# Quick start script for Zelda Campaign mod development

set -e

MOD_ROOT="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod"

echo "=== Zelda Campaign Mod - Quick Start ==="
echo ""

# Check Unity
if [ -z "$UNITY_EXECUTABLE" ]; then
    echo "UNITY_EXECUTABLE not set. Checking common locations..."
    for path in \
        "/opt/unity/editor/Unity" \
        "/Applications/Unity/Hub/Editor/*/Unity" \
        "$HOME/Unity/Hub/Editor/*/Unity" \
        "/usr/bin/unity-editor" \
        "/usr/local/bin/unity-editor"; do
        if ls $path 2>/dev/null | head -1 | grep -q Unity; then
            export UNITY_EXECUTABLE=$(ls $path 2>/dev/null | head -1)
            echo "Found Unity: $UNITY_EXECUTABLE"
            break
        fi
    done
fi

if [ -z "$UNITY_EXECUTABLE" ] || [ ! -f "$UNITY_EXECUTABLE" ]; then
    echo ""
    echo "ERROR: Unity not found!"
    echo "Install Unity Hub + Unity 2021.3 LTS with Android Build Support"
    echo "Then run: export UNITY_EXECUTABLE=/path/to/Unity"
    echo ""
    echo "On Arch/Garuda:"
    echo "  paru -S unityhub unity-editor"
    echo "  # Open Unity Hub, install 2021.3.28f1 + Android Build Support"
    echo "  export UNITY_EXECUTABLE=\$(find /opt/unity -name Unity -type f 2>/dev/null | head -1)"
    exit 1
fi

echo "Unity: $UNITY_EXECUTABLE"
echo ""

# Check Quest connection
echo "Checking Quest ADB connection..."
adb -s 340YC10GC70GST get-state > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Quest 3S: Connected (340YC10GC70GST)"
else
    echo "Quest 3S: Not connected or unauthorized"
    echo "Run: adb devices"
    echo "Put on headset and approve USB debugging"
fi
echo ""

# Show menu
echo "Available commands:"
echo "  1) Build mod for Quest     -> ./build_quest.sh"
echo "  2) Deploy mod to Quest     -> ./deploy_quest.sh"
echo "  3) Open Unity Editor       -> \$UNITY_EXECUTABLE -projectPath UnityProject"
echo "  4) View mod structure      -> ls -la Mods/ZeldaCampaign/"
echo "  5) Check Quest mods folder -> adb -s 340YC10GC70GST shell ls /sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods/"
echo ""
echo "Mod root: $MOD_ROOT"