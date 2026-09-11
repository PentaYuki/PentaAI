"""
Script khởi tạo toàn diện hệ thống Notion Workspace cho Penta AI Ecosystem:
- Cập nhật trang chủ PentaAi system với Phân tích Pentami Core & Bảng Tiến Độ Tổng Thể.
- Tạo các Trang Con (Child Pages) cho từng phân hệ:
  1. Pentami Core
  2. Pentaschool
  3. Pentakuru
  4. Pentamarket
  5. PentaJob
  6. MCP Playwright
- Trong mỗi trang con tích hợp đầy đủ:
  + Mục tiêu & Tầm nhìn
  + Tiến độ & Task list (Todo / In-Progress / Done)
  + Hệ Issue & Rủi ro
  + Kiến trúc Data (Database Schema, Vector, Cache)
  + Giao thức hành động liên phân hệ
"""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PARENT_PAGE_ID = "3d5ec2d5-0cde-8044-a025-c60875a4f00b"
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

def callout(text, emoji="💡"):
    return {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": text}}], "icon": {"type": "emoji", "emoji": emoji}}}

def todo(text, checked=False):
    return {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": text}}], "checked": checked}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def code(content, language="markdown"):
    return {"object": "block", "type": "code", "code": {"rich_text": [{"type": "text", "text": {"content": content}}], "language": language}}

def append_blocks(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    # Chia nhỏ chunk tối đa 100 blocks mỗi request
    for i in range(0, len(blocks), 80):
        chunk = blocks[i:i+80]
        api_call(url, method="PATCH", data={"children": chunk})
        time.sleep(0.5)

def create_child_page(parent_id, title, emoji, blocks):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        "children": blocks[:80] # Khởi tạo tối đa 80 blocks đầu
    }
    res = api_call(url, method="POST", data=payload)
    new_page_id = res["id"]
    print(f"✅ Created page: {title} (ID: {new_page_id})")
    
    # Nếu còn blocks dư, append tiếp
    if len(blocks) > 80:
        append_blocks(new_page_id, blocks[80:])
    return new_page_id

def main():
    print("🚀 Bắt đầu khởi tạo hệ sinh thái Penta AI trên Notion...")
    
    # =========================================================================
    # 1. NỘI DUNG TRANG CHỦ TỔNG THỂ (PARENT PAGE)
    # =========================================================================
    parent_blocks = [
        callout(
            "PENTA AI ECOSYSTEM (PENTAKURUMI) - TRÍ TUỆ NHẬN THỨC ĐA PHÂN HỆ\n"
            "Lấy Pentami Core làm Bộ Não Trung Tâm (Thức Uẩn) điều phối toàn bộ đời sống số: Học tập, Công việc, Thương mại và Quản lý cá nhân.",
            "🌟"
        ),
        h1("1. Phân Tích Bản Chất: Pentami Core Nghĩa Là Gì?"),
        p(
            "Pentami Core KHÔNG PHẢI chỉ là một backend server thông thường, mà là 'HỆ THẦN KINH & Ý THỨC TRUNG TÂM' của toàn bộ hệ sinh thái. "
            "Nó đóng vai trò là điểm hội tụ nhận thức (Thức Uẩn) của con người số:"
        ),
        bullet("🧠 Ý Thức Hợp Nhất: Nắm giữ bộ nhớ dài hạn, trạng thái người dùng xuyên suốt các phân hệ."),
        bullet("🔑 Một Chìa Khóa Cho Toàn Bộ Đời Sống: Định danh duy nhất với Unified API Key (penta_live_sk_...) tra cứu qua Redis < 1ms."),
        bullet("🎭 Giao Thức 3D Sống Động: Không chỉ nhả văn bản chết, mà truyền tải luồng đồng bộ: Cảm xúc (chunk_emo), Thời gian lip-sync (chunk_time), và Hành động thực thi (chunk_action)."),
        bullet("⚡ Vòng Lặp Thoại Tức Thì: Kết nối Deepgram Nova-2 STT và ElevenLabs Streaming TTS đạt độ trễ < 500ms."),
        divider(),
        
        h1("2. Bảng Tiến Độ Tổng Thể Dự Án (Master Progress Tracker)"),
        callout("Tiến độ tổng thể: Sprint 1 - Sprint 5 (Giai đoạn R&D & Kiến trúc nền tảng)", "📊"),
        todo("[Sprint 1] Thiết kế kiến trúc tổng thể & Giao thức 3D Chunks", True),
        todo("[Sprint 1] Chuẩn hóa Unified API Key Manager (HMAC-SHA256 & Scopes)", True),
        todo("[Sprint 1] Thiết lập RAG Service với all-MiniLM-L6-v2 (384 dims)", True),
        todo("[Sprint 2] Triển khai FastAPI Gateway & Redis Token Bucket Rate Limiter", False),
        todo("[Sprint 2] Tích hợp Deepgram Nova-2 STT Streaming & ElevenLabs WebSocket", False),
        todo("[Sprint 3] Xây dựng Server Playwright MCP tự động hóa trình duyệt", False),
        todo("[Sprint 4] Phát triển LMS Pentaschool với Virtual AI Teacher Avatar", False),
        todo("[Sprint 4] Phát triển Desktop Pentakuru lập chỉ mục file cục bộ", False),
        todo("[Sprint 5] Phát triển E-commerce Pentamarket & AI Sales Bot", False),
        todo("[Sprint 5] Phát triển Tuyển dụng PentaJob & AI Mock Interview Voice Room", False),
        divider(),

        h1("3. Trung Tâm Liên Kết Các Phân Hệ (Ecosystem Hub)"),
        p("Nhấp vào từng trang con dưới đây để xem chi tiết tiến độ, danh sách task, hệ thống issue và kiến trúc dữ liệu của từng phân hệ:")
    ]
    
    print("📝 Cập nhật trang chủ tổng thể...")
    append_blocks(PARENT_PAGE_ID, parent_blocks)
    
    # =========================================================================
    # 2. SUB-PAGE 1: PENTAMI CORE (AI BRAIN & GATEWAY)
    # =========================================================================
    pentami_blocks = [
        callout("Bộ Não Trung Tâm & Cổng Định Tuyến Nhận Thức của Hệ Sinh Thái Penta AI", "🧠"),
        h2("1. Mục Tiêu & Trách Nhiệm"),
        bullet("Xác thực API Key dùng chung, phân quyền Scopes (RBAC) với Redis Cache."),
        bullet("Điều phối RAG tri thức qua mô hình all-MiniLM-L6-v2 và Qdrant Vector DB."),
        bullet("Quản lý luồng streaming 3D: chunk_emo, chunk_time, chunk_action."),
        bullet("Điều phối đàm thoại 2 chiều siêu tốc Deepgram STT + ElevenLabs TTS."),
        divider(),
        
        h2("2. Bảng Tiến Độ & Danh Sách Tasks"),
        todo("Định nghĩa schema Pydantic/Dataclasses cho 3D Chunk Protocol", True),
        todo("Xây dựng module UnifiedKeyManager mã hóa HMAC-SHA256", True),
        todo("Cài đặt MiniLMEmbeddingService 384 dimensions", True),
        todo("Tạo FastAPI WebSocket endpoint /v1/chat/stream", False),
        todo("Cấu hình Redis Token Bucket Rate Limiting per API Key", False),
        todo("Tích hợp Voice Pipeline Full-Duplex Audio Buffer", False),
        todo("Viết bộ Router định tuyến Intent sang các phân hệ con", False),
        divider(),

        h2("3. Hệ Thống Issue & Rủi Ro Kỹ Thuật (Issue Tracker)"),
        callout("ISSUE-01: Độ trễ toàn trình Voice Streaming vượt ngưỡng 600ms\n-> Giải pháp: Cắt âm thanh bằng Silero-VAD tại client và stream partial transcript ngay khi có từ đầu tiên.", "⚠️"),
        callout("ISSUE-02: Đồng bộ trạng thái Cache khi thu hồi API Key (Key Revocation)\n-> Giải pháp: Dùng Redis Pub/Sub thông báo tức thời tới toàn bộ worker khi một key bị hủy.", "⚠️"),
        callout("ISSUE-03: Xung đột tài nguyên CPU khi xử lý embedding đồng thời nhiều user\n-> Giải pháp: Đưa tác vụ nhúng vector vào hàng đợi Celery/Redis Streams.", "⚠️"),
        divider(),

        h2("4. Kiến Trúc Dữ Liệu (Data Architecture)"),
        h3("PostgreSQL Tables:"),
        code(
"""CREATE TABLE api_keys (
    key_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    tenant_id VARCHAR(64) NOT NULL,
    key_hash VARCHAR(64) UNIQUE NOT NULL,
    scopes TEXT[] NOT NULL,
    rate_limit_rpm INT DEFAULT 120,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""", "sql"),
        h3("Redis Cache Key Patterns:"),
        bullet("penta:key:{key_hash} -> JSON {user_id, tenant_id, scopes, rate_limit}"),
        bullet("penta:ratelimit:{key_id}:{minute} -> Integer counter (Token bucket)"),
        h3("Qdrant Collections:"),
        bullet("Collection: penta_knowledge (384 dimensions, Cosine metric, Payload: {tenant_id, app_id, doc_id})")
    ]
    create_child_page(PARENT_PAGE_ID, "Pentami Core - AI Brain & Gateway", "🧠", pentami_blocks)

    # =========================================================================
    # 3. SUB-PAGE 2: PENTASCHOOL (LMS & AI TEACHER)
    # =========================================================================
    school_blocks = [
        callout("Hệ Thống LMS Tương Tác Giảng Viên Ảo 2D/3D (AI Virtual Instructor)", "🎓"),
        h2("1. Mục Tiêu & Trách Nhiệm"),
        bullet("Quản lý khóa học, bài giảng video, bài thi trắc nghiệm và đồ án."),
        bullet("AI Teacher Avatar tương tác đàm thoại giọng nói, cử chỉ cảm xúc theo bài giảng."),
        bullet("Tự động cá nhân hóa lộ trình học tập theo điểm yếu của từng học sinh."),
        divider(),

        h2("2. Bảng Tiến Độ & Danh Sách Tasks"),
        todo("Xây dựng kiến trúc thư mục pentaschool Next.js", True),
        todo("Tích hợp Canvas/Three.js hiển thị Avatar AI Virtual Instructor", False),
        todo("Module Lip-sync đọc viseme_code từ chunk_time để chuyển động môi", False),
        todo("Tạo bảng bài tập tương tác kích hoạt tự động qua chunk_action", False),
        todo("Kết nối API Client với pentami-core bằng Unified API Key", False),
        divider(),

        h2("3. Hệ Thống Issue & Rủi Ro Kỹ Thuật (Issue Tracker)"),
        callout("ISSUE-01: Lệch khẩu hình môi và âm thanh bài giảng (Audio-Visual Desync)\n-> Giải pháp: Sử dụng chunk_time làm Master Clock căn chỉnh Web Audio Context.", "⚠️"),
        callout("ISSUE-02: Học sinh hỏi lan man ngoài nội dung bài học\n-> Giải pháp: Giới hạn RAG Context chỉ trong tài liệu của bài học hiện tại.", "⚠️"),
        divider(),

        h2("4. Kiến Trúc Dữ Liệu (Data Architecture)"),
        code(
"""CREATE TABLE courses (
    course_id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_progress (
    user_id VARCHAR(64),
    course_id VARCHAR(64),
    completed_lessons INT DEFAULT 0,
    ai_feedback TEXT,
    PRIMARY KEY(user_id, course_id)
);""", "sql")
    ]
    create_child_page(PARENT_PAGE_ID, "Pentaschool - LMS & AI Teacher", "🎓", school_blocks)

    # =========================================================================
    # 4. SUB-PAGE 3: PENTAKURU (LOCAL FILE KNOWLEDGE ASSISTANT)
    # =========================================================================
    kuru_blocks = [
        callout("Ứng Dụng Desktop Tự Động Hóa Quản Lý Tệp Tin & Ghi Chú RAG Nhanh", "📂"),
        h2("1. Mục Tiêu & Trách Nhiệm"),
        bullet("Quét và theo dõi thư mục người dùng chỉ định (PDF, DOCX, Code, Markdown)."),
        bullet("Tự động tóm tắt tệp tin, trích xuất siêu dữ liệu và tạo cặp Q&A ban đầu."),
        bullet("Tìm kiếm ngữ nghĩa tức thì (Semantic Search) ngay trên máy tính cá nhân."),
        bullet("Đồng bộ dữ liệu tri thức lên pentami-core khi có kết nối mạng."),
        divider(),

        h2("2. Bảng Tiến Độ & Danh Sách Tasks"),
        todo("Thiết lập kiến trúc Pentakuru và README đặc tả", True),
        todo("Cài đặt Tauri App với Rust backend và React/Vite UI", False),
        todo("Xây dựng File Watcher (theo dõi file tạo mới/chỉnh sửa)", False),
        todo("Tích hợp LanceDB / SQLite-VSS lưu trữ vector cục bộ", False),
        todo("Xây dựng giao diện phím tắt toàn cục (Global Hotkey Quick Search)", False),
        todo("Đồng bộ hóa tri thức lên Pentami Core với Scopes penta:kuru:sync", False),
        divider(),

        h2("3. Hệ Thống Issue & Rủi Ro Kỹ Thuật (Issue Tracker)"),
        callout("ISSUE-01: Tệp PDF dung lượng lớn (hàng trăm trang) làm nghẽn RAM máy khách\n-> Giải pháp: Sử dụng Streaming Chunking xử lý từng trang và giải phóng bộ nhớ ngay lập tức.", "⚠️"),
        callout("ISSUE-02: Quyền riêng tư của tệp tin nhạy cảm của người dùng\n-> Giải pháp: Cho phép người dùng chọn chế độ 'Local Only' - không đồng bộ vector lên cloud.", "⚠️"),
        divider(),

        h2("4. Kiến Trúc Dữ Liệu Cục Bộ (Local Data Architecture)"),
        code(
"""-- SQLite Local Metadata DB
CREATE TABLE indexed_files (
    file_path TEXT PRIMARY KEY,
    file_hash TEXT NOT NULL,
    file_size INTEGER,
    summary TEXT,
    last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_status TEXT DEFAULT 'pending'
);""", "sql")
    ]
    create_child_page(PARENT_PAGE_ID, "Pentakuru - Local File Knowledge Assistant", "📂", kuru_blocks)

    # =========================================================================
    # 5. SUB-PAGE 4: PENTAMARKET (E-COMMERCE & AI SALES CONSULTANT)
    # =========================================================================
    market_blocks = [
        callout("Sàn Thương Mại Điện Tử & Hệ Thống Bán Hàng Tích Hợp AI Sales Consultant 24/7", "🛒"),
        h2("1. Mục Tiêu & Trách Nhiệm"),
        bullet("Gian hàng sản phẩm, dịch vụ và khóa học trong toàn bộ hệ sinh thái Penta."),
        bullet("AI Sales Bot am hiểu sản phẩm, tư vấn trực tiếp qua chat và giọng nói."),
        bullet("Tự động tạo giỏ hàng và áp dụng mã khuyến mãi qua chunk_action."),
        divider(),

        h2("2. Bảng Tiến Độ & Danh Sách Tasks"),
        todo("Thiết lập cấu trúc thư mục pentamarket", True),
        todo("Xây dựng Catalog sản phẩm và danh mục hàng hóa", False),
        todo("Huấn luyện System Prompt cho AI Sales Agent hiểu tâm lý khách", False),
        todo("Tích hợp chunk_action: add_to_cart và apply_discount", False),
        todo("Tích hợp cổng thanh toán trực tuyến bảo mật", False),
        divider(),

        h2("3. Hệ Thống Issue & Rủi Ro Kỹ Thuật (Issue Tracker)"),
        callout("ISSUE-01: AI báo sai giá hoặc cam kết khống tính năng sản phẩm (Hallucination)\n-> Giải pháp: Ràng buộc chặt chẽ tham số giá từ DB PostgreSQL, cấm LLM tự suy diễn giá.", "⚠️"),
        callout("ISSUE-02: Tự động tạo đơn hàng không mong muốn khi nhận diện nhầm ý định người dùng\n-> Giải pháp: Bắt buộc gắn cờ require_user_confirmation=True trong chunk_action.", "⚠️"),
        divider(),

        h2("4. Kiến Trúc Dữ Liệu (Data Architecture)"),
        code(
"""CREATE TABLE products (
    product_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(12, 2) NOT NULL,
    stock INT DEFAULT 0,
    specs JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(32) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""", "sql")
    ]
    create_child_page(PARENT_PAGE_ID, "Pentamarket - E-commerce & AI Sales", "🛒", market_blocks)

    # =========================================================================
    # 6. SUB-PAGE 5: PENTAJOB (AI RECRUITMENT & MOCK INTERVIEW)
    # =========================================================================
    job_blocks = [
        callout("Hệ Thống Tuyển Dụng Thông Minh, So Khớp Kỹ Năng & Phỏng Vấn AI", "💼"),
        h2("1. Mục Tiêu & Trách Nhiệm"),
        bullet("Tự động bóc tách kỹ năng, kinh nghiệm từ CV của ứng viên (PDF/Word)."),
        bullet("So khớp ngữ nghĩa giữa hồ sơ ứng viên và mô tả công việc (JD) bằng vector MiniLM."),
        bullet("Phòng phỏng vấn thử nghiệm bằng giọng nói real-time chấm điểm kỹ năng ứng viên."),
        bullet("Liên thông gợi ý khóa học thiếu hụt trên Pentaschool."),
        divider(),

        h2("2. Bảng Tiến Độ & Danh Sách Tasks"),
        todo("Thiết lập cấu trúc thư mục pentajob", True),
        todo("Xây dựng module AI Resume Parser trích xuất kỹ năng", False),
        todo("Xây dựng thuật toán Semantic Job Matching với độ tương đồng cosine", False),
        todo("Xây dựng phòng phỏng vấn giọng nói AI Interview Room với Voice Hub", False),
        todo("Hệ thống tự động sinh báo cáo đánh giá phỏng vấn (Interview Scorecard)", False),
        divider(),

        h2("3. Hệ Thống Issue & Rủi Ro Kỹ Thuật (Issue Tracker)"),
        callout("ISSUE-01: Định dạng CV quá phức tạp làm sai lệch dữ liệu kỹ năng\n-> Giải pháp: Kết hợp Vision OCR với mô hình ngôn ngữ bóc tách có cấu trúc (JSON Schema Output).", "⚠️"),
        callout("ISSUE-02: Đánh giá phỏng vấn mang tính máy móc, thiếu tự nhiên\n-> Giải pháp: Bổ sung chunk_emo khích lệ, đặt các câu hỏi phản biện mở dựa trên câu trả lời trước.", "⚠️"),
        divider(),

        h2("4. Kiến Trúc Dữ Liệu (Data Architecture)"),
        code(
"""CREATE TABLE job_postings (
    job_id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    requirements TEXT NOT NULL,
    salary_range VARCHAR(64),
    status VARCHAR(32) DEFAULT 'open'
);

CREATE TABLE interview_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    candidate_id VARCHAR(64) NOT NULL,
    job_id VARCHAR(64) NOT NULL,
    overall_score INT,
    strengths TEXT[],
    improvements TEXT[],
    transcript TEXT
);""", "sql")
    ]
    create_child_page(PARENT_PAGE_ID, "PentaJob - AI Talent & Mock Interview", "💼", job_blocks)

    # =========================================================================
    # 7. SUB-PAGE 6: MCP PLAYWRIGHT (BROWSER AUTOMATION SERVER)
    # =========================================================================
    playwright_blocks = [
        callout("Server Tự Động Hóa Trình Duyệt Web Theo Chuẩn Model Context Protocol (MCP)", "🌐"),
        h2("1. Mục Tiêu & Trách Nhiệm"),
        bullet("Cung cấp 'Đôi bàn tay' cho AI Agent tự động thao tác trên web."),
        bullet("Bảo vệ an toàn bằng Chromium context cô lập theo phiên của từng người dùng."),
        bullet("Hỗ trợ các công cụ: navigate, click, fill, screenshot, extract_text."),
        divider(),

        h2("2. Bảng Tiến Độ & Danh Sách Tasks"),
        todo("Viết mã nguồn controller MCP Playwright trong mcp-playwright/src/server.py", True),
        todo("Tích hợp giao thức JSON-RPC qua stdio và Server-Sent Events (SSE)", False),
        todo("Cơ chế mã hóa và lưu trữ Cookie / Session người dùng an toàn", False),
        todo("Xây dựng Whitelist URL chỉ cho phép truy cập các trang web được phê duyệt", False),
        todo("Tích hợp Vision LLM tự động phân tích ảnh chụp màn hình", False),
        divider(),

        h2("3. Hệ Thống Issue & Rủi Ro Kỹ Thuật (Issue Tracker)"),
        callout("ISSUE-01: Trang web bên ngoài chặn bot tự động (Cloudflare / CAPTCHA)\n-> Giải pháp: Cấu hình stealth mode cho Playwright và cơ chế bàn giao quyền điều khiển tạm thời cho người dùng (Human-in-the-loop).", "⚠️"),
        callout("ISSUE-02: Rò rỉ thông tin cá nhân hoặc thao tác ngoài ý muốn trên web\n-> Giải pháp: Bắt buộc quyền đặc biệt action:playwright:execute và xác nhận cấp 2.", "⚠️"),
        divider(),

        h2("4. Kiến Trúc Session Sandbox"),
        bullet("Session Lifecycle: Khởi tạo khi user ra lệnh -> Mở context biệt lập -> Lưu cookie mã hóa -> Tự động đóng sau 15 phút không hoạt động."),
        bullet("Audit Log: Ghi log toàn bộ lịch sử click, điền form vào PostgreSQL phục vụ kiểm toán bảo mật.")
    ]
    create_child_page(PARENT_PAGE_ID, "MCP Playwright - Browser Automation", "🌐", playwright_blocks)

    print("\n🎉 HOÀN TẤT! Đã đồng bộ toàn bộ hệ sinh thái lên trang Notion!")

if __name__ == "__main__":
    main()
