using BepInEx.Logging;

namespace MBStatTracker.Utils
{
    public static class Logger
    {
        private static ManualLogSource _logSource;

        /// <summary>
        /// Initializes the logger with the plugin's ManualLogSource.
        /// Call this once from MBStatTrackerPlugin.Load().
        /// </summary>
        public static void Initialize(ManualLogSource logSource)
        {
            _logSource = logSource;
        }

        public static void Info(string message)
        {
            _logSource?.LogInfo(message);
        }

        public static void Warn(string message)
        {
            _logSource?.LogWarning(message);
        }

        public static void Error(string message)
        {
            _logSource?.LogError(message);
        }

        public static void Debug(string message)
        {
            _logSource?.LogDebug(message);
        }
    }
}
