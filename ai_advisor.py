from google import genai
import os

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found in environment variables)*\n"

    try:
        # Khởi tạo Client theo chuẩn SDK 2026
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a senior financial analyst. Process this market data with a step-by-step reasoning approach:
        
        DATA:
        {market_data}
        
        INSTRUCTIONS:
        1. Macro Analysis: Identify the strongest and weakest sectors.
        2. Technical Focus: Spot any tickers with RSI signals.
        3. Strategic Advice: Provide a concise English summary.
        
        OUTPUT REQUIREMENT:
        - Language: English.
        - Tone: Sharp and professional.
        """
        
        # Sửa lỗi 404 bằng cách gọi model chuẩn
        response = client.models.generate_content(
            model='gemini-1.5-flash', # Lưu ý: Không cần thêm tiền tố 'models/'
            contents=prompt
        )
        
        advice_content = f"\n---\n### 🤖 AI Financial Advisor Analysis:\n\n"
        advice_content += response.text
        advice_content += "\n\n*Disclaimer: For educational purposes only.*"
        
        return advice_content
    except Exception as e:
        return f"\n*(AI Error: {e})*\n"