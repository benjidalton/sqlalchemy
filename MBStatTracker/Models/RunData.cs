using System;
using System.Collections.Generic;
using System.Text.Json;

namespace MBStatTracker.Models
{
	public class RunData
	{
		public string RunId { get; set; }
		public DateTime Timestamp { get; set; }
		public string Character { get; set; }
		public string Map { get; set; }
		public bool Win { get; set; }

		public float TotalDamage { get; set; }
		public int EnemiesKilled { get; set; }
		public int LevelReached { get; set; }

		public Dictionary<string, float> Items { get; set; } = new();
		public Dictionary<string, int> Weapons { get; set; } = new();
		public Dictionary<string, int> Tomes { get; set; } = new();
		public Dictionary<string, List<Dictionary<string, object>>> Stats { get; set; } = new();
		public Dictionary<string, float> DamageBySource { get; set; } = new();
		public Dictionary<string, float> RunStats { get; set; } = new();

		// Add any other session-specific info you want:
		// public List<string> ItemsCollected { get; set; } = new();

		public RunData()
		{
			RunId = Guid.NewGuid().ToString();
			Timestamp = DateTime.UtcNow;
		}

		/// <summary>
		/// Convert this RunData instance into a formatted JSON string.
		/// </summary>
		public string ToJson(bool indented = true)
		{
			var options = new JsonSerializerOptions
			{
				WriteIndented = indented
			};
			return JsonSerializer.Serialize(this, options);
		}
	}
}
