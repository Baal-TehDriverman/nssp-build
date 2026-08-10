#!/bin/bash
# Auto-generated deploy for task 4 - pushes mod to Quest B&S Mods folder
set -e
SERIAL="340YC10GC70GST"
DEST="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods/ZeldaCampaign"

echo "=== Deploying ZeldaCampaign to Quest ==="
adb -s $SERIAL get-state >/dev/null 2>&1 || { echo "Quest not connected/authorized"; exit 1; }

# Stage PN-Gs into the target tree if Unity-built assets absent
adb -s $SERIAL shell "mkdir -p $DEST/bundles $DEST/TextureAssets/UI"

# Push scripts/resources references via manifest (source copy)
for d in TextureAssets Scripts Resources bundles; do
  if [ -d "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign/$d" ]; then
    echo "Pushing $d..."
    adb -s $SERIAL push "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign/$d/." "$DEST/$d/" 2>/dev/null || true
  fi
done

# id.modio
adb -s $SERIAL push "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign/id.modio" "$DEST/" 2>&1

echo "=== Deployment complete. Enable 'ZeldaCampaign' in B&S Mods menu. ==="
adb -s $SERIAL shell "ls -laR $DEST" 2>&1 | head -40
