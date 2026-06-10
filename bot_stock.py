import pandas as pd
from ai_advisor import get_ai_advice
from datetime import datetime, timedelta
from analyzer import add_indicators, get_signal
import time
import os
import requests

WATCHLIST = {
    "Military": ["LMT", "RTX", "NOC"],
    "Energy": ["XOM", "CVX", "COP"],
    "Tech": ["TSLA", "AAPL", "MSFT", "GOOGL"],
    "Finance": ["JPM", "BAC", "GS"],
    "Precious Metals": ["GLD", "SLV", "GOLD"]  
}

API_KEY = "Zs4SH9hyFZuV03aAGq7ZuhDs2i9HJQmC"

def fetch_stock_quote_fmp(symbol):
    """
    Sử dụng endpoint v3/quote (Luôn mở và miễn phí 100% cho gói Free).
    Lấy trực tiếp giá hiện tại và % thay đổi trong ngày từ sàn Mỹ.
    """
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return {
                    "price": data[0].get("price"),
                    "changesPercentage": data[0].get("changesPercentage")
                }
        return None
    except Exception as e:
        print(f"❌ Lỗi kết nối API với mã {symbol}: {e}")
        return None

def get_multi_sector_data():
    now_vn = datetime.utcnow() + timedelta(hours=7)
    timestamp = now_vn.strftime('%d/%m/%Y %H:%M:%S')
    
    content = f"### 📊 USA Market Update - {timestamp}\n\n"
    content += "| Sector | Ticker | Price (USD) | Change (%) | Status |\n"
    
    for sector, tickers in WATCHLIST.items():
        print(f"Processing Sector: {sector}")
        for symbol in tickers:
            try:
                quote = fetch_stock_quote_fmp(symbol)
                    
                if quote and quote["price"] is not None:
                    current_price = quote["price"]
                    change_pc = quote["changesPercentage"]
                    status_signal = "Stable" 
                    try:
                        fake_df = pd.DataFrame([{ 'Close': current_price }])
                        fake_df = add_indicators(fake_df)
                        status_signal = get_signal(fake_df.iloc[-1])
                    except:
                        status_signal = "Stable" 
                    icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
                    display_symbol = "GC" if symbol == "GLD" else "SI" if symbol == "SLV" else symbol
                    
                    content += f"| {sector} | **{display_symbol}** | ${current_price:,.2f} | {change_pc:+.2f}% | {status_signal} {icon} |\n"
                else:
                    content += f"| {sector} | **{symbol}** | API Connection Error | 0.00% | Stable 🟡 |\n"
                
                time.sleep(0.2)
                
            except Exception as e:
                print(f"❌ Lỗi xử lý logic mã {symbol}: {e}")
                content += f"| {sector} | **{symbol}** | Logic Error | 0.00% | Stable 🟡 |\n"
                
    return content

if __name__ == "__main__":
    new_report = get_multi_sector_data()
    
    ai_advice = get_ai_advice(new_report)
    full_content_with_ai = new_report + "\n" + ai_advice 

    file_name = "daily_stock_report.txt"
    temp_file = "latest_news.tmp"
    
    with open(temp_file, "w", encoding="utf-8") as tmp:
        tmp.write(full_content_with_ai)

    old_content = ""
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            old_content = "".join(lines[:1000]) 

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(full_content_with_ai + "\n" + "-"*40 + "\n\n" + old_content)
        
    print(f"Successfully updated {file_name}. Price fetched via FMP Quote API.")
