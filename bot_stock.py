import requests
import time  # <--- Bước 1: Import thư viện thời gian
from datetime import datetime

stocks = ["BSR", "PVT", "PVC"]

def get_live_stock_with_delay():
    url = "https://wgateway-iboard.ssi.com.vn/api/v1/Board/stock/list"
    payload = {"stockSymbols": stocks}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Bước 2: Thêm một khoảng nghỉ ngắn trước khi bắt đầu request (giả lập người dùng)
    print("Bot đang khởi động, chờ 3 giây...")
    time.sleep(3) 
    
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 📊 Stock Report - {now}\n\n"
    content += "| Ticker | Price (VND) | Change (%) | Status |\n| :--- | :--- | :--- | :--- |\n"
    
    try:
        print(f"Đang gửi yêu cầu lấy dữ liệu cho: {', '.join(stocks)}...")
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        
        # Bước 3: Nghỉ thêm 2 giây sau khi nhận phản hồi để xử lý dữ liệu từ tốn
        time.sleep(2)
        
        response.raise_for_status()
        data = response.json().get('data', [])
        
        if not data:
            content += "| - | No data returned from SSI | - | ❓ |\n"
        
        for item in data:
            symbol = item.get('ss')
            price = item.get('l', 0) * 1000 
            change_pc = item.get('cp', 0)
            icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
            content += f"| **{symbol}** | {price:,.0f} | {change_pc}% | {icon} |\n"
            
    except Exception as e:
        content += f"| Error | Connection Issue | - | ⚠️ |\n"
        print(f"Lỗi: {str(e)}")
        
    return content

if __name__ == "__main__":
    report = get_live_stock_with_delay()
    with open("autocommit.txt", "a", encoding="utf-8") as f:
        f.write(report + "\n---\n")
    print("Đã cập nhật file thành công!")
