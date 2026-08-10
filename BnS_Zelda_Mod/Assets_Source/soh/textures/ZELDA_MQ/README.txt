OOT Community Texture Pack Installation
=========================================

1. Download the pack from:
   - GitHub: https://github.com/henriqueloureiro/oot-community-texture-pack
   - ModDB: https://www.moddb.com/mods/oot-community-texture-pack
   - Or Google "OOT Community Texture Pack v1.0"

2. Extract the ZIP - you should see folders like:
   - characters/
   - environments/
   - items/
   - ui/
   - sky/
   - fonts/

3. Copy ALL extracted folders into this directory:
   ~/Shipwright/soh/assets/custom/textures/ZELDA_MQ/

4. Rebuild SoH:
   cd ~/Shipwright && cmake --build build --target soh

5. Copy new build to desktop:
   cp ~/Shipwright/build/soh/soh.elf ~/Desktop/"Legend of Zelda, The - Ocarina of Time - Master Quest (USA) (GameCube)"/soh
   cp -r ~/Shipwright/build/soh/assets ~/Desktop/"Legend of Zelda, The - Ocarina of Time - Master Quest (USA) (GameCube)"/

Folder structure should look like:
ZELDA_MQ/
├── characters/
│   ├── link/
│   ├── navi/
│   └── ...
├── environments/
│   ├── kokiri_forest/
│   └── ...
├── items/
├── ui/
├── sky/
└── fonts/

NOTE: Game ID for Master Quest may be different. If textures don't load,
check the console output for the actual Game ID when running SoH.
