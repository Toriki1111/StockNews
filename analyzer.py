import pandas_ta as ta

def add_indicators(df):
    # Đảm bảo dữ liệu không trống
    if df.empty:
        return df
    
    # Tính RSI (Chỉ số sức mạnh tương đối)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    
    # Tính EMA 20 (Đường trung bình động lũy thừa)
    df['EMA_20'] = ta.ema(df['Close'], length=20)
    
    return df

def get_signal(row):
    # Logic đưa ra lời khuyên dựa trên chỉ số
    if row['RSI'] > 70:
        return "⚠️ Overbought (Quá mua)"
    elif row['RSI'] < 30:
        return "✅ Oversold (Quá bán)"
    return "Neutral (Ổn định)"