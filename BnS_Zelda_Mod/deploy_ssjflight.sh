#!/bin/bash
# Deploy SSJ Flight mod to Quest 3S
set -e
export S=340YC10GC70GST
ROOT="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods"
BNS="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods"

echo "=== Deploying SSJ Flight + verifying SuperSaiyanTransformations ==="
adb -s $S get-state >/dev/null 2>&1 || { echo "Quest not connected/authorized"; exit 1; }

MOD="$ROOT/SSJFlight"
DEST="$BNS/SSJFlight"
adb -s $S shell "mkdir -p $DEST/Skills $DEST/Spells $DEST/Effects"
for f in "$MOD"/Skills/*.json; do adb -s $S push "$f" "$DEST/Skills/" >/dev/null 2>&1; done
for f in "$MOD"/Spells/*.json; do adb -s $S push "$f" "$DEST/Spells/" >/dev/null 2>&1; done
for f in "$MOD"/Effects/*.json; do adb -s $S push "$f" "$DEST/Effects/" >/dev/null 2>&1; done
adb -s $S push "$MOD/SSJFlight.dll" "$DEST/" 2>&1 | tail -1
adb -s $S push "$MOD/id.modio" "$DEST/" 2>&1 | tail -1
adb -s $S push "$MOD/manifest.json" "$DEST/" 2>&1 | tail -1

echo "=== SSJFlight deployed: ==="
adb -s $S shell "find $DEST -type f | wc -l" 2>&1

echo "=== SuperSaiyanTransformations still present: ==="
adb -s $S shell "find $BNS/SuperSaiyanTransformations -type f | wc -l" 2>&1

echo "=== ALL B&S mods now: ==="
adb -s $S shell "ls $BNS/" 2>&1 | tr '\n' ' '
echo ""
echo "=== Enable in-game: SSJ Flight + SuperSaiyanTransformations + WaterSpell + Pilots Super Sayan Spell, restart ==="