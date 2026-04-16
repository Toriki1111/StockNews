import google.generativeai as genai
import os

def get_ai_advice(market_data):
    api_key = os.getenv("AI_KEY")
    
    if not api_key:
        return "\n*(Note: AI_KEY not found)*\n"

    try:
        # 1. Cấu hình API Key
        genai.configure(api_key=api_key)
        
        # 2. KHẮC PHỤC LỖI 404: Tạo model và ép dùng API v1
        # Chúng ta dùng cấu hình từ thư viện core để đảm bảo không bị nhảy version
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash'
        )
        
        prompt = f"Summarize this US stock market data in 3-4 professional English sentences: {market_data}"
        
        # 3. Gọi API với transport mặc định là 'grpc' hoặc 'rest' để ổn định
        response = model.generate_content(prompt)
        
        return f"\n---\n### 🤖 AI Financial Advisor:\n\n{response.text}"

    except Exception as e:
        # Nếu vẫn lỗi, in ra để check xem nó còn báo v1beta không
        return f"\n*(Gemini Error: {str(e)})*\n"