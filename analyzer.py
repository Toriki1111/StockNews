import pandas as pd

def add_indicators(df):
    if df.empty:
        return df
    # close Col 
    close = df['Close']
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    # calculate EMA 20
    df['EMA_20'] = close.ewm(span=20, adjust=False).mean()
    return df

def get_signal(row):
    # check if RSI is NaN (e.g., not enough data to calculate)
    if pd.isna(row.get('RSI')):
        return "Grinding"
        
    rsi_val = row['RSI']
    if rsi_val > 70:
        return "⚠️ Overbought!"
    elif rsi_val < 30:
        return "✅ Oversale"
    return "Stable"
