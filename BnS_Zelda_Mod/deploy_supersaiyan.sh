#!/bin/bash
# Deploy the Super Saiyan Transformations mod to Quest 3S
set -e
export S=340YC10GC70GST
MOD="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/SuperSaiyanTransformations"
DEST="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods/SuperSaiyanTransformations"

echo "=== Deploying Super Saiyan Transformations to Quest ==="
adb -s $S get-state >/dev/null 2>&1 || { echo "Quest not connected/authorized"; exit 1; }

adb -s $S shell "mkdir -p $DEST/Spells $DEST/Effects $DEST/DamageModifiers $DEST/Skills"

# Push each JSON in its subfolder (per-file push avoids the empty-dir pitfall)
for f in "$MOD"/Spells/*.json; do adb -s $S push "$f" "$DEST/Spells/" >/dev/null 2>&1; done
for f in "$MOD"/Effects/*.json; do adb -s $S push "$f" "$DEST/Effects/" >/dev/null 2>&1; done
for f in "$MOD"/DamageModifiers/*.json; do adb -s $S push "$f" "$DEST/DamageModifiers/" >/dev/null 2>&1; done

# Push the compiled DLL + metadata
adb -s $S push "$MOD/SuperSaiyan.dll" "$DEST/" 2>&1 | tail -1
adb -s $S push "$MOD/id.modio" "$DEST/" 2>&1 | tail -1
adb -s $S push "$MOD/manifest.json" "$DEST/" 2>&1 | tail -1

# Verify
echo "=== Deployment tree on Quest ==="
adb -s $S shell "find $DEST -type f | sed 's#$DEST/##'" 2>&1
echo "=== File count ==="
adb -s $S shell "find $DEST -type f | wc -l" 2>&1
echo "=== Enable 'Super Saiyan Transformations' + 'Pilots Super Sayan Spell' in the B&S Mods menu, then restart the game ==="