"""
Script ghi nhận Rulebook GEMINI.md / ANTIGRAVITY.md lên Notion:
- Quy tắc thiết kế module chuẩn Guru Factory
- Quản lý dữ liệu & tri thức: Phân tầng dữ liệu có cấu trúc và Semantic RAG
- Hệ thống Intent liên thông toàn bộ hệ sinh thái Penta
"""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
MAIN_PAGE_ID = "3d5ec2d5-0cde-8044-a025-c60875a4f00b"
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

def callout(text, emoji="📜"):
    return {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": text}}], "icon": {"type": "emoji", "emoji": emoji}}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def main():
    print("🚀 Ghi nhận Rulebook GEMINI.md lên trang chính Notion...")
    blocks = [
        divider(),
        h1("4. Bộ Quy Tắc Kiến Trúc Bắt Buộc (GEMINI.md / ANTIGRAVITY.md) 📜"),
        callout(
            "QUY TẮC PHÁT TRIỂN & TIÊU CHUẨN GURU FACTORY:\n"
            "Tệp GEMINI.md tại gốc dự án đã được thiết lập chặt chẽ để đảm bảo mọi module phát triển tiếp theo đều đồng nhất, không phân mảnh và chuẩn hóa tuyệt đối.",
            "⚖️"
        ),
        bullet("🏭 Tiêu chuẩn Guru Factory: Mọi module phải có interface, implementation, factory và registry độc lập; cấm import chéo chặt chẽ."),
        bullet("📐 Quản lý tri thức: Phân tầng dữ liệu có cấu trúc qua SQL/Storage và tri thức ngữ nghĩa qua Semantic Vector RAG."),
        bullet("🌐 Intent Router Toàn Hệ Sinh Thái: Phủ sóng toàn bộ 5 phân hệ (Pentaschool, Pentakuru, Pentamarket, PentaJob, Playwright) và kháng lỗi 100% tiếng Việt không dấu."),
        bullet("🎭 Stream 3D: chunk_emo, chunk_time, chunk_action đóng gói chuẩn hóa, tách riêng action sang giai đoạn sau.")
    ]
    url = f"https://api.notion.com/v1/blocks/{MAIN_PAGE_ID}/children"
    api_call(url, method="PATCH", data={"children": blocks})
    print("✅ Đã ghi nhận Rulebook lên trang chính Notion!")

if __name__ == "__main__":
    main()
