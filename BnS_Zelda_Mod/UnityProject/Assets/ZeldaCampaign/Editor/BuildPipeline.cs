using UnityEngine;
using UnityEditor;
using UnityEditor.Build.Reporting;
using System.IO;

namespace ZeldaCampaign
{
    public static class BuildPipeline
    {
        [MenuItem("ZeldaCampaign/Build Quest Mod")]
        public static void BuildQuestMod()
        {
            string modDir = "/home/tehlappy/🜏 Lilith/BnS_Zelda_Mod/Mods/ZeldaCampaign";
            string buildDir = Path.Combine(modDir, "Build");
            string bundlesDir = Path.Combine(modDir, "bundles");
            
            Directory.CreateDirectory(buildDir);
            Directory.CreateDirectory(bundlesDir);
            
            // Build asset bundles for Quest (Android ARM64)
            BuildAssetBundles(bundlesDir);
            
            // Build the mod DLL
            BuildModDLL(modDir);
            
            // Create mod package
            CreateModPackage(modDir, buildDir);
            
            Debug.Log("[ZeldaCampaign] Build complete!");
        }
        
        private static void BuildAssetBundles(string outputPath)
        {
            Debug.Log($"[ZeldaCampaign] Building asset bundles to {outputPath}");
            
            var buildParams = new AssetBundleBuildParams
            {
                assetBundleNames = new string[] { "zelda_campaign" },
                assetNames = GetAssetsToBundle(),
                outputPath = outputPath,
                targetPlatform = BuildTarget.Android,
                compression = AssetBundleCompression.LZ4,
                options = BuildAssetBundleOptions.None
            };
            
            AssetBundleBuild build = new AssetBundleBuild
            {
                assetBundleName = "zelda_campaign",
                assetNames = buildParams.assetNames,
                addressableNames = new string[] { "zelda_campaign" }
            };
            
            BuildPipeline.BuildAssetBundles(outputPath, new[] { build }, BuildAssetBundleOptions.None, BuildTarget.Android);
        }
        
        private static string[] GetAssetsToBundle()
        {
            // Return list of assets to include in bundle
            // Prefabs, materials, textures, audio clips, etc.
            return new string[]
            {
                "Assets/ZeldaCampaign/Prefabs",
                "Assets/ZeldaCampaign/Resources",
                "Assets/ZeldaCampaign/Levels"
            };
        }
        
        private static void BuildModDLL(string modDir)
        {
            Debug.Log("[ZeldaCampaign] Building mod DLL...");
            
            // This would normally use csc or dotnet build
            // For Unity mods, the DLL is built by Unity's script compilation
            // We just need to ensure the scripts compile
        }
        
        private static void CreateModPackage(string modDir, string buildDir)
        {
            Debug.Log("[ZeldaCampaign] Creating mod package...");
            
            // Copy id.modio to build dir
            File.Copy(Path.Combine(modDir, "id.modio"), Path.Combine(buildDir, "id.modio"), true);
            
            // Create mod.zip for mod.io upload
            string zipPath = Path.Combine(buildDir, "ZeldaCampaign_v1.0.0.zip");
            if (File.Exists(zipPath)) File.Delete(zipPath);
            
            System.Diagnostics.Process.Start("zip", $"-r \"{zipPath}\" \"{modDir}/ZeldaCampaign.dll\" \"{modDir}/bundles/\" \"{modDir}/id.modio\"").WaitForExit();
        }
    }
}