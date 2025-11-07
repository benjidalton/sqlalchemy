using System;
using Assets.Scripts.Inventory__Items__Pickups.Items;
using Assets.Scripts.Inventory__Items__Pickups.Weapons;
using Assets.Scripts.Inventory__Items__Pickups.Stats;
using Assets.Scripts._Data.Tomes;
using Assets.Scripts.Menu.Shop;
using Il2CppSystem.Collections.Generic;
using Assets.Scripts.Actors;
using Logger = MBStatTracker.Utils.Logger;


namespace MBStatTracker.Models
{
    public static class RunManager
    {
        public static RunData CurrentRun { get; private set; }

        public static void StartNewRun(string character, string map)
        {
            CurrentRun = new RunData
            {
                Character = character,
                Map = map
            };

            Logger.Info($"🎬 Started new run: {CurrentRun.RunId} ({character} on {map})");
        }

        public static void EndRun(bool win)
        {
            if (CurrentRun == null)
            {
                Logger.Warn("⚠️ Tried to end a run, but no active run exists!");
                return;
            }

            CurrentRun.Win = win;
            Logger.Info($"🏁 Run ended — Win: {win}, Total Damage: {CurrentRun.TotalDamage:F1}");
        }

        public static void AddDamage(DamageContainer dc)
        {
            if (CurrentRun == null)
            {
                Logger.Warn("⚠️ Damage recorded before run started!");
                return;
            }

            string source = dc.damageSource?.ToString() ?? "Unknown";
            float damage = dc.damage;

            if (!CurrentRun.DamageBySource.ContainsKey(source))
                CurrentRun.DamageBySource[source] = 0;

            CurrentRun.DamageBySource[source] += damage;
            CurrentRun.TotalDamage += damage;
        }

        public static string ToJson(bool indented = true)
        {
            if (CurrentRun == null)
                return "{}";

            return CurrentRun.ToJson(indented);
        }

        public static void UpdateRunDataFromInventories(
            Dictionary<EItem, ItemBase> itemInventory,
            Dictionary<EWeapon, WeaponBase> weaponInventory,
            Dictionary<ETome, int> tomeInventory,
            Dictionary<EStat, List<StatModifier>> statInventory)
        {
            if (CurrentRun == null)
            {
                Logger.Error("❌ RunData instance is null — cannot update inventories.");
                return;
            }

            try
            {
                // --- Items ---
                if (itemInventory != null)
                {
                    CurrentRun.Items.Clear();
                    foreach (var kvp in itemInventory)
                    {
                        string itemName = kvp.Key.ToString() ?? "UnknownItem";
                        try
                        {
                            float amount = kvp.Value.amount;
                            CurrentRun.Items[itemName] = amount;
                        }
                        catch (Exception ex)
                        {
                            Logger.Warn($"⚠️ Failed to read item '{itemName}': {ex.Message}");
                        }
                    }
                }

                // --- Weapons ---
                if (weaponInventory != null)
                {
                    CurrentRun.Weapons.Clear();
                    foreach (var kvp in weaponInventory)
                    {
                        string weaponName = kvp.Key.ToString() ?? "UnknownWeapon";
                        try
                        {
                            int level = kvp.Value.level;
                            CurrentRun.Weapons[weaponName] = level;
                        }
                        catch (Exception ex)
                        {
                            Logger.Warn($"⚠️ Failed to read weapon '{weaponName}': {ex.Message}");
                        }
                    }
                }

                // --- Tomes ---
                if (tomeInventory != null)
                {
                    CurrentRun.Tomes.Clear();
                    foreach (var kvp in tomeInventory)
                    {
                        string tomeName = kvp.Key.ToString() ?? "UnknownTome";
                        int level = kvp.Value;
                        CurrentRun.Tomes[tomeName] = level;
                    }
                }

                // --- Stats ---
                if (statInventory != null)
                {
                    CurrentRun.Stats.Clear();

                    foreach (var kvpObj in PlayerInventoryManager.statInventory)
                    {
                        // Reflect out the List<StatModifier>
                        var statModifierList = (Il2CppSystem.Collections.Generic.List<StatModifier>)
                            kvpObj.GetType().GetProperty("value")?.GetValue(kvpObj);

                        if (statModifierList == null)
                        {
                            Logger.Warn("⚠️ statModifierList is null — skipping.");
                            continue;
                        }

                        foreach (var statModifier in statModifierList)
                        {
                            EStat stat = statModifier.stat;
                            EStatModifyType modifyType = statModifier.modifyType;
                            float modificationAmount = statModifier.modification;

                            Logger.Info($"🧩 Processing statModifier: {statModifier}");
                            Logger.Info($"=> Stat: {stat}");
                            Logger.Info($"=> Modification Type: {modifyType}");
                            Logger.Info($"=> Modification: {modificationAmount}");

                            // Convert enum key to string for JSON serialization safety
                            string statKey = stat.ToString();

                            // Ensure the stat exists in the dictionary
                            if (!CurrentRun.Stats.ContainsKey(statKey))
                                CurrentRun.Stats[statKey] = new System.Collections.Generic.List<System.Collections.Generic.Dictionary<string, object>>();

                            // Add the modifier as an object to that stat’s list
                            var modifierData = new System.Collections.Generic.Dictionary<string, object>();
                            modifierData.Add("type", modifyType.ToString());
                            modifierData.Add("amount", modificationAmount);

                            ((System.Collections.Generic.List<System.Collections.Generic.Dictionary<string, object>>)CurrentRun.Stats[statKey]).Add(modifierData);
                        }
                    }

                    Logger.Info("✅ Finished processing all stat modifiers!");
                    Logger.Info($"📊 Total Stats Recorded: {CurrentRun.Stats.Count}");
                }

            }
            catch (Exception ex)
            {
                Logger.Error($"❌ Error updating RunData inventories: {ex}");
            }
        }
    }
}
