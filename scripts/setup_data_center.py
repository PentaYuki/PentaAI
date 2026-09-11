"""
Script khởi tạo Sub-page 'Data Center' bên dưới Pentami Core trên Notion:
- Tổ chức toàn bộ dữ liệu có thể xuất hiện trong hệ sinh thái Penta AI:
  1. Identity & IAM Data
  2. Sessions & 3D Stream Chunks Data
  3. Knowledge & RAG Vector Data
  4. Realtime Voice & Audio Data
  5. Business Domain Data (Pentaschool, Pentakuru, Pentamarket, PentaJob)
  6. MCP Playwright Automation Data
- Cung cấp schema SQL mẫu, Redis key structures, Vector payload specs.
"""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PENTAMI_CORE_PAGE_ID = "3d5ec2d5-0cde-810b-a566-d329dfd2a6f5" # ID của trang Pentami Core
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

def h3(text):
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def p(text):
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def callout(text, emoji="💾"):
    return {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": text}}], "icon": {"type": "emoji", "emoji": emoji}}}

def todo(text, checked=False):
    return {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": text}}], "checked": checked}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def code(content, language="sql"):
    return {"object": "block", "type": "code", "code": {"rich_text": [{"type": "text", "text": {"content": content}}], "language": language}}

def append_blocks(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    for i in range(0, len(blocks), 75):
        chunk = blocks[i:i+75]
        api_call(url, method="PATCH", data={"children": chunk})
        time.sleep(0.5)

def main():
    print("🚀 Bắt đầu khởi tạo sub-page 'Data Center' dưới Pentami Core...")

    data_center_blocks = [
        callout(
            "PENTA DATA CENTER - TRUNG TÂM DỮ LIỆU & STATE ENGINE CỦA HỆ SINH THÁI PENTA\n"
            "Nơi hội tụ, lưu trữ, điều phối và phân vùng toàn bộ dữ liệu sống: Từ định danh người dùng, luồng nhận thức 3D, tri thức RAG đến nghiệp vụ của các phân hệ vệ tinh.",
            "💾"
        ),
        h1("1. Chiến Lược Kiến Trúc Dữ Liệu 4 Tầng (Tiered Storage)"),
        bullet("⚡ Tầng Siêu Tốc (In-Memory Cache): Redis 7.2 - Quản lý Session, Token Bucket Rate Limit, Pub/Sub, Presence, tra cứu API Key < 1ms."),
        bullet("🏛️ Tầng Quan Hệ Bền Vững (ACID Master): PostgreSQL 16 - Quản lý Người dùng, Tổ chức (Tenants), Khóa bảo mật, Đơn hàng, Khóa học."),
        bullet("🔮 Tầng Ngữ Nghĩa Tri Thức (Vector Database): Qdrant - Lưu trữ 384 dimensions vector từ all-MiniLM-L6-v2 với Payload Filtering cô lập."),
        bullet("💻 Tầng Biên Cục Bộ (Client / Edge Embedded DB): SQLite-VSS / LanceDB - Quản lý chỉ mục file và ghi chú nhanh trên máy khách Pentakuru."),
        divider(),

        h1("2. Danh Mục Các Thực Thể Dữ Liệu Xuất Hiện Trong Hệ Sinh Thái"),
        
        # ----------------------------------------------------
        h2("Phần 1: Dữ Liệu Định Danh & Bảo Mật (Identity & IAM)"),
        p("Xuất hiện tại: Penta Gateway, Pentami Core, và làm chìa khóa liên thông cho mọi phân hệ:"),
        bullet("User / Account: ID người dùng, email, họ tên, avatar, mật khẩu băm bcrypt, trạng thái kích hoạt."),
        bullet("Tenant / Organization: Định danh tổ chức/công ty, gói dịch vụ (Pro/Enterprise), giới hạn tài nguyên."),
        bullet("API Key & Scopes: Khóa truy cập (penta_live_sk_...), hash HMAC-SHA256, mảng quyền (penta:school:*, penta:market:*, action:playwright:execute)."),
        bullet("Audit Security Log: Lịch sử gọi API, địa chỉ IP, sự kiện vi phạm rate limit."),
        code(
"""-- 1. BẢNG NGƯỜI DÙNG & TỔ CHỨC
CREATE TABLE tenants (
    tenant_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(32) DEFAULT 'standard',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(32) DEFAULT 'member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. BẢNG API KEY LIÊN THÔNG TOÀN HỆ SINH THÁI
CREATE TABLE api_keys (
    key_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(user_id),
    tenant_id VARCHAR(64) REFERENCES tenants(tenant_id),
    key_hash VARCHAR(64) UNIQUE NOT NULL, -- Băm HMAC-SHA256
    name VARCHAR(128) NOT NULL,
    scopes TEXT[] NOT NULL,
    rate_limit_rpm INT DEFAULT 120,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);""", "sql"),
        divider(),

        # ----------------------------------------------------
        h2("Phần 2: Dữ Liệu Hội Thoại & Giao Thức Stream 3D (Cognitive & Stream Data)"),
        p("Xuất hiện tại: Pentami Core, Pentaschool (Avatar), Pentamarket (Sales Bot), PentaJob (Interviewer):"),
        bullet("Session State: Phiên hội thoại trực tuyến, phân hệ đang tương tác, Persona được chọn."),
        bullet("Message History: Lịch sử câu hỏi người dùng và câu trả lời của AI."),
        bullet("Chunk Emo: Cảm xúc (neutral, joyful, encouraging, thoughtful, serious), intensity (0.0-1.0), cử chỉ Avatar (head_nod, hand_wave), pitch/rate giọng nói."),
        bullet("Chunk Time: Token index, thời điểm phát âm cue_start_ms, độ dài duration_ms, mã khẩu hình môi viseme_code cho Avatar."),
        bullet("Chunk Action: Lệnh tự động hóa (action_id, target_system, command, params, require_confirmation)."),
        code(
"""-- CẤU TRÚC JSON GIAO THỨC STREAM 3D (PUASP)
{
  "seq": 108,
  "session_id": "sess_889123",
  "type": "emo" | "time" | "action" | "text",
  "emo": {
    "emotion": "encouraging",
    "intensity": 0.85,
    "gesture": "head_nod"
  },
  "time": {
    "token_index": 12,
    "cue_start_ms": 1400,
    "duration_ms": 320,
    "viseme_code": "viseme_oh"
  },
  "action": {
    "action_id": "act_open_quiz_01",
    "target_system": "pentaschool",
    "command": "render_interactive_quiz",
    "params": { "quiz_id": "algo_tree_01" }
  }
}""", "json"),
        divider(),

        # ----------------------------------------------------
        h2("Phần 3: Dữ Liệu Tri Thức & Vector RAG (Knowledge & Embedding Vectors)"),
        p("Xuất hiện tại: Pentami Core, Qdrant Vector DB:"),
        bullet("Mô hình nhúng: sentence-transformers/all-MiniLM-L6-v2 (Vector 384 dimensions)."),
        bullet("Knowledge Documents: Văn bản nguồn (sách giáo trình, cẩm nang sản phẩm, JD tuyển dụng, file máy tính)."),
        bullet("Synthetic Q&A Pairs: Cặp câu hỏi - trả lời ban đầu (Cold Start) kết hợp làm giàu động (Dynamic Enrichment) bằng LLM."),
        code(
"""-- CẤU TRÚC QDRANT VECTOR PAYLOAD (384 dimensions)
{
  "id": "doc_chk_991823",
  "vector": [0.034, -0.012, 0.089, ...], -- 384 dimensions
  "payload": {
    "tenant_id": "tenant_penta_corp",
    "app_id": "pentaschool", -- hoặc "pentamarket", "pentakuru", "pentajob"
    "doc_id": "doc_algo_ch03",
    "chunk_index": 4,
    "question": "Độ phức tạp của cây nhị phân là gì?",
    "answer": "Độ phức tạp trung bình khi tìm kiếm là O(log n)...",
    "source_context": "Giáo trình Cấu trúc dữ liệu chương 3",
    "tags": ["algorithm", "binary_tree"],
    "is_enriched": true
  }
}""", "json"),
        divider(),

        # ----------------------------------------------------
        h2("Phần 4: Dữ Liệu Nghiệp Vụ Từng Phân Hệ Vệ Tinh (Domain Business Data)"),
        
        h3("A. Dữ Liệu Pentaschool (LMS):"),
        bullet("Khóa học & Bài học: courses, chapters, lessons, video_url, transcript."),
        bullet("Bài tập & Kiểm tra: quizzes, questions, options, correct_answer."),
        bullet("Tiến độ & Học bạ AI: course_progress, quiz_submissions, ai_learning_analytics."),
        
        h3("B. Dữ Liệu Pentakuru (Local File Knowledge):"),
        bullet("Chỉ mục tệp tin máy tính: file_path, file_hash (SHA-256), file_size, file_type, last_modified."),
        bullet("Ghi chú & Tóm tắt AI: quick_summary, key_takeaways, local_vector_ids, sync_status."),

        h3("C. Dữ Liệu Pentamarket (E-commerce):"),
        bullet("Gian hàng & Sản phẩm: products, categories, price, stock, specifications_json, images."),
        bullet("Giao dịch & Giỏ hàng: cart_items, orders, order_items, payment_status, shipping_address."),

        h3("D. Dữ Liệu PentaJob (Tuyển Dụng & Phỏng Vấn):"),
        bullet("Tin tuyển dụng: job_postings, company_name, requirements, salary_range, required_skills."),
        bullet("Hồ sơ ứng viên: candidate_resumes, parsed_skills_json, years_of_experience."),
        bullet("Phòng phỏng vấn giọng nói: mock_interviews, audio_recordings, transcripts, ai_scorecard."),
        divider(),

        # ----------------------------------------------------
        h2("Phần 5: Dữ Liệu Tự Động Hóa Web (Playwright MCP Data)"),
        bullet("Browser Session State: Phiên Chromium cô lập, viewport size, proxy cấu hình."),
        bullet("Encrypted Credentials: Cookie, Auth tokens được mã hóa an toàn lưu trữ theo phiên user."),
        bullet("Automation Action Logs: Lịch sử các lệnh navigate, click, fill, screenshot, trích xuất dữ liệu DOM."),
        divider(),

        h1("3. Lộ Trình Xây Dựng Data Center (Build Roadmap)"),
        todo("1. Khởi tạo Database Schema PostgreSQL 16 (Tenants, Users, API Keys, Business Tables)", False),
        todo("2. Thiết lập Redis Data Structures (API Key Cache, Token Bucket Rate Limiting, Stream Buffers)", False),
        todo("3. Khởi tạo Qdrant Collection 'penta_knowledge' với vector 384 dimensions & Payload Indexes", False),
        todo("4. Xây dựng Data Migration Script & Seed Data ban đầu cho các phân hệ", False),
        todo("5. Viết Pydantic Models & ORM Entities chuẩn hóa dùng chung toàn hệ thống", False)
    ]

    # Tạo Sub-page Data Center dưới Pentami Core
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"page_id": PENTAMI_CORE_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "💾"},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "Data Center - Trung Tâm Dữ Liệu Toàn Hệ Sinh Thái"}}]
            }
        },
        "children": data_center_blocks[:75]
    }
    res = api_call(url, method="POST", data=payload)
    new_page_id = res["id"]
    print(f"✅ Created Sub-Page: Data Center (ID: {new_page_id})")

    if len(data_center_blocks) > 75:
        append_blocks(new_page_id, data_center_blocks[75:])
        print("✅ Appended all remaining Data Center blocks successfully!")

    print("\n🎉 HOÀN TẤT KHỞI TẠO DATA CENTER TRÊN NOTION!")

if __name__ == "__main__":
    main()
