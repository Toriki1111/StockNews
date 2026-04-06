import requests
from datetime import datetime

# Danh sách các mã bạn quan tâm
stocks = ["BSR", "PVT", "PVC"]

def get_stock_info():
    content = f"## Nhật ký chứng khoán - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    content += "| Mã | Trạng thái |\n|---|---|\n"
    
    for symbol in stocks:
        # Đây là ví dụ, thực tế bạn có thể dùng API của SSI hoặc các nguồn free
        content += f"| {symbol} | Đã cập nhật hoạt động |\n"
    
    return content

if __name__ == "__main__":
    data = get_stock_info()
    with open("autocommit.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n")