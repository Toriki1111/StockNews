import pandas as pd

def add_indicators(df):
    if df.empty:
        return df
    
    # Đảm bảo dữ liệu là số
    close = df['Close']
    
    # 1. Tự tính RSI (Công thức chuẩn)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 2. Tự tính EMA 20
    df['EMA_20'] = close.ewm(span=20, adjust=False).mean()
    
    return df

def get_signal(row):
    # Kiểm tra nếu RSI là NaN
    if pd.isna(row.get('RSI')):
        return "Tích lũy"
        
    rsi_val = row['RSI']
    if rsi_val > 70:
        return "⚠️ Quá mua"
    elif rsi_val < 30:
        return "✅ Quá bán"
    return "Ổn định"
