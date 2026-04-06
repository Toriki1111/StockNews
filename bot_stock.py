from vnstock3 import Vnstock
from datetime import datetime
import time

stocks = ["BSR", "PVT", "PVC"]

def get_stock_data():
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 📊 Market Update - {now}\n\n"
    content += "| Ticker | Price | Change | % |\n| :--- | :--- | :--- | :--- |\n"
    
    try:
        # Khởi tạo vnstock
        for symbol in stocks:
            stock = Vnstock().stock(symbol=symbol, source='VCI') # Hoặc source='TCBS'
            df = stock.quote.history(start='2026-04-01', end='2026-04-06') # Lấy dòng cuối
            
            # Lấy giá đóng cửa gần nhất
            last_price = df.iloc[-1]['close'] * 1000
            content += f"| **{symbol}** | {last_price:,.0f} | Updated | ✅ |\n"
            time.sleep(1) # Nghỉ 1s giữa mỗi mã
            
    except Exception as e:
        content += f"| Error | Data Fetch Failed | {str(e)[:30]}... | ⚠️ |\n"
        
    return content

if __name__ == "__main__":
    report = get_stock_data()
    with open("autocommit.txt", "a", encoding="utf-8") as f:
        f.write(report + "\n---\n")
