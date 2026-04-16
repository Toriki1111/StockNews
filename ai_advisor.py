from google import genai
import os

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    try:
        # 1. Khởi tạo Client
        client = genai.Client(api_key=api_key)
        
        # 2. Gọi model - Lưu ý: dùng đúng tên 'gemini-1.5-flash' 
        # và không cần thêm tiền tố 'models/'
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=f"Analyze this market data in professional English: {market_data}"
        )
        
        # 3. Trả về kết quả
        if response and response.text:
            advice_content = f"\n---\n### 🤖 AI Financial Advisor (SDK 2026):\n\n"
            advice_content += response.text
            advice_content += "\n\n*Disclaimer: Technical analysis for educational purposes only.*"
            return advice_content
        else:
            return "\n*(AI returned empty response)*\n"

    except Exception as e:
        # In ra lỗi chi tiết để Phu dễ debug nếu vẫn còn 404
        return f"\n*(AI Migration Error: {str(e)})*\n"