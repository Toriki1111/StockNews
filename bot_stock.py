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

def fetch_clean_stock_data(symbol):
    try:
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ API báo lỗi hệ thống (Status {response.status_code}) với mã {symbol}")
            return pd.DataFrame()
            
        raw_data = response.json()
        if "historical" not in raw_data or not raw_data["historical"]:
            print(f"⚠️ Không tìm thấy dữ liệu lịch sử của mã {symbol}")
            return pd.DataFrame()
            
        # Chuyển đổi dữ liệu JSON từ API thành bảng DataFrame
        df = pd.DataFrame(raw_data["historical"])
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').set_index('date')
        
        # Đổi tên các cột viết hoa chữ cái đầu để khớp 100% với file analyzer.py của bạn
        df = df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })
        
        # Trả về đúng 60 dòng gần nhất giống y như period="60d" cũ
        return df.tail(60)
        
    except Exception as e:
        print(f"❌ Lỗi kết nối API khi tải mã {symbol}: {e}")
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
                # Lấy dữ liệu sạch từ API FMP
                df = fetch_clean_stock_data(symbol)
                    
                if not df.empty and 'Close' in df.columns:
                    # Truyền dữ liệu vào file analyzer gốc của bạn để tính RSI, MACD...
                    df = add_indicators(df)
                    latest = df.iloc[-1] 
                    prev = df.iloc[-2]   
                    
                    current_price = latest['Close']
                    # Tính toán phần trăm tăng giảm giá đóng cửa
                    change_pc = ((current_price - prev['Close']) / prev['Close']) * 100
                    
                    # Lấy tín hiệu mua/bán (Oversale, Stable...) từ hàm get_signal gốc của bạn
                    status_signal = get_signal(latest)
                    
                    icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
                    
                    # Đổi lại tên hiển thị trên bảng Discord thành GC và SI cho đúng ý bạn
                    display_symbol = "GC" if symbol == "GLD" else "SI" if symbol == "SLV" else symbol
                    
                    content += f"| {sector} | **{display_symbol}** | ${current_price:,.2f} | {change_pc:+.2f}% | {status_signal} {icon} |\n"
                else:
                    content += f"| {sector} | **{symbol}** | API Empty | 0.00% | Stable 🟡 |\n"
                
                # Nghỉ 0.2 giây giữa các mã, API chính thống xử lý cực nhanh không cần sleep lâu
                time.sleep(0.2)
                
            except Exception as e:
                print(f"❌ Lỗi xử lý logic hiển thị mã {symbol}: {e}")
                content += f"| {sector} | **{symbol}** | Logic Error | 0.00% | Stable 🟡 |\n"
                
    return content

if __name__ == "__main__":
    # Luồng xử lý ghi đè và rotate log giữ nguyên kiến trúc lưu trữ của bạn
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
        
    print(f"Successfully updated {file_name}. Bot updated via official API.")
