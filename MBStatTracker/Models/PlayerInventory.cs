using System;
using Assets.Scripts.Inventory__Items__Pickups.Items;
using Assets.Scripts.Inventory__Items__Pickups.Weapons;
using Assets.Scripts.Inventory__Items__Pickups.Stats;
using Assets.Scripts._Data.Tomes;
using Assets.Scripts.Menu.Shop;
using Logger = MBStatTracker.Utils.Logger;

namespace MBStatTracker.Models

{
	public class PlayerInventoryManager
	{
		public static Il2CppSystem.Collections.Generic.Dictionary<EItem, ItemBase> itemInventory;
		public static Il2CppSystem.Collections.Generic.Dictionary<EWeapon, WeaponBase> weaponInventory;
		public static Il2CppSystem.Collections.Generic.Dictionary<ETome, int> tomeInventory;
		public static Il2CppSystem.Collections.Generic.Dictionary<EStat, Il2CppSystem.Collections.Generic.List<StatModifier>> statInventory;


		public static void InitializeInventories()
		{
			try
			{
				var playerInventory = GameManager.Instance?.GetPlayerInventory();
				if (playerInventory == null)
				{
					Logger.Warn("PlayerInventory is null — maybe not initialized yet?");
					return;
				}

				itemInventory = playerInventory.itemInventory.items;
				weaponInventory = playerInventory.weaponInventory.weapons;
				tomeInventory = playerInventory.tomeInventory.tomeLevels;
				statInventory = playerInventory.statInventory.permanentChanges;

				Logger.Info("[MB Stat Tracker] ✅ Player inventories initialized successfully.");
			}
			catch (Exception ex)
			{
				Logger.Error($"Error initializing inventories: {ex}");
			}
		}

		public static System.Collections.Generic.Dictionary<string, object> GetAllInventoriesAsDictionary()
		{
			var result = new System.Collections.Generic.Dictionary<string, object>();

			try
			{
				// --- Items ---
				var itemsDict = new System.Collections.Generic.Dictionary<string, float>();
				if (itemInventory != null)
				{
					foreach (var kvp in itemInventory)
					{
						string itemName = kvp.Key.ToString() ?? "UnknownItem";
						var item = kvp.Value;


						itemsDict[itemName] = item.amount;
					}
				}
				result["items"] = itemsDict;

				// --- Weapons ---
				var weaponsDict = new System.Collections.Generic.Dictionary<string, int>();
				if (weaponInventory != null)
				{
					foreach (var kvp in weaponInventory)
					{
						string weaponName = kvp.Key.ToString() ?? "UnknownWeapon";
						var weapon = kvp.Value;
						weaponsDict[weaponName] = weapon.level;
					}
				}
				result["weapons"] = weaponsDict;

				// --- Tomes ---
				var tomesDict = new System.Collections.Generic.Dictionary<string, int>();
				if (tomeInventory != null)
				{
					foreach (var kvp in tomeInventory)
					{
						string tomeName = kvp.Key.ToString() ?? "UnknownTome";
						tomesDict[tomeName] = kvp.Value;
					}
				}
				result["tomes"] = tomesDict;

				// --- Stats ---
				var statsDict = new System.Collections.Generic.Dictionary<string, Il2CppSystem.Collections.Generic.List<string>>();
				if (statInventory != null)
				{
					foreach (var kvpObj in statInventory)
					{
						Il2CppSystem.Collections.Generic.List<StatModifier> statModifidierList = (Il2CppSystem.Collections.Generic.List<StatModifier>)kvpObj.GetType().GetProperty("value")?.GetValue(kvpObj);

						foreach (var statModifier in statModifidierList)
						{
							EStat stat = statModifier.stat;
							EStatModifyType modifyType = statModifier.modifyType;
							float modification = statModifier.modification;
							Logger.Info($"🧩 Processing statModifier: {statModifier}");
							Logger.Info($"=> Stat: {stat}");
							Logger.Info($"=> Modification Type: {modifyType}");
							Logger.Info($"=> Modification: {modification}");

						}
					}
				}
				else
				{
					Logger.Warn("⚠️ permanentChanges dictionary is null!");
				}

				// Store it into your result object (for serialization)
				result["stats"] = statsDict;


			}
			catch (Exception ex)
			{
				Logger.Error($"Error building inventory dictionary: {ex}");
			}

			return result;
		}
	}
}
