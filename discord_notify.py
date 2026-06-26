import requests
import os
from datetime import datetime

ROLE_Stock = "1520029320847036547" #ID of the role in discord not important if you tend not to change @mention 

PING_Mention_Stock = f"<@&{ROLE_Stock}>"

def send_to_discord():
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL") #github SECRETS
    temp_file = "latest_news.tmp"
    
    if not webhook_url:
        print("❌ Error: DISCORD_WEBHOOK_URL not set.")
        return

    if not os.path.exists(temp_file):
        print(f"⚠️ Warning: {temp_file} not found.")
        return

    with open(temp_file, "r", encoding="utf-8") as f:
        report_content = f.read()

    payload = {
        "content": f"{PING_Mention_Stock} 🔔 **UPDATED NEWEST US STOCK!**",
        "embeds": [{
            "title": "📊 DAILY USA MARKET REPORT",
            "description": report_content,
            "color": 5814783,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": "Automated via GitHub Actions"}
        }]
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("✅ Discord Notification Sent!")
    else:
        print(f"❌ Failed: {response.status_code}")

if __name__ == "__main__":
    send_to_discord()
