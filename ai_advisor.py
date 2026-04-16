from google import genai
import os

def get_ai_advice(market_data):
    # Lấy Key từ GitHub Secret đã cấu hình ở bước trên
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    try:
        # ÉP DÙNG VERSION v1 (ỔN ĐỊNH NHẤT)
        client = genai.Client(
            api_key=api_key,
            http_options={'api_version': 'v1'}
        )
        
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=f"Analyze this US stock data in English: {market_data}"
        )
        
        return f"\n---\n### 🤖 AI Advisor:\n\n{response.text}"
    except Exception as e:
        return f"\n*(AI Error: {str(e)})*\n"