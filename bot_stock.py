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
    "Precious Metals": ["GC=F", "SI=F", "GOLD"]
}

def fetch_yahoo_direct(symbol):
    try:
        # Giả lập như đang mở bằng trình duyệt Chrome trên máy tính để tránh bị Yahoo bann 401
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # store 1 month of data for AI analyze
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1mo&interval=1d"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return pd.DataFrame()
            
        data = response.json()
        result = data['chart']['result'][0]
        
        timestamps = result['timestamp']
        indicators = result['indicators']['quote'][0]
        
        df = pd.DataFrame({
            'Open': indicators['open'],
            'High': indicators['high'],
            'Low': indicators['low'],
            'Close': indicators['close'],
            'Volume': indicators['volume']
        }, index=pd.to_datetime(timestamps, unit='s'))
        
        # rid of empty space give out clean board
        return df.dropna().tail(60)
    except:
        return pd.DataFrame()

def get_multi_sector_data():
    now_vn = datetime.utcnow() + timedelta(hours=7)
    timestamp = now_vn.strftime('%d/%m/%Y %H:%M:%S')
    
    content = f"### 📊 USA Market Update - {timestamp}\n\n"
    content += "| Sector | Ticker | Price (USD) | Change (%) | Status |\n"
    
    for sector, tickers in WATCHLIST.items():
        print(f"Processing Sector: {sector}")
        for symbol in tickers:
            try:
                df = fetch_yahoo_direct(symbol)
                    
                if not df.empty and 'Close' in df.columns:
                    df = add_indicators(df)
                    latest = df.iloc[-1] 
                    prev = df.iloc[-2]   
                    
                    current_price = latest['Close']
                    change_pc = ((current_price - prev['Close']) / prev['Close']) * 100
                    
                    status_signal = get_signal(latest)
                    icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
                    
                    content += f"| {sector} | **{symbol}** | ${current_price:,.2f} | {change_pc:+.2f}% | {status_signal} {icon} |\n"
                else:
                    content += f"| {sector} | **{symbol}** | Data Error | 0.00% | Stable 🟡 |\n"
                
                time.sleep(1) #delay
                
            except Exception as e:
                print(f"❌ Lỗi xử lý mã {symbol}: {e}")
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
        
    print(f"Successfully updated {file_name}. Log updated via direct Yahoo alternative.")
