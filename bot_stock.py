import yfinance as yf
from datetime import datetime
import time

# Dictionary mapping Sectors to their "Big Three" leaders
WATCHLIST = {
    "Energy": ["XOM", "CVX", "COP"],
    "Tech": ["AAPL", "MSFT", "GOOGL"],
    "Finance": ["JPM", "BAC", "GS"],
    "Precious Metals": ["GC=F", "SI=F", "GOLD"],
    "Defense": ["LMT", "RTX", "NOC"] # Lockheed Martin, Raytheon, Northrop Grumman
}

def get_multi_sector_data():
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    content = f"### 📊 Global Market Update - {timestamp}\n\n"
    content += "| Sector | Ticker | Price (USD) | Change (%) | Status |\n"
    content += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for sector, tickers in WATCHLIST.items():
        print(f"Processing Sector: {sector}")
        for symbol in tickers:
            try:
                # Fetch data from Yahoo Finance
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info
                
                current_price = info['last_price']
                prev_close = info['previous_close']
                change_pc = ((current_price - prev_close) / prev_close) * 100
                
                # Visual indicator
                icon = "🟢" if change_pc > 0 else "🔴" if change_pc < 0 else "🟡"
                
                # Clean up symbol names for display
                display_symbol = symbol.replace("=F", "")
                
                content += f"| {sector} | **{display_symbol}** | ${current_price:,.2f} | {change_pc:+.2f}% | {icon} |\n"
                
                time.sleep(1) 
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                content += f"| {sector} | **{symbol}** | Error | N/A | ⚠️ |\n"
                
    return content

if __name__ == "__main__":
    report = get_multi_sector_data()
    with open("autocommit.txt", "a", encoding="utf-8") as file:
        file.write(report + "\n---\n")
    print("Market update with Defense sector complete!")
