import google.generativeai as genai
import os

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found in environment variables)*\n"

    try:
        # Cấu hình API Key
        genai.configure(api_key=api_key)
        
        # Khởi tạo model - dùng tên chuẩn
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a senior financial analyst. Analyze this market data:
        {market_data}
        
        Requirements:
        - Language: English.
        - Summary: 3-4 sentences.
        - Highlights: 2 stocks.
        """
        
        # Gọi API
        response = model.generate_content(prompt)
        
        advice_content = f"\n---\n### 🤖 AI Financial Advisor Analysis:\n\n"
        advice_content += response.text
        advice_content += "\n\n*Disclaimer: For educational purposes only.*"
        
        return advice_content
    except Exception as e:
        return f"\n*(AI Error: {str(e)})*\n"