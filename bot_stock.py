import yfinance as yf
import pandas as pd
from ai_advisor import get_ai_advice
from datetime import datetime, timedelta
from analyzer import add_indicators, get_signal
import time
import os

import yfinance.shared as shared
shared._column_name_map = {}
# List of sectors and their corresponding stock tickers
WATCHLIST = {
    "Military": ["LMT", "RTX", "NOC"],
    "Energy": ["XOM", "CVX", "COP"],
    "Tech": ["TSLA", "AAPL", "MSFT", "GOOGL"],
    "Finance": ["JPM", "BAC", "GS"],
    "Precious Metals": ["GC=F", "SI=F", "GOLD"]
}

def get_multi_sector_data():
    now_utc = datetime.utcnow()
    now_vn = now_utc + timedelta(hours=7)
    
    timestamp = now_vn.strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 📊 USA Market Update - {timestamp}\n\n"
    content += "| Sector | Ticker | Price (USD) | Change (%) | Status |\n"
    
    for sector, tickers in WATCHLIST.items():
        print(f"Processing Sector: {sector}")
        for symbol in tickers:
            try:
                # Thay vì dùng fast_info, ta tải bảng dữ liệu 60 days
                df = yf.download(symbol, period="60d", interval="1d", progress=False)
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                    
                if not df.empty:
                    # sending this to file analyzer to calculate indicators and get signal
                    df = add_indicators(df)
                    latest = df.iloc[-1] # Dòng mới nhất
                    prev = df.iloc[-2]   # Dòng ngày hôm trước
                    
                    current_price = latest['Close']
                    # calculating percentage change from previous close to current price
                    change_pc = ((current_price - prev['Close']) / prev['Close']) * 100
                    
                    # Get signal from analyzer based on indicators
                    status_signal = get_signal(latest)
                    
                    icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
                    display_symbol = symbol.replace("=F", "")
                    
                    # Format the content for Discord
                    content += f"| {sector} | **{display_symbol}** | ${current_price:,.2f} | {change_pc:+.2f}% | {status_signal} {icon} |\n"
                
                time.sleep(1)
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                content += f"| {sector} | **{symbol}** | Error fetching data |\n"
                
    return content

if __name__ == "__main__":
    new_report = get_multi_sector_data()

    #IMPORTANT: If you dont want to use AI advice, delete the line below and change full_content_with_ai to full_content_with_ai = new_report in the 2nd code below
    ai_advice = get_ai_advice(new_report)
    full_content_with_ai = new_report + "\n" + ai_advice 

    file_name = "daily_stock_report.txt"
    temp_file = "latest_news.tmp"
    # Important: create file for discord to read, then we can safely rotate logs without worrying about file locks or read/write conflicts
    with open(temp_file, "w", encoding="utf-8") as tmp:
        tmp.write(full_content_with_ai)

    # Read old datas and limit lines
    old_content = ""
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            # Read maximum 1000 lines in log
            lines = file.readlines()
            old_content = "".join(lines[:1000]) 

    # Over write file : [Dữ liệu mới] + [Dữ liệu cũ đã cắt bớt]
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(full_content_with_ai + "\n" + "-"*40 + "\n\n" + old_content)
        
    print(f"Successfully updated {file_name}. Log rotated to keep it lightweight.")

