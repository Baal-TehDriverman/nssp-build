#!/bin/bash
# Master deploy — deploys ALL our B&S Quest mods in the correct order.
set -e
export S=340YC10GC70GST
ROOT="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods"
BNS="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods"

echo "===== Deploying ALL custom B&S Quest mods ====="
adb -s $S get-state >/dev/null 2>&1 || { echo "Quest not connected/authorized"; exit 1; }

deploy_mod () {
    local NAME="$1"
    local SRC="$ROOT/$NAME"
    local DEST="$BNS/$NAME"
    echo "--- Deploying $NAME ---"
    adb -s $S shell "mkdir -p '$DEST'"
    # Push ALL relevant mod files
    (cd "$SRC" && find . -type f \( \
        -name '*.json' -o \
        -name '*.dll' -o \
        -name '*.cs' -o \
        -name '*.png' -o \
        -name '*.bundle' -o \
        -name '*.hash' -o \
        -name '*.modio' \
    \) | while IFS= read -r rel; do
        dir=$(dirname "$rel" | sed 's/^\.//')
        if [ -n "$dir" ] && [ "$dir" != "." ]; then
            adb -s $S shell "mkdir -p '$DEST$dir'" 2>/dev/null
        fi
        adb -s $S push "$rel" "$DEST$dir/" >/dev/null 2>&1
    done)
    echo "  $NAME pushed: $(adb -s $S shell "find $DEST -type f | wc -l" | tr -d '\r') files"
}

# Deploy ALL 4 custom mods
deploy_mod ZeldaCampaign
deploy_mod SuperSaiyanTransformations
deploy_mod SSJFlight
deploy_mod LithosphereLootPack

echo ""
echo "===== Final on-Quest mod inventory ====="
for m in ZeldaCampaign SuperSaiyanTransformations SSJFlight LithosphereLootPack; do
    echo "  $m: $(adb -s $S shell "find $BNS/$m -type f | wc -l" | tr -d '\r') files"
done
echo ""
echo "===== ALL B&S mods now ====="
adb -s $S shell "ls $BNS/" 2>&1 | tr '\n' ' '
echo ""
echo "===== Enable in-game (order): Pilots Super Sayan Spell, WaterSpell, BlackFire, DBmapPackNOMAD, ZeldaCampaign, SuperSaiyanTransformations, SSJFlight, LithosphereLootPack. Restart. ====="
