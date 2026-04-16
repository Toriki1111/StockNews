import yfinance as yf
from datetime import datetime, timedelta
from analyzer import add_indicators, get_signal
import time
import os

import yfinance.shared as shared
shared._column_name_map = {}
# List of sectors and their corresponding stock tickers
WATCHLIST = {
    "Defense": ["LMT", "RTX", "NOC"],
    "Energy": ["XOM", "CVX", "COP"],
    "Tech": ["TSLA", "AAPL", "MSFT", "GOOGL"],
    "Finance": ["JPM", "BAC", "GS"],
    "Precious Metals": ["GC=F", "SI=F", "GOLD"]
}

def get_multi_sector_data():
    now_utc = datetime.utcnow()
    now_vn = now_utc + timedelta(hours=7)
    
    timestamp = now_vn.strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 📊 Global Market Update - {timestamp}\n\n"
    content += "| Sector | Ticker | Price (USD) | Change (%) | Status |\n"
    content += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for sector, tickers in WATCHLIST.items():
        print(f"Processing Sector: {sector}")
        for symbol in tickers:
            try:
                # Thay vì dùng fast_info, ta tải bảng dữ liệu 1 tháng
                df = yf.download(symbol, period="60d", interval="1d", progress=False)
                
                if not df.empty:
                    # Gửi bảng này qua file analyzer để tính toán
                    df = add_indicators(df)
                    latest = df.iloc[-1] # Dòng mới nhất
                    prev = df.iloc[-2]   # Dòng ngày hôm trước
                    
                    current_price = latest['Close']
                    # Tính % thay đổi dựa trên giá đóng cửa hôm trước
                    change_pc = ((current_price - prev['Close']) / prev['Close']) * 100
                    
                    # Lấy status từ hàm get_signal bạn đã viết
                    status_signal = get_signal(latest)
                    
                    icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
                    display_symbol = symbol.replace("=F", "")
                    
                    # Thêm status_signal vào cột cuối cùng của bảng
                    content += f"| {sector} | **{display_symbol}** | ${current_price:,.2f} | {change_pc:+.2f}% | {status_signal} {icon} |\n"
                
                time.sleep(1)
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                content += f"| {sector} | **{symbol}** | Error fetching data |\n"
                
    return content

if __name__ == "__main__":
    new_report = get_multi_sector_data()
    file_name = "autocommit.txt"
    temp_file = "latest_news.tmp"
    # Important: create file for discord
    with open(temp_file, "w", encoding="utf-8") as tmp:
        tmp.write(new_report)

    # Đọc dữ liệu cũ và giới hạn số dòng
    old_content = ""
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            # Read maximum 1000 lines in log
            lines = file.readlines()
            old_content = "".join(lines[:1000]) 

    # Over write file : [Dữ liệu mới] + [Dữ liệu cũ đã cắt bớt]
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(new_report + "\n" + "-"*40 + "\n\n" + old_content)
        
    print(f"Successfully updated {file_name}. Log rotated to keep it lightweight.")

