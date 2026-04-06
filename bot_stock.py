from vnstock3 import Vnstock
from datetime import datetime
import time

# Danh sách các mã họ P bạn đang theo dõi
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
            # Sử dụng Vnstock để lấy dữ liệu từ nguồn VND (VNDIRECT)
            stock = Vnstock().stock(symbol=symbol, source='VND')
            
            # Lấy bảng giá lịch sử gần nhất (5 ngày gần đây để đảm bảo có dữ liệu)
            df = stock.quote.history(start='2026-04-01', end='2026-04-06')
            
            if not df.empty:
                # iloc[-1] lấy dòng cuối cùng (phiên gần nhất)
                last_price = df.iloc[-1]['close'] * 1000
                content += f"| **{symbol}** | {last_price:,.0f} | VNDIRECT | ✅ |\n"
            else:
                content += f"| **{symbol}** | N/A | No Data | ❓ |\n"
            
            # Nghỉ 1 giây giữa các lần gọi để tránh bị nghi ngờ là bot spam
            time.sleep(1)
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            content += f"| **{symbol}** | Error | {str(e)[:20]}... | ⚠️ |\n"
            
    return content

if __name__ == "__main__":
    # 1. Lấy dữ liệu chứng khoán
    report_content = get_market_data()
    
    # 2. Ghi vào file nhật ký autocommit.txt
    # Chế độ 'a' (append) giúp bạn giữ lại lịch sử các ngày trước đó
    try:
        with open("autocommit.txt", "a", encoding="utf-8") as f:
            f.write(report_content + "\n---\n")
        print("Successfully updated autocommit.txt")
    except Exception as e:
        print(f"File writing error: {e}")
