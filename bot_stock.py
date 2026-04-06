import yfinance as yf
from datetime import datetime
import time

# Danh sách 3 mã dầu khí lớn nhất sàn Mỹ
STOCKS = ["XOM", "CVX", "COP"]

def get_us_stock_data():
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 🌎 Global Oil Market Update (US) - {now}\n\n"
    content += "| Ticker | Company | Price (USD) | Change (%) | Status |\n"
    content += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    print(f"Starting US Stock bot at {now}...")
    
    for symbol in STOCKS:
        try:
            print(f"Fetching data for {symbol}...")
            # Truy vấn dữ liệu từ Yahoo Finance
            ticker = yf.Ticker(symbol)
            
            # Lấy thông tin giá nhanh (Fast Info)
            info = ticker.fast_info
            current_price = info['last_price']
            prev_close = info['previous_close']
            
            # Tính toán % thay đổi
            change_pc = ((current_price - prev_close) / prev_close) * 100
            
            # Chọn icon theo biến động
            icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
            
            content += f"| **{symbol}** | {symbol} Corp | ${current_price:.2f} | {change_pc:+.2f}% | {icon} |\n"
            
            # Nghỉ 1s để đảm bảo không bị API giới hạn
            time.sleep(1)
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            content += f"| **{symbol}** | Error | N/A | N/A | ⚠️ |\n"
            
    return content

if __name__ == "__main__":
    # 1. Lấy dữ liệu chứng khoán Mỹ
    report_content = get_us_stock_data()
    
    # 2. Ghi vào file autocommit.txt
    try:
        with open("autocommit.txt", "a", encoding="utf-8") as f:
            f.write(report_content + "\n---\n")
        print("Successfully updated autocommit.txt with US data!")
    except Exception as e:
        print(f"File writing error: {e}")
