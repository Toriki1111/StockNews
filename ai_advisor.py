import requests
import os
import json
import time

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}

    prompt_text = (
        f"You are a professional International Financial Advisor. Analyze this market data: {market_data}\n\n"
        f"Provide a concise, actionable report in English using exactly 3 bullet points (1-2 sentences per point):\n"
        f"1. **Market Trend**: Identify where the money is flowing or exiting based on sector performance.\n"
        f"2. **Key Tickers to Watch**: Highlight 1-2 specific symbols with notable technical signals (e.g., Oversold, Overbought, or major price surges/drops) and why.\n"
        f"3. **Actionable Strategy**: Give clear, direct trading advice (e.g., Accumulate, Take Profit, Stop Loss, or Wait & Watch) for the upcoming session."
    )

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt_text
            }]
        }]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        
        if response.status_code == 429:
            return "\n*(AI Error 429: Rate limit exceeded. Please wait 1 minute before trying again.)*\n"
        if response.status_code != 200:
            return f"\n*(AI Error {response.status_code}: {response.text})*\n"
        if response.status_code == 503:
            return get_ai_advise()
            
        result = response.json()
        advice_text = result['candidates'][0]['content']['parts'][0]['text']
        return f"\n---\n### AI Financial Advisor:\n\n{advice_text}"

    except Exception as e:
        return f"\n*(Connection Error: {str(e)})*\n"
