#!/bin/bash
# Final health check of our 3 custom mods on the Quest.
export S=340YC10GC70GST
BNS="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files"
echo "===== CUSTOM MOD DEPLOYMENT HEALTH CHECK ====="
for m in ZeldaCampaign SSJFlight SuperSaiyanTransformations; do
  echo ""
  echo "=== $m ==="
  echo "  files in Mods/:        $(adb -s $S shell "find '$BNS/Mods/$m' -type f 2>/dev/null | wc -l" | tr -d '\r')"
  echo "  id.modio:              $(adb -s $S shell "test -f '$BNS/Mods/$m/id.modio' && echo OK || echo MISSING" 2>&1 | tr -d '\r')"
  echo "  manifest Name:         $(adb -s $S shell "grep -m1 '\"Name\"' '$BNS/Mods/$m/manifest.json' 2>/dev/null" | tr -d '\r' | xargs)"
  echo "  manifest GameVersion:  $(adb -s $S shell "grep -m1 '\"GameVersion\"' '$BNS/Mods/$m/manifest.json' 2>/dev/null" | tr -d '\r' | xargs)"
  echo "  DLL present:           $(adb -s $S shell "find '$BNS/Mods/$m' -name '*.dll' | wc -l" | tr -d '\r')"
done
echo ""
echo "===== Backing installs present (for manager recognition) ====="
adb -s $S shell "ls '$BNS/mod.io/3852/mods/' " 2>&1 | tr '\n' ' ' | grep -oE '700000[12]_1[01]' | while read b; do echo "  found backing: $b"; done
echo ""
echo "===== ALL mods the manager will see ====="
adb -s $S shell "ls '$BNS/Mods/'" 2>&1 | tr '\n' ' '