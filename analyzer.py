import pandas as pd
import pandas_ta as ta

def add_indicators(df):
    if df.empty:
        return df

    # CAlculate RSI
    # Notice : yfinance return column is 'Close', have to make sure things working fine
    close_prices = df['Close']
    df['RSI'] = ta.rsi(close_prices, length=14)
    
    # calculate EMA 20
    df['EMA_20'] = ta.ema(close_prices, length=20)
    
    return df

def get_signal(row):
    # Check if RSI is NaN (usually happen in first 14 lines of the data)
    if pd.isna(row.get('RSI')):
        return "N/A (Chờ dữ liệu)"
        
    rsi_val = row['RSI']
    
    if rsi_val > 70:
        return "⚠️ Overbought"
    elif rsi_val < 30:
        return "✅ Oversold"
    
    return "Neutral"
