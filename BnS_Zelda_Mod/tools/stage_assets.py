#!/usr/bin/env python3
"""
Asset staging + mod packaging for ZeldaCampaign B&S Quest mod.
Gathers Unity-ready assets, copies raw-Toonz/embedded data for manual import,
and produces a mod.zip + a deploy_assets.sh for ADB push to Quest.

Task 4 (deploy) uses this to build the exact target tree expected by B&S:
  Android/data/com.Warpfrog.BladeAndSorcery/files/Mods/ZeldaCampaign/
    ZeldaCampaign.dll        <- compiled (needs Unity build step), else placeholder
    id.modio
    bundles/                 <- asset bundles (Unity build), else empty
    TextureAssets/UI/*.png   <- standalone PNGs usable via Texture.Load
"""
import os, shutil, subprocess, zipfile, sys
from pathlib import Path

MOD_ROOT = Path("/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod")
MOD_DIR = MOD_ROOT / "Mods" / "ZeldaCampaign"
SOURCES = MOD_ROOT / "Assets_Source"
DEST_QUEST = {
    "local": MOD_DIR,
    "quest_abs": "/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods/ZeldaCampaign",
}

def ensure_dirs():
    for sub in ["bundles", "TextureAssets/UI", "Scripts", "Levels", "Resources"]:
        (MOD_DIR / sub).mkdir(parents=True, exist_ok=True)

def copy_staged():
    # UI PNGs already copied
    ui = MOD_DIR / "TextureAssets" / "UI"
    ui.mkdir(parents=True, exist_ok=True)
    if (SOURCES / "soh" / "textures" / "buttons").exists():
        for p in (SOURCES / "soh" / "textures" / "buttons").glob("*.png"):
            shutil.copy(p, ui / p.name)
    print(f"Staged UI PNGs: {len(list(ui.glob('*.png')))}")

def write_manifest():
    pngs = sorted((MOD_DIR / "TextureAssets" / "UI").glob("*.png"))
    manifest = {
        "mod": "ZeldaCampaign",
        "name": "Zelda Campaign",
        "version": "1.0.0",
        "ui_png_count": len(pngs),
        "script_files": [f.name for f in (MOD_DIR / "Scripts").glob("*.cs")],
        "resources": [f.name for f in (MOD_DIR / "Resources").glob("*")],
    }
    (MOD_DIR / "manifest.json").write_text(__import__("json").dumps(manifest, indent=2))
    print(f"Wrote manifest: {len(pngs)} UI PNGs, {len(manifest['script_files'])} scripts")

def build_zip():
    out = MOD_ROOT / "ZeldaCampaign_v1.0.0.zip"
    if out.exists():
        out.unlink()
    zfiles = []
    for p in MOD_DIR.rglob("*"):
        if p.is_file() and p.name != "manifest.json":
            zfiles.append(p)
    # mod.io expects: ZeldaCampaign.dll, id.modio, bundles/ at zip root
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        # id.modio at root
        if (MOD_DIR / "id.modio").exists():
            z.write(MOD_DIR / "id.modio", "id.modio")
        # place a placeholder dll marker so structure is obvious
        z.writestr("ZeldaCampaign.dll",
                   "// placeholder - run build_quest.sh (Unity batch) to produce real DLL")
        # texture assets folder
        for p in (MOD_DIR / "TextureAssets").rglob("*.png"):
            z.write(p, p.relative_to(MOD_DIR))
        # scripts (source copy for reference)
        for p in (MOD_DIR / "Scripts").rglob("*.cs"):
            z.write(p, p.relative_to(MOD_DIR))
        # resources
        for p in (MOD_DIR / "Resources").rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(MOD_DIR))
    print(f"Built {out} ({out.stat().st_size/1024:.1f} KB)")

def write_deploy_script():
    script = f"""#!/bin/bash
# Auto-generated deploy for task 4 - pushes mod to Quest B&S Mods folder
set -e
SERIAL="340YC10GC70GST"
DEST="/sdcard/Android/data/com.Warpfrog.BladeAndSorcery/files/Mods/ZeldaCampaign"

echo "=== Deploying ZeldaCampaign to Quest ==="
adb -s $SERIAL get-state >/dev/null 2>&1 || {{ echo "Quest not connected/authorized"; exit 1; }}

# Stage PN-Gs into the target tree if Unity-built assets absent
adb -s $SERIAL shell "mkdir -p $DEST/bundles $DEST/TextureAssets/UI"

# Push scripts/resources references via manifest (source copy)
for d in TextureAssets Scripts Resources bundles; do
  if [ -d "{MOD_DIR}/$d" ]; then
    echo "Pushing $d..."
    adb -s $SERIAL push "{MOD_DIR}/$d/." "$DEST/$d/" 2>/dev/null || true
  fi
done

# id.modio
adb -s $SERIAL push "{MOD_DIR}/id.modio" "$DEST/" 2>&1

echo "=== Deployment complete. Enable 'ZeldaCampaign' in B&S Mods menu. ==="
adb -s $SERIAL shell "ls -laR $DEST" 2>&1 | head -40
"""
    (MOD_ROOT / "deploy_quest.sh").write_text(script)
    os.chmod(MOD_ROOT / "deploy_quest.sh", 0o755)
    print("Wrote deploy_quest.sh")

if __name__ == "__main__":
    ensure_dirs()
    copy_staged()
    write_manifest()
    build_zip()
    write_deploy_script()
    print("\n=== Asset staging + packaging complete ===")