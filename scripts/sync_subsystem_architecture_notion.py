"""
Script cập nhật cấu trúc phân tách Master Data theo từng phân hệ lên Notion:
- Ghi nhận việc tách biệt data: Pentaschool (từng bài học), Pentakuru (tính toán), Pentamarket (thuế & giá trường học).
- Cập nhật bộ 1.000 câu Intent mở rộng đa dạng (dù gõ kiểu gì cũng nhận diện chuẩn).
"""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PAGE_ID = "3d5ec2d5-0cde-81c9-a2f0-cbafc39cf4ed" # Sub-page Master Data 3 nhân vật & Intent
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

def api_call(url, method="GET", data=None):
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"[HTTP Error {e.code}] on {method} {url}: {err_body}")
            if e.code == 429:
                time.sleep(2)
                continue
            raise e
        except Exception as e:
            print(f"[Request Error] {e}")
            time.sleep(1)
    return None

def h1(text):
    return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h2(text):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def p(text):
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def callout(text, emoji="🏛️"):
    return {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": text}}], "icon": {"type": "emoji", "emoji": emoji}}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def code(content, language="json"):
    return {"object": "block", "type": "code", "code": {"rich_text": [{"type": "text", "text": {"content": content}}], "language": language}}

def append_blocks(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    for i in range(0, len(blocks), 60):
        chunk = blocks[i:i+60]
        api_call(url, method="PATCH", data={"children": chunk})
        time.sleep(0.5)

def main():
    print("🚀 Ghi cập nhật cấu trúc phân tách Master Data độc lập lên Notion...")

    subsystem_blocks = [
        divider(),
        h1("6. Phân Tách Master Data Độc Lập Cho Từng Phân Hệ 🏛️"),
        callout(
            "NGUYÊN TẮC THIẾT KẾ DATA MASTER (MODULAR ISOLATION):\n"
            "Không gộp chung dữ liệu vào một file duy nhất. Mỗi phân hệ sở hữu kho dữ liệu chuyên biệt phục vụ logic nghiệp vụ phức tạp của riêng mình.",
            "📦"
        ),
        
        h2("1. Pentaschool Data (Q&A Chi Tiết Từng Môn Học & Bài Học) 🎓"),
        bullet("Vị trí lưu trữ: pentaschool/dataset/master_qa_courses.json"),
        bullet("Cấu trúc phân cấp: Course -> Chapter -> Lesson -> Q&A Pair."),
        bullet("Nội dung: Bao phủ chi tiết các môn thuật toán cây nhị phân, quy hoạch động, Golang concurrency, hệ thống phân tán và kỹ thuật AI."),

        h2("2. Pentakuru Data (Tìm File + Module Tính Toán Bảng Biểu Số Liệu) 📂"),
        bullet("Vị trí lưu trữ: pentakuru/dataset/master_file_calc.json"),
        bullet("Đặc thù phức tạp: Vừa tìm kiếm file (PDF, Excel, Word, Code) vừa tích hợp Module Tính Toán (Computational Math Engine)."),
        bullet("Các tác vụ tính toán: Tính tổng doanh thu từ file Excel, tính trung bình cộng điểm số, tính phần trăm tăng trưởng ngân sách, đếm dòng code."),

        h2("3. Pentamarket / Pentamo Data (Giá Cả, Thuế VAT & Biểu Phí Nhà Trường) 🛒"),
        bullet("Vị trí lưu trữ: pentamarket/dataset/master_pricing_tax.json"),
        bullet("Cơ chế tùy chỉnh theo Tenant (Configurable per School): Các trường học/doanh nghiệp có thể tự điều chỉnh mức thuế VAT (8% hoặc 10%), biểu phí tài liệu, phụ phí học kỳ và chính sách học bổng."),
        bullet("Quy tắc tính toán: Module hỗ trợ tính giá combo, giá sau giảm voucher và miễn giảm thuế."),

        h2("4. PentaJob Data (Tuyển Dụng, Kỹ Năng & Kịch Bản Phỏng Vấn) 💼"),
        bullet("Vị trí lưu trữ: pentajob/dataset/master_career_interview.json"),
        bullet("Nội dung: Phân tích thang lương thị trường theo từng vị trí (Backend, Frontend, AI Engineer, DevOps) và ngân hàng câu hỏi phỏng vấn kỹ thuật."),

        h2("5. Pentami Core Data (1.000 Mẫu Ý Định Mở Rộng - Có Dấu & Không Dấu) 🎯"),
        bullet("Vị trí lưu trữ: pentami-core/dataset/master_intent_1000.json"),
        bullet("Quy mô: Đúng 1.000 mẫu câu truy vấn (200 câu cho mỗi phân hệ)."),
        bullet("Độ bền bỉ: Dù người dùng gõ sai chính tả nhẹ, gõ tắt, hay gõ 100% KHÔNG DẤU, hệ thống vẫn nhận diện chính xác ý định."),
        callout("Đã hoàn tất phân tách toàn bộ dữ liệu master vào từng thư mục dự án tương ứng!", "✅")
    ]

    append_blocks(PAGE_ID, subsystem_blocks)
    print("🎉 Hoàn tất cập nhật kiến trúc phân tách Master Data lên Notion!")

if __name__ == "__main__":
    main()
