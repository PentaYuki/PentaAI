"""
Script cập nhật cấu trúc Datasheet chi tiết cho Pentaschool (Toán, Lý, Hóa, Sinh, Văn, Sử, Địa, Ngoại Ngữ, Tin Học)
và các thư mục tính toán, biểu phí trường học lên Notion.
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

def callout(text, emoji="📚"):
    return {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": text}}], "icon": {"type": "emoji", "emoji": emoji}}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def append_blocks(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    for i in range(0, len(blocks), 60):
        chunk = blocks[i:i+60]
        api_call(url, method="PATCH", data={"children": chunk})
        time.sleep(0.5)

def main():
    print("🚀 Ghi nhận cấu trúc thư mục Datasheet phổ thông lên Notion...")

    datasheet_blocks = [
        divider(),
        h1("7. Cấu Trúc Thư Mục Datasheet Các Môn Học (Toán, Lý, Hóa, Sinh, Văn...) 📚"),
        callout(
            "QUY HOẠCH CHUẨN: Toàn bộ dữ liệu Pentaschool được chia nhỏ theo từng thư mục môn học phổ thông & nâng cao, đảm bảo đầy đủ và dễ mở rộng cho nhà trường.",
            "🏫"
        ),
        bullet("📐 toan/: dai_so, hinh_hoc, giai_tich (Phương trình, hình không gian, đạo hàm, tích phân)"),
        bullet("⚡ vat_ly/: co_hoc, nhiet_hoc, dien_tu_hoc, quang_hoc (Chuyển động, nhiệt học, mạch điện, sóng)"),
        bullet("🧪 hoa_hoc/: hoa_vo_co, hoa_huu_co, hoa_dai_cuong (Kim loại, phi kim, este, polime, bảng tuần hoàn)"),
        bullet("🧬 sinh_hoc/: sinh_hoc_te_bao, di_truyen_hoc, sinh_thai_hoc (DNA, quy luật di truyền, hệ sinh thái)"),
        bullet("📖 ngu_van/: van_hoc_trung_dai, van_hoc_hien_dai, ky_nang_lam_van (Thơ, truyện ngắn, nghị luận xã hội)"),
        bullet("🇬🇧 tieng_anh/: ngu_phap_grammar, tu_vung_vocabulary, luyen_thi_ielts_toeic (Ngữ pháp, từ vựng theo chủ đề)"),
        bullet("🏛️ lich_su/: lich_su_viet_nam, lich_su_the_gioi (Lịch sử dựng nước, các thời kỳ văn minh)"),
        bullet("🌍 dia_ly/: dia_ly_tu_nhien, dia_ly_kinh_te_xa_hoi (Khí hậu, địa hình, các vùng kinh tế)"),
        bullet("💻 tin_hoc/: tin_hoc_dai_cuong, lap_trinh_co_ban (Hệ điều hành, tư duy thuật toán)"),
        
        divider(),
        h2("Cấu Trúc Thư Mục Tính Toán & Biểu Phí Nhà Trường:"),
        bullet("📂 Pentakuru: file_retrieval, computational_math (Module tính toán bảng biểu), financial_tables, code_analysis."),
        bullet("🛒 Pentamarket: pricing_rules, tax_vat_configs (Thuế VAT 8%/10% tùy chỉnh theo trường), school_fee_policies, discounts_vouchers.")
    ]

    append_blocks(PAGE_ID, datasheet_blocks)
    print("✅ Đã cập nhật đầy đủ cấu trúc thư mục Datasheet lên Notion!")

if __name__ == "__main__":
    main()
