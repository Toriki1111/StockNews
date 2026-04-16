import google.generativeai as genai
import os

def get_ai_advice(market_data):
    # Lấy Key Phu vừa mới tạo ngày hôm nay dán vào GitHub Secret nhé
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    try:
        # Cấu hình kiểu cũ nhưng cực kỳ chắc chắn
        genai.configure(api_key=api_key)
        
        # Gọi model 1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Analyze this market data in 3-4 professional English sentences: {market_data}"
        
        response = model.generate_content(prompt)
        
        return f"\n---\n### 🤖 AI Financial Advisor:\n\n{response.text}\n\n*Free Tier Analysis*"
    except Exception as e:
        return f"\n*(Gemini Error: {str(e)})*\n"