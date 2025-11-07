using BepInEx;
using BepInEx.Logging;
using BepInEx.Unity.IL2CPP;
using HarmonyLib;

namespace MBStatTracker.Plugin
{
	[BepInPlugin("MBStatTracker", "MB Stat Tracker", "1.2.0")]
	public class MBStatTrackerPlugin : BasePlugin
	{
		public new static ManualLogSource Log;
		private Harmony _harmony;

		public override void Load()
		{
			Log = base.Log;
			Utils.Logger.Initialize(Log);
			Log.LogInfo("MBStatTracker loaded!");
			_harmony = new Harmony("MBStatTracker");
			_harmony.PatchAll();
		}

		public override bool Unload()
		{
			_harmony?.UnpatchSelf();
			return true;
		}
	}
}
