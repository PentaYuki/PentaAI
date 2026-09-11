"""
Script tạo Trang Dự Án Đầu Tiên (Phase 1):
"Dự Án 1: Pentami Core - Bộ Não Điều Phối & Quản Lý Tri Thức RAG"
lên hệ thống Notion Workspace của Penta AI Ecosystem.
Gồm đầy đủ:
- Tên dự án & Mục tiêu cốt lõi
- Giải thích chi tiết tại sao phải làm dự án này trước tiên (5 luận điểm kiến trúc)
- Các bước thực hiện chi tiết (theo chuẩn Guru Factory & Knowledge/Storage Rule)
- Bảng công việc (Action Tasks & To-Do List)
- Tiêu chí nghiệm thu & Mã lệnh chạy thử
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

def text_span(content, bold=False, italic=False, code=False, color="default"):
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "strikethrough": False,
            "underline": False,
            "code": code,
            "color": color
        }
    }

def h1(title):
    return {
        "object": "block",
        "type": "heading_1",
        "heading_1": {"rich_text": [text_span(title, bold=True)]}
    }

def h2(title):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [text_span(title, bold=True)]}
    }

def h3(title):
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": [text_span(title, bold=True)]}
    }

def p(spans):
    if isinstance(spans, str):
        spans = [text_span(spans)]
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": spans}
    }

def callout(spans, emoji="💡", color="default"):
    if isinstance(spans, str):
        spans = [text_span(spans)]
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": spans,
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color
        }
    }

def bullet(spans):
    if isinstance(spans, str):
        spans = [text_span(spans)]
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": spans}
    }

def numbered(spans):
    if isinstance(spans, str):
        spans = [text_span(spans)]
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": spans}
    }

def todo(text, checked=False):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [text_span(text)],
            "checked": checked
        }
    }

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def code_block(code, language="python"):
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [text_span(code)],
            "language": language
        }
    }

def build_project_page_blocks():
    blocks = []
    
    # Header Banner Callout
    blocks.append(callout([
        text_span("🚀 DỰ ÁN GIAI ĐOẠN 1 (ƯU TIÊN SỐ 1 TOÀN HỆ THỐNG)\n", bold=True, color="blue"),
        text_span("Tên Dự Án: ", bold=True),
        text_span("PENTAMI CORE - BỘ NÃO ĐIỀU PHỐI TRUNG TÂM & QUẢN LÝ TRI THỨC RAG\n"),
        text_span("Mục Tiêu Tối Thượng: ", bold=True),
        text_span("Xây dựng cột sống trung tâm, chuẩn hóa bộ nhớ lưu trữ tri thức RAG, chuẩn hóa intent 100% tiếng Việt không dấu, và cung cấp gateway xác thực tốc độ cao cho toàn bộ các phân hệ vệ tinh.")
    ], emoji="🎯", color="blue_background"))
    
    blocks.append(divider())
    
    # PHẦN 1: GIẢI THÍCH TẠI SAO LÀM TRƯỚC
    blocks.append(h1("🏛️ PHẦN 1: TẠI SAO PHẢI XÂY DỰNG PENTAMI CORE TRƯỚC TIÊN?"))
    blocks.append(p([
        text_span("Trong kiến trúc hệ thống phân tán và trí tuệ nhân tạo, việc lựa chọn module khởi đầu quyết định 90% sự thành bại của toàn bộ dự án. Dưới đây là "),
        text_span("5 lý do kiến trúc cốt lõi", bold=True, color="red"),
        text_span(" giải thích vì sao "),
        text_span("Pentami Core", bold=True),
        text_span(" bắt buộc phải là viên gạch đầu tiên được đặt xuống:")
    ]))
    
    blocks.append(callout([
        text_span("1. Nguyên Lý 'Hệ Thần Kinh Trung Ương' (Central Nervous System First)\n", bold=True),
        text_span("Toàn bộ hệ sinh thái gồm các phân hệ chuyên trách: Pentaschool (Giáo dục), Pentakuru (File máy tính), Pentamarket (Thương mại), PentaJob (Việc làm) và MCP Playwright (Web Action). Tất cả các phân hệ này là các 'chi thể' vệ tinh. Nếu không có 'Bộ Não' (Pentami Core) tiếp nhận yêu cầu, phân loại và điều phối thì các chi thể hoàn toàn bất động và không thể tự nói chuyện với nhau. Việc xây dựng Pentami Core trước cung cấp điểm tựa cho mọi API sau này.")
    ], emoji="🧠", color="gray_background"))
    
    blocks.append(callout([
        text_span("2. Quản Lý Tri Thức RAG & Hạn Chế Ảo Giác (Knowledge RAG & Grounding)\n", bold=True),
        text_span("Lõi giá trị của Pentaschool, Pentakuru và Pentanote là cung cấp thông tin, bài giảng và tài liệu chính xác. Bộ nhớ ngữ cảnh và vector RAG tại Pentami Core được thiết kế để nạp dữ liệu và làm giàu tri thức có căn cứ, giảm thiểu tối đa ảo giác thông tin từ mô hình ngôn ngữ.")
    ], emoji="⚖️", color="blue_background"))
    
    blocks.append(callout([
        text_span("3. Kháng Lỗi Tiếng Việt Tuyệt Đối (100% Unaccented & Slang Robustness)\n", bold=True),
        text_span("Thực tế người dùng Việt Nam gõ câu hỏi thường xuyên không dấu ('hoc bai toan lop 5', 'tim file bao cao thang 8', 'tinh gia thue vat'). Nếu Intent Router chưa được huấn luyện và kiểm thử chịu tải trên tập 1,000 mẫu câu chuẩn hóa thì hệ thống sẽ định tuyến sai phân hệ ngay từ cửa ngõ. Hoàn thiện Intent Router ở Pentami Core đảm bảo cửa ngõ vững chắc.")
    ], emoji="🌐", color="green_background"))
    
    blocks.append(callout([
        text_span("4. Trục Bảo Mật Unified Key & Đa Thuê Bao Dưới 1ms (Multi-tenancy Security)\n", bold=True),
        text_span("Khóa 'penta_live_sk_...' được băm HMAC-SHA256 và cache trên Redis cho tốc độ tra cứu < 1ms, kèm theo phân quyền RBAC và cách ly tenant_id. Nếu các phân hệ vệ tinh được code trước mà không có chuẩn bảo mật này, toàn bộ mã nguồn sẽ phải đập đi sửa lại để gắn middleware xác thực.")
    ], emoji="🔐", color="yellow_background"))
    
    blocks.append(callout([
        text_span("5. Khóa Hợp Đồng Giao Thức PUASP (Protocol for Unified Audio, Stream & Persona)\n", bold=True),
        text_span("Pentami Core định hình cấu trúc phản hồi thời gian thực: 'chunk_emo' (cảm xúc avatar), 'chunk_time' (lip-sync mili-giây) và 'chunk_action' (lệnh Playwright) qua 3 nhân cách (Cute, Serious, Yandere). Khi hợp đồng dữ liệu này cố định, các team làm giao diện Web UI, 3D Avatar hoặc Playwright chỉ việc 'plug-and-play' mà không lo vỡ định dạng.")
    ], emoji="🎭", color="purple_background"))
    
    blocks.append(divider())
    
    # PHẦN 2: CÁC BƯỚC THỰC HIỆN CHI TIẾT
    blocks.append(h1("🛠️ PHẦN 2: CÁC BƯỚC THỰC HIỆN DỰ ÁN CHI TIẾT (IMPLEMENTATION ROADMAP)"))
    blocks.append(p([
        text_span("Quá trình thực thi tuân thủ nghiêm ngặt mô hình "),
        text_span("Guru Factory Pattern", bold=True, code=True),
        text_span(" (Tách biệt Interface - Implementation - Factory - Registry) và "),
        text_span("Cơ Chế Phân Luồng Kép (Dual-Path Q&A Rule)", bold=True, code=True),
        text_span(" theo quy tắc kiến trúc GEMINI.md:")
    ]))
    
    # BƯỚC 1
    blocks.append(h2("📍 Bước 1: Khởi Tạo Cụm Hạ Tầng Độc Lập (Infrastructure Layer)"))
    blocks.append(bullet([text_span("Triển khai cụm Docker Compose: PostgreSQL 16 (Lưu trữ API Keys, Users, Tenants), Redis 7.2 (Cache xác thực < 1ms & Token Bucket Rate Limiting), Qdrant Vector DB (Lưu trữ Embeddings 384 dimensions).")]))
    blocks.append(bullet([text_span("Cấu hình file biến môi trường "), text_span(".env", code=True), text_span(" bảo mật master secret, ports và pool connections.")]))
    blocks.append(bullet([text_span("Chạy lệnh kiểm tra kết nối & tạo bảng (Migration DB, Healthcheck Ping).")]))
    blocks.append(code_block("cd /Users/gooleseswsq1gmail.com/Documents/pentaAI/deploy\ndocker compose up -d\npython3 -c 'import redis; r = redis.Redis(); print(\"Redis Ping:\", r.ping())'", "bash"))
    
    # BƯỚC 2
    blocks.append(h2("📍 Bước 2: Xây Dựng Module Bảo Mật UnifiedKeyManager theo Chuẩn Guru Factory"))
    blocks.append(bullet([text_span("Tầng Interface: "), text_span("pentami-core/auth/interface.py", code=True), text_span(" định nghĩa IKeyManager, IScopeChecker, IRateLimiter.")]))
    blocks.append(bullet([text_span("Tầng Implementation: "), text_span("pentami-core/auth/implementation.py", code=True), text_span(" thực thi băm HMAC-SHA256, tra cứu Redis Cache dưới 1ms, sinh Ephemeral JWT 60s.")]))
    blocks.append(bullet([text_span("Tầng Factory: "), text_span("pentami-core/auth/factory.py", code=True), text_span(" inject Redis client, DB session và secret config.")]))
    blocks.append(bullet([text_span("Tầng Registry: "), text_span("pentami-core/auth/registry.py", code=True), text_span(" đăng ký Auth Service vào Gateway Dependency Container.")]))
    blocks.append(todo("Viết mã nguồn 4 tầng auth theo chuẩn Guru Factory", checked=False))
    blocks.append(todo("Unit test xác thực key và đo lường latency Redis < 1ms", checked=False))
    
    # BƯỚC 3
    blocks.append(h2("📍 Bước 3: Xây Dựng Bộ Phân Loại Ý Định Kháng Lỗi Tiếng Việt (Intent Router)"))
    blocks.append(bullet([text_span("Tầng Tiền Xử Lý: "), text_span("pentami-core/router/normalizer.py", code=True), text_span(" loại bỏ dấu tiếng Việt, chuẩn hóa teencode và từ lóng học đường.")]))
    blocks.append(bullet([text_span("Tầng Phân Loại: "), text_span("pentami-core/router/implementation.py", code=True), text_span(" định tuyến chính xác vào 5 phân hệ: pentaschool, pentakuru, pentamarket, pentajob, mcp_playwright.")]))
    blocks.append(bullet([text_span("Benchmark Dataset: Nạp 1,000 mẫu câu đa dạng từ "), text_span("master_intent_1000.json", code=True), text_span(" để đo tỷ lệ chính xác.")]))
    blocks.append(todo("Xây dựng Unaccented Normalizer đạt 100% kháng lỗi tiếng Việt", checked=False))
    blocks.append(todo("Tích hợp Intent Router Factory & Registry vào Pentami Core", checked=False))
    
    # BƯỚC 4
    blocks.append(h2("📍 Bước 4: Xây Dựng Cơ Chế Quản Lý Bộ Nhớ & Vector RAG (Memory & Knowledge Engine)"))
    blocks.append(callout([
        text_span("NGUYÊN TẮC QUẢN LÝ TRI THỨC: ", bold=True, color="blue"),
        text_span("Bộ nhớ ngữ cảnh và Qdrant Vector RAG hoạt động đồng bộ để cung cấp thông tin chính xác, hạn chế ảo giác và duy trì ngữ cảnh đa lượt hội thoại.")
    ], emoji="🧠", color="blue_background"))
    blocks.append(bullet([text_span("Semantic Memory: Lưu trữ cửa sổ trượt hội thoại và giải quyết câu hỏi ngữ cảnh đa lượt.")]))
    blocks.append(bullet([text_span("Vector Embedding: Tích hợp mô hình "), text_span("sentence-transformers/all-MiniLM-L6-v2", code=True), text_span(" để sinh vector 384 dimensions.")]))
    blocks.append(bullet([text_span("Qdrant Search: Truy vấn tri thức tài liệu theo độ tương đồng ngữ nghĩa (Cosine Similarity).")]))
    blocks.append(todo("Xây dựng Memory Interface & Implementation", checked=False))
    blocks.append(todo("Tích hợp Qdrant Vector Client và Embedding Service", checked=False))
    blocks.append(todo("Benchmark kiểm thử truy vấn RAG độ trễ < 50ms", checked=False))
    
    # BƯỚC 5
    blocks.append(h2("📍 Bước 5: Đóng Gói Giao Thức Stream PUASP & 3 Nhân Cách AI"))
    blocks.append(bullet([text_span("LLM Đóng Vai Trò Phát Ngôn Viên: Tiếp nhận context RAG từ Qdrant và bộ nhớ hội thoại, sau đó biên soạn câu trả lời tự nhiên theo tính cách.")]))
    blocks.append(bullet([text_span("3 Nhân Cách: "), text_span("Cute (Đáng yêu, hỗ trợ tận tâm) | Serious (Nghiêm túc, chuẩn mực sư phạm) | Yandere (Chiếm hữu, gắn kết tri thức mãnh liệt).", italic=True)]))
    blocks.append(bullet([text_span("Cấu trúc PentaStreamEnvelope: Đóng gói JSON stream chứa: "), text_span("chunk_emo (hoạt ảnh), chunk_time (lip-sync TTS), chunk_action (lệnh Playwright tách biệt).", code=True)]))
    blocks.append(bullet([text_span("FastAPI Endpoint: Tạo WebSocket "), text_span("/v1/chat/stream", code=True), text_span(" phục vụ kết nối trực tiếp với Client.")]))
    blocks.append(todo("Tạo Persona Speech Formatter nạp 3 dataset 500 câu", checked=False))
    blocks.append(todo("Tạo WebSocket endpoint streaming PUASP", checked=False))
    
    # BƯỚC 6
    blocks.append(h2("📍 Bước 6: Bộ Kiểm Thử Tự Động Toàn Diện & Tiêu Chí Nghiệm Thu (Verification)"))
    blocks.append(p([text_span("Bộ kiểm thử tự động xác nhận hệ thống sẵn sàng trước khi kết nối với các phân hệ vệ tinh:")]))
    blocks.append(callout([
        text_span("BẢNG TIÊU CHÍ NGHIỆM THU (ACCEPTANCE CRITERIA):\n", bold=True),
        text_span("✅ TC1: Unaccented Intent Recognition đạt độ chính xác > 98% trên 1,000 mẫu câu.\n"),
        text_span("✅ TC2: Semantic Memory & Vector RAG truy vấn chính xác dưới 50ms.\n"),
        text_span("✅ TC3: Unified Key Authentication qua Redis đạt độ trễ trung bình < 1ms.\n"),
        text_span("✅ TC4: Giao thức PUASP streaming trả về đúng định dạng chunk_emo và chunk_action an toàn.\n"),
        text_span("✅ TC5: Mã nguồn tuân thủ 100% chuẩn Guru Factory (không cross-import trực tiếp).")
    ], emoji="📋", color="green_background"))
    blocks.append(code_block("pytest pentami-core/tests/test_auth.py\npytest pentami-core/tests/test_intent_normalizer.py\npytest pentami-core/tests/test_core_components.py\npytest pentami-core/tests/test_puasp_stream.py", "bash"))
    
    blocks.append(divider())
    
    # PHẦN 3: KẾT LUẬN & LIÊN KẾT BƯỚC KẾ TIẾP
    blocks.append(h1("🚀 KẾT LUẬN & BƯỚC TIẾP THEO"))
    blocks.append(p([
        text_span("Khi Dự án Giai Đoạn 1 (Pentami Core) hoàn thành, toàn bộ hệ sinh thái Penta AI sẽ sở hữu một "),
        text_span("Bộ Não Trung Ương vững như bàn thạch", bold=True),
        text_span(". Từ đây, việc triển khai "),
        text_span("Pentaschool (LMS), Pentakuru (Phân tích file), Pentanote, Pentamarket, PentaJob", bold=True),
        text_span(" sẽ diễn ra cực kỳ nhanh chóng và an toàn vì các phân hệ chỉ việc kết nối vào Gateway thông qua hợp đồng chuẩn.")
    ]))
    
    return blocks

def main():
    print("[1] Kiểm tra trang chính PentaAi system...")
    
    # Tạo Trang Con Dự Án 1
    page_data = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🚀"},
        "properties": {
            "title": {
                "title": [
                    {"type": "text", "text": {"content": "🚀 DỰ ÁN 1 (KHỞI ĐẦU): PENTAMI CORE & QUẢN LÝ TRI THỨC RAG"}}
                ]
            }
        }
    }
    
    print("[2] Tạo Child Page trên Notion...")
    res = api_call("https://api.notion.com/v1/pages", method="POST", data=page_data)
    if not res or "id" not in res:
        print("[ERROR] Không thể tạo Child Page:", res)
        return
    
    new_page_id = res["id"]
    new_page_url = res.get("url", "")
    print(f"[SUCCESS] Đã tạo Child Page thành công: ID = {new_page_id}")
    print(f"URL: {new_page_url}")
    
    # Nạp nội dung chi tiết
    blocks = build_project_page_blocks()
    print(f"[3] Đang nạp {len(blocks)} blocks nội dung chi tiết vào trang dự án...")
    
    # Gửi theo batch 100 blocks
    for i in range(0, len(blocks), 80):
        batch = blocks[i:i+80]
        append_data = {"children": batch}
        api_call(f"https://api.notion.com/v1/blocks/{new_page_id}/children", method="PATCH", data=append_data)
        print(f"    -> Đã nạp batch {i//80 + 1} ({len(batch)} blocks)")
        time.sleep(0.5)
        
    print("[4] Đang gắn Callout liên kết nổi bật lên Master Page...")
    # Thêm một Callout ở đầu Master Page thông báo Dự án 1 đang được thực hiện
    master_notice = [
        callout([
            text_span("🎯 DỰ ÁN ĐANG THỰC HIỆN TRƯỚC TIÊN: ", bold=True, color="blue"),
            text_span("GIAI ĐOẠN 1 - PENTAMI CORE & QUẢN LÝ TRI THỨC RAG\n", bold=True),
            text_span("Hệ thống đã xác định Pentami Core là phân hệ trọng tâm cần xây dựng đầu tiên. Nhấp vào trang con bên dưới để xem chi tiết lộ trình và giải thích lý do kiến trúc: "),
            text_span("Xem Chi Tiết Dự Án 1 ➔", bold=True, color="blue")
        ], emoji="🚀", color="blue_background")
    ]
    api_call(f"https://api.notion.com/v1/blocks/{PARENT_PAGE_ID}/children", method="PATCH", data={"children": master_notice})
    
    print("\n=======================================================")
    print("HOÀN TẤT TẠO DỰ ÁN ĐẦU TIÊN LÊN NOTION THÀNH CÔNG!")
    print(f"Trang Dự Án 1: {new_page_url}")
    print("=======================================================")

if __name__ == "__main__":
    main()
