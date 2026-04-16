import anthropic
import os

def get_ai_advice(market_data):
    # Lấy Key của Claude (đã dán vào Secret AI_KEY)
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: Claude API Key not found)*\n"

    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Gọi model Claude 3.5 Sonnet hoặc Claude 3 Haiku
        message = client.messages.create(
            model="claude-3-haiku-20240307", # Bản Haiku chạy rất nhanh và rẻ
            max_tokens=500,
            messages=[
                {
                    "role": "user", 
                    "content": f"Analyze this US stock data in professional English: {market_data}"
                }
            ]
        )
        
        return f"\n---\n### 🤖 Claude AI Advisor:\n\n{message.content[0].text}"
    except Exception as e:
        return f"\n*(Claude Error: {str(e)})*\n"