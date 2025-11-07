using System.Reflection;

namespace MBStatTracker.Utils
{
	public static class ObjectDumper
	{
		public static void DumpObject(object obj, string label = null)
		{
			if (obj == null)
			{
				Logger.Warn($"[{label ?? "Object"}] is null");
				return;
			}

			var type = obj.GetType();
			Logger.Info($"\n\n--- Dumping object of type: {type.FullName} ---");

			foreach (var prop in type.GetProperties(BindingFlags.Public | BindingFlags.Instance))
			{
				try
				{
					var value = prop.GetValue(obj, null);
					Logger.Info($"PROP {prop.Name} = {value}");
				}
				catch { }
			}

			foreach (var field in type.GetFields(BindingFlags.Public | BindingFlags.Instance))
			{
				try
				{
					var value = field.GetValue(obj);
					Logger.Info($"FIELD {field.Name} = {value}");
				}
				catch { }
			}
		}
	}
}
