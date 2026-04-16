import google.generativeai as genai
import os

def get_ai_advice(market_data):
    # Lấy API Key từ Secret bạn đặt là AI_KEY
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found in environment variables)*\n"

    try:
        genai.configure(api_key=api_key)
        
        # Khởi tạo model với cấu hình tối ưu tư duy
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "max_output_tokens": 1024,
            }
        )
        
        prompt = f"""
        You are a senior financial analyst. Process this market data with a step-by-step reasoning approach:
        
        DATA:
        {market_data}
        
        INSTRUCTIONS:
        1. Macro Analysis: Identify the strongest and weakest sectors from the data.
        2. Technical Focus: Spot any tickers with RSI > 70 (Overbought) or RSI < 30 (Oversold). 
        3. Strategic Advice: Provide a concise English summary and actionable outlook.
        
        OUTPUT REQUIREMENT:
        - Language: English.
        - Tone: Sharp, professional, and data-driven.
        """
        
        response = model.generate_content(prompt)
        
        advice_content = f"\n---\n### 🤖 AI Financial Advisor Analysis:\n\n"
        advice_content += response.text
        advice_content += "\n\n*Disclaimer: Technical analysis is for informational purposes only.*"
        
        return advice_content
    except Exception as e:
        return f"\n*(AI Error: {e})*\n"