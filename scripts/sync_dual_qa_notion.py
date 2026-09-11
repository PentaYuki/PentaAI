"""
Script cập nhật đặc tả Phân tách Q&A Có Công Thức vs Q&A Không Công Thức
và Kho Tri Thức Công Thức Tập Trung lên Notion.
"""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PAGE_ID = "3d5ec2d5-0cde-81c9-a2f0-cbafc39cf4ed"
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

def callout(text, emoji="⚖️"):
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
    print("🚀 Đang cập nhật kiến trúc phân tách Q&A Có/Không Công Thức lên Notion...")

    dual_qa_blocks = [
        divider(),
        h1("8. Phân Tách Hai Nhánh Dữ Liệu: Q&A Có Công Thức vs Không Công Thức ⚖️"),
        callout(
            "NGUYÊN TẮC LIÊN KẾT HỆ THỐNG:\n"
            "Dữ liệu hỏi đáp (Q&A) trong Pentaschool bắt buộc phân tách thành 2 luồng xử lý độc lập để đảm bảo độ chính xác tuyệt đối:",
            "🧠"
        ),
        
        h2("Nhánh 1: Q&A CÓ CHỨA CÔNG THỨC (has_formula: true) 📐"),
        bullet("Vị trí lưu trữ: pentaschool/dataset/qa_with_formula/"),
        bullet("Liên kết hệ thống: Trỏ trực tiếp mã formula_ref tới Kho Tri Thức Công Thức Tập Trung (pentaschool/knowledge_base/formula_registry.json)."),
        bullet("Cơ chế giải: MÁY TÍNH TỰ GIẢI THEO CÔNG THỨC CHUẨN, đảm bảo độ chính xác tuyệt đối."),
        bullet("Ví dụ: '1 + 1 bằng mấy?', 'Giải phương trình x^2 - 5x + 6 = 0', 'Tính cạnh huyền tam giác vuông 3 và 4', 'Tính số mol của 11.2g Fe'."),
        code(
"""// Cấu trúc Q&A Có Chứa Công Thức
{
  "qa_id": "qa_form_003",
  "has_formula": true,
  "formula_ref": "MATH_QUADRATIC_EQ_01",
  "subject": "toan",
  "grade": "lop_9",
  "question": "Giải phương trình x^2 - 5x + 6 = 0",
  "extracted_params": { "a": 1, "b": -5, "c": 6 },
  "execution_path": "Pentaschool_Formula_Engine",
  "requires_llm_reasoning": false
}""", "json"),

        h2("Nhánh 2: Q&A KHÔNG CHỨA CÔNG THỨC (has_formula: false) 📖"),
        bullet("Vị trí lưu trữ: pentaschool/dataset/qa_no_formula/"),
        bullet("Liên kết hệ thống: Truy vấn qua Semantic Vector RAG (Qdrant + all-MiniLM-L6-v2) kết hợp LLM để diễn giải ý nghĩa."),
        bullet("Bản chất: Thuần túy là tri thức lý thuyết, định nghĩa, cảm thụ văn học, sự kiện lịch sử, giải thích hiện tượng tự nhiên."),
        bullet("Ví dụ: 'Tại sao lá cây có màu xanh?', 'Ý nghĩa nhan đề bài thơ Đồng chí', 'Định nghĩa số nguyên tố', 'Chiến thắng Điện Biên Phủ 1954'."),
        code(
"""// Cấu trúc Q&A Không Chứa Công Thức
{
  "qa_id": "qa_concept_001",
  "has_formula": false,
  "formula_ref": null,
  "subject": "sinh_hoc",
  "grade": "lop_6",
  "question": "Tại sao hầu hết lá cây lại có màu xanh?",
  "execution_path": "Semantic_RAG_LLM",
  "requires_llm_reasoning": true,
  "answer": "Lá cây có màu xanh do chứa sắc tố diệp lục phản xạ ánh sáng xanh lục..."
}""", "json"),

        callout("Hệ thống đã thiết lập luồng định tuyến tự động (Dynamic Routing) phân loại câu hỏi của học sinh vào đúng 1 trong 2 nhánh xử lý!", "🚀")
    ]

    append_blocks(PAGE_ID, dual_qa_blocks)
    print("✅ Đã ghi nhận kiến trúc phân tách Q&A Có/Không Công Thức lên Notion!")

if __name__ == "__main__":
    main()
