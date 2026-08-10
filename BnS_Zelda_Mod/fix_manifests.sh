#!/bin/bash
# Fix the two just-deployed mods:
#  - proper B&S manifest.json (Name/Description/Author/ModVersion/GameVersion/Thumbnail)
#  - ensure id.modio (registry key) is present
set -e
export S=340YC10GC70GST
BNS="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files"
MODS="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods"

# 1. Write correct manifest.json to laptop mod dirs first
cat > "$MODS/ZeldaCampaign/manifest.json" <<'EOF'
{
  "Name": "Zelda Campaign",
  "Description": "Blade of Hyrule — a full Zelda campaign for B&S Quest. 9 dungeon gauntlets on the Cell Games arena, 37 items, 9 bosses (Gohma to Ganondorf). Wave-based campaign, no Unity required.",
  "Author": "Lilith / Baal-TehDriverman",
  "ModVersion": "1.0.0",
  "GameVersion": "1.0.0.0",
  "Thumbnail": ""
}
EOF
cat > "$MODS/SSJFlight/manifest.json" <<'EOF'
{
  "Name": "SSJ Flight",
  "Description": "Super Saiyan flight — hover/fly/boost, thrust scales with transformation stage. Gravity+base merge to engage.",
  "Author": "Lilith / Baal-TehDriverman",
  "ModVersion": "1.0.0",
  "GameVersion": "1.0.0.0",
  "Thumbnail": ""
}
EOF
echo "laptop manifests fixed"

# 2. Also give SSJFlight a proper id.modio (it may be missing locally too)
cat > "$MODS/SSJFlight/id.modio" <<'EOF'
{"id":7000002,"lastChecked":"2026-08-08T16:40:00.000Z","dependencies":[]}
EOF
cat > "$MODS/ZeldaCampaign/id.modio" <<'EOF'
{"id":7000001,"lastChecked":"2026-08-08T16:40:00.000Z","dependencies":[]}
EOF
echo "laptop id.modio set"

# 3. Push manifest + id.modio into Mods/ and backing for both
for NAME in ZeldaCampaign SSJFlight; do
  for DEST in "$BNS/Mods/$NAME" "$BNS/mod.io/3852/mods/7000001_101/$NAME" "$BNS/mod.io/3852/mods/7000002_102/$NAME"; do
    # only push backing that matches this mod
    case "$DEST" in
      *7000001*ZeldaCampaign|*7000002*SSJFlight|*Mods/$NAME)
        adb -s $S push "$MODS/$NAME/manifest.json" "$DEST/" >/dev/null 2>&1
        adb -s $S push "$MODS/$NAME/id.modio" "$DEST/" >/dev/null 2>&1
        ;;
    esac
  done
done

echo ""
echo "=== Verify ==="
for m in ZeldaCampaign SSJFlight; do
  echo "--- $m manifest ---"; adb -s $S shell "head -c 200 '$BNS/Mods/$m/manifest.json'" 2>&1; echo ""
  adb -s $S shell "test -f '$BNS/Mods/$m/id.modio' && echo '  id.modio OK' || echo '  MISSING id.modio'" 2>&1
done