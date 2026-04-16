from google import genai
import os

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    try:
        # Unified SDK sử dụng Client object
        client = genai.Client(api_key=api_key)
        
        # Cú pháp mới: models.generate_content
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Please analyze this US market data in English: {market_data}"
        )
        
        advice_content = f"\n---\n### 🤖 AI Financial Advisor (New SDK):\n\n"
        advice_content += response.text
        advice_content += "\n\n*Disclaimer: Technical analysis for educational purposes only.*"
        
        return advice_content
    except Exception as e:
        return f"\n*(AI Migration Error: {str(e)})*\n"