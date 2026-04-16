import requests
import os
import json
import time

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    # Dùng Gemini 1.5 Flash cho nhẹ và tiết kiệm quota
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"Summarize this stock data in 3 professional sentences: {market_data}"}]}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        
        # Xử lý lỗi 429 - Quá tải
        if response.status_code == 429:
            return "\n*(AI Error 429: Rate limit exceeded. Please wait 1 minute before trying again.)*\n"
            
        if response.status_code != 200:
            return f"\n*(AI Error {response.status_code}: {response.text})*\n"

        result = response.json()
        advice_text = result['candidates'][0]['content']['parts'][0]['text']
        return f"\n---\n### 🤖 AI Financial Advisor:\n\n{advice_text}"

    except Exception as e:
        return f"\n*(Connection Error: {str(e)})*\n"