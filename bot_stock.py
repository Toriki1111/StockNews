from vnstock import Vnstock 
from datetime import datetime
import time

# Danh sách các mã họ P bạn quan tâm
STOCKS = ["BSR", "PVT", "PVC"]

def get_market_data():
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 📊 Market Update - {now}\n\n"
    content += "| Ticker | Price (VND) | Source | Status |\n"
    content += "| :--- | :--- | :--- | :--- |\n"
    
    print(f"Starting bot at {now}...")
    
    for symbol in STOCKS:
        try:
            print(f"Fetching data for {symbol}...")
            # Sử dụng thư viện vnstock mới nhất
            stock = Vnstock().stock(symbol=symbol, source='VND')
            
            # Lấy dữ liệu lịch sử gần nhất
            df = stock.quote.history(start='2026-04-01', end='2026-04-06')
            
            if not df.empty:
                # Lấy giá đóng cửa dòng cuối cùng và nhân 1000
                last_price = df.iloc[-1]['close'] * 1000
                content += f"| **{symbol}** | {last_price:,.0f} | VNDIRECT | ✅ |\n"
            else:
                content += f"| **{symbol}** | N/A | No Data | ❓ |\n"
            
            time.sleep(1) # Nghỉ 1s giữa các mã
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            content += f"| **{symbol}** | Error | {str(e)[:20]}... | ⚠️ |\n"
            
    return content

if __name__ == "__main__":
    # Lấy dữ liệu
    report_content = get_market_data()
    
    # Ghi vào file log
    try:
        with open("autocommit.txt", "a", encoding="utf-8") as f:
            f.write(report_content + "\n---\n")
        print("Update successful!")
    except Exception as e:
        print(f"File error: {e}")
