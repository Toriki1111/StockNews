import yfinance as yf
from datetime import datetime, timedelta
import time
import os

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
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info
                
                current_price = info['last_price']
                prev_close = info['previous_close']
                change_pc = ((current_price - prev_close) / prev_close) * 100
                
                icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
                display_symbol = symbol.replace("=F", "")
                
                content += f"| {sector} | **{display_symbol}** | ${current_price:,.2f} | {change_pc:+.2f}% | {icon} |\n"
                
                time.sleep(1) #prevent getting block API
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                content += f"| {sector} | **{symbol}** | Error | N/A | ⚠️ |\n"
                
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
