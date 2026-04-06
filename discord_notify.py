import requests
import os

def send_to_discord():
    # Bước 1: Lấy Webhook URL từ biến môi trường (GitHub Secrets)
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("❌ Error: DISCORD_WEBHOOK_URL is not set in GitHub Secrets.")
        return

    # Bước 2: Đọc nội dung báo cáo mới nhất từ file tạm
    temp_file = "latest_news.tmp"
    if not os.path.exists(temp_file):
        print(f"⚠️ Warning: {temp_file} not found. Nothing to send.")
        return

    with open(temp_file, "r", encoding="utf-8") as f:
        report_content = f.read()

    # Bước 3: Chuẩn bị dữ liệu gửi đi (Dưới dạng Embed cho đẹp)
    payload = {
        "username": "Market Guardian Bot",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/1553/1553155.png",
        "content": "🔔 **Cập nhật thị trường mới nhất đây!**",
        "embeds": [{
            "title": "📊 Daily Global Market Report",
            "description": report_content,
            "color": 5814783, # Màu tím Blurple của Discord
            "timestamp": os.path.getmtime(temp_file), # Lấy thời gian tạo file
            "footer": {
                "text": "Dữ liệu được cập nhật tự động qua GitHub Actions",
                "icon_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
            }
        }]
    }

    # Bước 4: Gửi request tới Discord
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("✅ Successfully sent notification to Discord!")
        else:
            print(f"❌ Failed to send: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    send_to_discord()