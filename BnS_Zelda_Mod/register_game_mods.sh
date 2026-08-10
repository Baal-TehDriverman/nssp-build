#!/bin/bash
# Register + redeploy ZeldaCampaign & SSJFlight into the game's mod.io backing
# system so the mod manager recognizes them and copies them into Mods/.
#
# Ground truth from the game log:
#  - The manager prunes Mods/<name> that have no backing install in
#    mod.io/3852/mods/<id>_<install>/<ModName>/. (ZeldaCampaign/SSJFlight were dropped.)
#  - SuperSaiyanTransformations survived only because id 5029348 has backing (Pilots).
#  - Manifest GameVersion must be 1.0.0.0 (0.12.0.0 / others get rejected).
#
# We create a backing dir for each mod under a unique (fake) id space, give it a
# valid 1.0.0.0 manifest, then ALSO place the manifest-fixed version into Mods/.
set -e
export S=340YC10GC70GST
BNS=/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files
MODS="/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods"

fix_manifest () {  # $1=mod dir on laptop
  python3 - "$1" <<'PY'
import json,sys
p=sys.argv[1]+"/manifest.json"
d=json.load(open(p))
d["GameVersion"]="1.0.0.0"
d["Name"]=d.get("Name","Mod")
d.setdefault("Author","Lilith / Baal-TehDriverman")
d.setdefault("ModVersion","1.0.0")
d.setdefault("Thumbnail","")
json.dump(d,open(p,"w"),indent=2)
print("  manifest fixed ->",d["Name"],"GameVersion 1.0.0.0")
PY
}

echo "===== Fix manifests (GameVersion 1.0.0.0) ====="
# Only fix the two that were PRUNED. Do NOT touch SuperSaiyanTransformations —
# it survived on the Quest (id 5029348 riding Pilots' backing); leave it intact.
for m in ZeldaCampaign SSJFlight; do
  fix_manifest "$MODS/$m"
done

echo ""
echo "===== Copy manifest-fixed mods into BOTH Mods/ and a backing install ====="
declare -A BACK  # name -> registry key
BACK[ZeldaCampaign]="7000001_101"
BACK[SSJFlight]="7000002_102"

for NAME in ZeldaCampaign SSJFlight; do
  SRC="$MODS/$NAME"
  DEST="$BNS/Mods/$NAME"
  BACKDIR="$BNS/mod.io/3852/mods/${BACK[$NAME]}/$NAME"
  echo "--- $NAME ---"
  adb -s $S shell "mkdir -p '$DEST' '$BACKDIR'"
  # push into Mods/
  (cd "$SRC" && find . -type f \( -name '*.json' -o -name '*.dll' -o -name '*.cs' -o -name '*.png' \) | while read -r rel; do
    d=$(dirname "$rel" | sed 's/^\.//'); [ -n "$d" ] && [ "$d" != "." ] && adb -s $S shell "mkdir -p '$DEST$d' '$BACKDIR$d'" 2>/dev/null
    adb -s $S push "$rel" "$DEST$d/" >/dev/null 2>&1
    adb -s $S push "$rel" "$BACKDIR$d/" >/dev/null 2>&1
  done)
  echo "  Mods/$NAME: $(adb -s $S shell "find '$DEST' -type f | wc -l" | tr -d '\r') files"
  echo "  backing ${BACK[$NAME]}: $(adb -s $S shell "find '$BACKDIR' -type f | wc -l" | tr -d '\r') files"
done

echo ""
echo "===== Done. Restart the game or refresh Mod Manager so it re-installs from backing. ====="