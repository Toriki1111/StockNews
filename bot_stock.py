import requests
from datetime import datetime

stocks = ["BSR", "PVT", "PVC"]

def get_live_stock():
    # Sử dụng API của SSI (iBoard) - thường thân thiện hơn với các dải IP cloud
    url = "https://wgateway-iboard.ssi.com.vn/api/v1/Board/stock/list"
    payload = {"stockSymbols": stocks}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 📊 Stock Report - {now}\n\n"
    content += "| Ticker | Price (VND) | Change (%) | Status |\n| :--- | :--- | :--- | :--- |\n"
    
    try:
        # Gửi request POST đến SSI
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json().get('data', [])
        
        for item in data:
            symbol = item.get('ss') # Ticker
            price = item.get('l', 0) * 1000 # Last price
            change_pc = item.get('cp', 0) # Change percentage
            
            icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
            content += f"| **{symbol}** | {price:,.0f} | {change_pc}% | {icon} |\n"
            
    except Exception as e:
        # Nếu vẫn lỗi, bot vẫn sẽ ghi log để "nhuộm xanh" GitHub nhưng báo lỗi data
        content += f"| Error | Connection issue (SSI) | - | ⚠️ |\n"
        print(f"Log: {str(e)}")
        
    return content

if __name__ == "__main__":
    report = get_live_stock()
    with open("autocommit.txt", "a", encoding="utf-8") as f:
        f.write(report + "\n---\n")
