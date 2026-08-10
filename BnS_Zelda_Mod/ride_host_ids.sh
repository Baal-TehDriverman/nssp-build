#!/bin/bash
# Make ZeldaCampaign + SSJFlight persist by riding an APPROVED host mod's mod.io id,
# exactly like SuperSaiyanTransformations does (it survives by sharing Pilots' id 5029348).
#
# Pattern proven to work: a SEPARATE folder in Mods/<Name> whose id.modio references an
# approved (backed) mod.io id. The game keeps it because the id is recognized.
#
# ZeldaCampaign -> DBmapPackNOMAD (6259354, Cell Games arena = campaign host)
# SSJFlight      -> WaterSpell     (5692226, jetpack = flight host)
set -e
export S=340YC10GC70GST
BNS="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files"
MODS="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods"

# id.modio keyed to the host mod's approved id
cat > "$MODS/ZeldaCampaign/id.modio" <<'EOF'
{"id":6259354,"lastChecked":"2026-08-08T17:00:00.000Z","dependencies":[]}
EOF
cat > "$MODS/SSJFlight/id.modio" <<'EOF'
{"id":5692226,"lastChecked":"2026-08-08T17:00:00.000Z","dependencies":[]}
EOF
echo "id.modio set: ZeldaCampaign rides 6259354 (DBmapPack), SSJFlight rides 5692226 (WaterSpell)"

# Deploy folders into Mods/ + into the host's backing install dir so it's backed too
for NAME in ZeldaCampaign SSJFlight; do
  # host backing dir depends on mod
  case "$NAME" in
    ZeldaCampaign) HOSTBACK="$BNS/mod.io/3852/mods/6259354_8042579$NAME" ;;
    SSJFlight)     HOSTBACK="$BNS/mod.io/3852/mods/5692226_7434725$NAME" ;;
  esac
  echo "--- $NAME ---"
  ./deploy_mod.sh "$S" "$MODS/$NAME" "$BNS/Mods" "$NAME"
  # also drop a copy inside the host's backing install dir (so the manager sees it backed)
  adb -s $S shell "mkdir -p '$HOSTBACK'" 2>/dev/null
  ./deploy_mod.sh "$S" "$MODS/$NAME" "$(dirname "$HOSTBACK")" "$(basename "$HOSTBACK")"
done

echo ""
echo "===== Verify persistence setup ====="
for m in ZeldaCampaign SSJFlight; do
  id=$(adb -s $S shell "cat '$BNS/Mods/$m/id.modio' 2>/dev/null" | grep -oE '[0-9]+' | head -1)
  echo "  $m: $(adb -s $S shell "find '$BNS/Mods/$m' -type f | wc -l" | tr -d '\r') files, id=$id"
done