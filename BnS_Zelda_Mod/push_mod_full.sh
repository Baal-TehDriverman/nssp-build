#!/bin/bash
set -e
export S=340YC10GC70GST
ROOT="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods"
BNS="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods"

push_mod () {
    local NAME="$1"
    local SRC="$ROOT/$NAME"
    local DEST="$BNS/$NAME"
    echo "--- Pushing $NAME ---"
    adb -s $S shell "mkdir -p '$DEST'"
    
    cd "$SRC"
    find . -type f \( \
        -name '*.json' -o \
        -name '*.dll' -o \
        -name '*.cs' -o \
        -name '*.png' -o \
        -name '*.bundle' -o \
        -name '*.hash' -o \
        -name '*.modio' \
    \) | while IFS= read -r rel; do
        # Remove ./ prefix
        rel="${rel#./}"
        dir=$(dirname "$rel")
        if [ "$dir" = "." ] || [ "$dir" = "" ]; then
            adb -s $S push "$rel" "$DEST/" >/dev/null 2>&1
        else
            adb -s $S shell "mkdir -p '$DEST/$dir'" 2>/dev/null
            adb -s $S push "$rel" "$DEST/$dir/" >/dev/null 2>&1
        fi
    done
    count=$(adb -s $S shell "find $DEST -type f | wc -l" | tr -d '\r')
    echo "  $NAME: $count files"
}

push_mod ZeldaCampaign
push_mod SuperSaiyanTransformations
push_mod SSJFlight
push_mod LithosphereLootPack

echo ""
echo "===== Final verification ====="
for m in ZeldaCampaign SuperSaiyanTransformations SSJFlight LithosphereLootPack; do
    echo "  $m: $(adb -s $S shell "find $BNS/$m -type f | wc -l" | tr -d '\r') files"
done
