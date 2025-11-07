using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using MBStatTracker.Models;

namespace MBStatTracker.Utils
{
    public static class Api
    {
        public static async Task SendRunDataAsync(RunData run)
        {
            using var client = new HttpClient();

            string json = run.ToJson(false); // compact JSON for network efficiency
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            try
            {
                var response = await client.PostAsync("http://127.0.0.1:8000/megabonk/submit", content);
                response.EnsureSuccessStatusCode();

                Logger.Info($"✅ Run data successfully sent! Status: {response.StatusCode}");
            }
            catch (Exception ex)
            {
                Logger.Error($"❌ Failed to send run data: {ex.Message}");
            }
        }
    }
}
