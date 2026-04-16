import requests
import os
import json

def get_ai_advice(market_data):
    # 1. Lấy API Key từ GitHub Secrets
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found in environment)*\n"

    # 2. Đường dẫn chuẩn của Google (Ép dùng v1 - Stable)
    # Chúng ta gọi thẳng vào endpoint mà không qua SDK nào cả
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # 3. Cấu hình Header
    headers = {
        "Content-Type": "application/json"
    }
    
    # 4. Cấu hình Body dữ liệu (JSON Payload) theo đúng chuẩn Google yêu cầu
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"You are a professional financial analyst. Based on this market data, provide a concise summary (3-4 sentences) and highlight 2 interesting tickers in English:\n\n{market_data}"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }

    try:
        # 5. Gửi yêu cầu đi
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Kiểm tra nếu phản hồi lỗi
        if response.status_code != 200:
            return f"\n*(API Error: {response.status_code} - {response.text})*\n"
        
        # 6. Bóc tách dữ liệu JSON trả về
        result = response.json()
        
        # Dữ liệu của Gemini nằm ở: candidates -> content -> parts -> text
        advice_text = result['candidates'][0]['content']['parts'][0]['text']
        
        return f"\n---\n### 🤖 AI Financial Advisor (Direct REST API):\n\n{advice_text}\n\n*Analysis powered by Gemini 1.5 Flash*"

    except Exception as e:
        return f"\n*(Connection Error: {str(e)})*\n"