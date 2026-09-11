"""
Script tạo và nạp dữ liệu thực tế vào 2 Database tương tác trực tiếp trên Notion:
1. Database 1: '🎯 Dataset Phân Loại Ý Định (Intent)' (Có dấu & Không dấu)
2. Database 2: '🎭 Dataset Q&A 3 Nhân Vật (Cute - Serious - Yandere)' (Từng nhân vật với câu trả lời đặc trưng)
Nạp dữ liệu từ các file JSON trong pentami-core/dataset/ lên Notion.
"""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PAGE_ID = "3d5ec2d5-0cde-81c9-a2f0-cbafc39cf4ed" # Sub-page Master Data 3 nhân vật
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

def create_database(page_id, title, properties):
    url = "https://api.notion.com/v1/databases"
    payload = {
        "parent": {"type": "page_id", "page_id": page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties
    }
    res = api_call(url, method="POST", data=payload)
    print(f"✅ Created Database: {title} (ID: {res['id']})")
    return res["id"]

def add_intent_row(db_id, query_acc, query_unacc, app_name):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Câu Hỏi (Có Dấu)": {
                "title": [{"text": {"content": query_acc[:100]}}]
            },
            "Câu Hỏi (Không Dấu)": {
                "rich_text": [{"text": {"content": query_unacc[:100]}}]
            },
            "Phân Hệ (Target App)": {
                "select": {"name": app_name}
            }
        }
    }
    return api_call(url, method="POST", data=payload)

def add_persona_row(db_id, query_acc, query_unacc, persona_name, category, answer):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Câu Hỏi (Có Dấu)": {
                "title": [{"text": {"content": query_acc[:100]}}]
            },
            "Câu Hỏi (Không Dấu)": {
                "rich_text": [{"text": {"content": query_unacc[:100]}}]
            },
            "Nhân Vật (Persona)": {
                "select": {"name": persona_name}
            },
            "Chủ Đề (Category)": {
                "select": {"name": category}
            },
            "Câu Trả Lời (Answer)": {
                "rich_text": [{"text": {"content": answer[:1000]}}]
            }
        }
    }
    return api_call(url, method="POST", data=payload)

def main():
    print("🚀 Bắt đầu tạo 2 Database Notion trực quan...")

    # 1. DATABASE 1: INTENT CLASSIFICATION DATABASE
    intent_db_id = "3d5ec2d5-0cde-814a-a509-d9aa4c86d556" # Đã tạo ở test trước

    # 2. DATABASE 2: PERSONA Q&A DATABASE
    persona_db_props = {
        "Câu Hỏi (Có Dấu)": {"title": {}},
        "Câu Hỏi (Không Dấu)": {"rich_text": {}},
        "Nhân Vật (Persona)": {
            "select": {
                "options": [
                    {"name": "Dễ Thương 🎀", "color": "pink"},
                    {"name": "Nghiêm Túc 👔", "color": "blue"},
                    {"name": "Yandere 🖤", "color": "red"}
                ]
            }
        },
        "Chủ Đề (Category)": {
            "select": {
                "options": [
                    {"name": "Học bài", "color": "green"},
                    {"name": "Lười học", "color": "yellow"},
                    {"name": "Tìm file", "color": "purple"},
                    {"name": "Dọn máy", "color": "gray"},
                    {"name": "Mua sắm", "color": "orange"},
                    {"name": "Giảm giá", "color": "brown"},
                    {"name": "Tìm việc", "color": "blue"},
                    {"name": "Phỏng vấn", "color": "red"},
                    {"name": "Chào hỏi", "color": "default"}
                ]
            }
        },
        "Câu Trả Lời (Answer)": {"rich_text": {}}
    }
    persona_db_id = create_database(PAGE_ID, "🎭 Dataset Q&A 3 Nhân Vật (Cute - Serious - Yandere)", persona_db_props)

    # 3. Nạp dữ liệu vào Database 1 (Intent)
    print("📥 Nạp dữ liệu vào Intent Database...")
    with open("pentami-core/dataset/intent_classification_500.json", "r", encoding="utf-8") as f:
        intent_items = json.load(f)

    app_map = {
        "pentaschool": "Pentaschool",
        "pentakuru": "Pentakuru",
        "pentamarket": "Pentamarket",
        "pentajob": "PentaJob",
        "general_chat": "General Chat"
    }

    # Chọn mẫu tiêu biểu đa dạng từ các nhóm intent
    sample_intents = []
    for app_key in app_map.keys():
        matching = [x for x in intent_items if x["intent"] == app_key]
        sample_intents.extend(matching[:6]) # Lấy 6 mẫu cho mỗi app = 30 mẫu trực quan trên bảng

    for item in sample_intents:
        add_intent_row(intent_db_id, item["query_accented"], item["query_unaccented"], app_map[item["intent"]])
        time.sleep(0.15)
    print(f"✅ Đã nạp {len(sample_intents)} dòng vào Intent Database!")

    # 4. Nạp dữ liệu vào Database 2 (Persona Q&A)
    print("📥 Nạp dữ liệu vào Persona Q&A Database...")
    cute_items = json.load(open("pentami-core/dataset/persona_cute_500.json", encoding="utf-8"))
    serious_items = json.load(open("pentami-core/dataset/persona_serious_500.json", encoding="utf-8"))
    yandere_items = json.load(open("pentami-core/dataset/persona_yandere_500.json", encoding="utf-8"))

    cat_map = {
        "học bài": "Học bài",
        "lười học": "Lười học",
        "tìm file": "Tìm file",
        "dọn máy": "Dọn máy",
        "mua sắm": "Mua sắm",
        "giảm giá": "Giảm giá",
        "tìm việc": "Tìm việc",
        "phỏng vấn": "Phỏng vấn",
        "chào hỏi": "Chào hỏi"
    }

    # Nạp mẫu đối chiếu giữa 3 nhân vật cho từng chủ đề
    for cat_raw, cat_name in cat_map.items():
        # Dễ thương
        c = next((x for x in cute_items if x["category"] == cat_raw), None)
        if c:
            add_persona_row(persona_db_id, c["question"], c["question_no_accent"], "Dễ Thương 🎀", cat_name, c["answer"])
            time.sleep(0.15)
        # Nghiêm túc
        s = next((x for x in serious_items if x["category"] == cat_raw), None)
        if s:
            add_persona_row(persona_db_id, s["question"], s["question_no_accent"], "Nghiêm Túc 👔", cat_name, s["answer"])
            time.sleep(0.15)
        # Yandere
        y = next((x for x in yandere_items if x["category"] == cat_raw), None)
        if y:
            add_persona_row(persona_db_id, y["question"], y["question_no_accent"], "Yandere 🖤", cat_name, y["answer"])
            time.sleep(0.15)

    print("🎉 HOÀN TẤT NẠP TOÀN BỘ DATASET VÀO CÁC BẢNG DATABASE NOTION!")

if __name__ == "__main__":
    main()
