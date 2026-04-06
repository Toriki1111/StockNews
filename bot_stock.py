import requests
from datetime import datetime

# Danh sách các mã bạn quan tâm (Họ P)
stocks = ["BSR", "PVT", "PVC"]

def get_live_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Sử dụng API của VNDIRECT (khá ổn định và không cần key phức tạp)
    url = f"https://finfo-api.vndirect.com.vn/v2/hosts/quotes/symbols?symbols={','.join(stocks)}"
    
    content = f"## 📈 Stock Log - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    content += "| Ticker | Price (VND) | Change (%) |\n|---|---|---|\n"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()['data']
        
        for item in data:
            symbol = item['symbol']
            price = item['lastPrice'] * 1000 # Convert to VND
            change = item['changePc']
            
            # Thêm icon cho trực quan
            icon = "🔴" if change < 0 else "🟢"
            content += f"| **{symbol}** | {price:,.0f} | {icon} {change}% |\n"
            
    except Exception as e:
        content += f"| Error | Failed to fetch data: {str(e)} | - |\n"
    
    return content

if __name__ == "__main__":
    stock_data = get_live_stock()
    # Lưu vào file autocommit.txt (chế độ "a" để cộng dồn hoặc "w" để ghi đè mỗi ngày)
    with open("autocommit.txt", "a", encoding="utf-8") as f:
        f.write(stock_data + "\n---\n")