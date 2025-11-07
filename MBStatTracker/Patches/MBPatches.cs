using HarmonyLib;
using Assets.Scripts.Actors;
using Assets.Scripts.Actors.Enemies;
using Assets.Scripts.Saves___Serialization.Progression.Stats;
using MBStatTracker.Utils;
using MBStatTracker.Models;

namespace MBStatTracker.Patches
{

	// Harmony looks for HarmonyPatch to either PreFix or PostFix your code
	// to bind to an event from the game
	[HarmonyPatch(typeof(PlayerRenderer))]
	[HarmonyPatch(nameof(PlayerRenderer.SetCharacter))] // Choose character
	public class SetCharacterPatch
	{
		public static void Postfix(CharacterData characterData, PlayerInventory inventory)
		{
			string characterName = characterData?.name ?? "UnknownCharacter";
			string mapName = "UnknownMap";
			RunManager.StartNewRun(characterName, mapName);
			PlayerInventoryManager.InitializeInventories();
		}
	}

	[HarmonyPatch(typeof(Enemy))]
	[HarmonyPatch(nameof(Enemy.Damage))] // Enemy taking damage
	public class EnemyDamagePatch
	{
		public static void Postfix(DamageContainer __0)
		{
			RunManager.AddDamage(__0);
		}
	}

	[HarmonyPatch(typeof(PlayerRenderer))]
	[HarmonyPatch(nameof(PlayerRenderer.OnDeath))] // Player Death
	public class PlayerDeathPatch
	{
		public static void Postfix()
		{
			RunManager.UpdateRunDataFromInventories(
				PlayerInventoryManager.itemInventory,
				PlayerInventoryManager.weaponInventory,
				PlayerInventoryManager.tomeInventory,
				PlayerInventoryManager.statInventory
			);
			foreach (var kvp in RunStats.stats)
			{
				RunManager.CurrentRun.RunStats[kvp.Key] = kvp.Value;
			}
			_ = Api.SendRunDataAsync(RunManager.CurrentRun);
		}
	}
}
