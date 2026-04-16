import requests
import os
import json

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    # PHƯƠNG ÁN 2026: Dùng Gemini 2.0 Flash (Model mặc định mới của Google)
    # Lưu ý: Model 2.0 dùng endpoint v1alpha hoặc v1beta tùy vùng, mình sẽ dùng v1beta
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Professional financial summary in English (3 sentences) for this data: {market_data}"
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        
        # Nếu vẫn 404, chúng ta sẽ gọi API để xem chính xác Phu được dùng model nào
        if response.status_code == 404:
            list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            list_res = requests.get(list_url).json()
            models = [m['name'] for m in list_res.get('models', [])]
            return f"\n*(Lỗi 404: Model 2.0 không tìm thấy. Các model bạn có quyền dùng là: {', '.join(models)})*\n"

        if response.status_code != 200:
            return f"\n*(API Error: {response.status_code})*\n"

        result = response.json()
        advice_text = result['candidates'][0]['content']['parts'][0]['text']
        return f"\n---\n### 🤖 AI Financial Advisor (Gemini 2.0):\n\n{advice_text}"

    except Exception as e:
        return f"\n*(Connection Error: {str(e)})*\n"