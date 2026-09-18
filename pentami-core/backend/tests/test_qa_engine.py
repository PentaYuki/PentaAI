import pytest
import asyncio
import httpx
import sys
from pathlib import Path

# Thêm root dir và backend dir vào sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import (
    app,
    USERS_DB,
    EMAIL_TO_USER_ID,
    LIFETIME_LEDGERS_DB,
    CLASSROOMS_DB,
    CLASSROOM_CODE_TO_ID,
)
from qa_engine import SlotResolver, KnowledgeBase, QAEngine, qa_engine
from shared.models.user import UserLifetimeLedger, LearningStyleLER, UserRole


class SyncTestClient:
    """Helper client tương thích ASGI FastAPI"""
    def __init__(self, asgi_app):
        self.app = asgi_app
        self.base_url = "http://testserver"

    def _run(self, coro):
        return asyncio.run(coro)

    def get(self, url, headers=None):
        async def _req():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url=self.base_url) as ac:
                return await ac.get(url, headers=headers)
        return self._run(_req())

    def post(self, url, json=None, params=None, headers=None):
        async def _req():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url=self.base_url) as ac:
                return await ac.post(url, json=json, params=params, headers=headers)
        return self._run(_req())


client = SyncTestClient(app)


@pytest.fixture(autouse=True)
def clean_all_stores():
    USERS_DB.clear()
    EMAIL_TO_USER_ID.clear()
    LIFETIME_LEDGERS_DB.clear()
    CLASSROOMS_DB.clear()
    CLASSROOM_CODE_TO_ID.clear()
    qa_engine.reset()
    yield
    USERS_DB.clear()
    EMAIL_TO_USER_ID.clear()
    LIFETIME_LEDGERS_DB.clear()
    CLASSROOMS_DB.clear()
    CLASSROOM_CODE_TO_ID.clear()
    qa_engine.reset()


# ==========================================
# 1. Unit Tests for Slot Resolver & Calculations
# ==========================================
def test_slot_resolver_avg_and_color_conditions():
    resolver = SlotResolver()
    
    # Tạo mock User có nguy cơ tụt hậu cao (at_risk_score = 0.85)
    user_high_risk = UserLifetimeLedger(
        user_id="usr_001",
        penta_id="PID-2026-RISK",
        email="risk@penta.vn",
        full_name="Nguyễn Văn Cần Cố Gắng",
        ler_profile=LearningStyleLER(
            primary_style="visual",
            learning_speed=0.8,
            at_risk_score=0.85
        )
    )
    
    template = "Chào [STUDENT_NAME]! Điểm trung bình là [AVG]. Màu trạng thái: [STATUS_COLOR]. Đề xuất: [LER_ACTION]."
    
    # 1. Test tính toán [AVG] từ danh sách điểm [7.0, 8.0, 9.0] -> 8.0
    context = {"scores": [7.0, 8.0, 9.0]}
    resolved = resolver.resolve(template, user=user_high_risk, context=context)
    
    assert "Nguyễn Văn Cần Cố Gắng" in resolved
    assert "8.0" in resolved
    assert "Đỏ" in resolved  # Vì at_risk_score = 0.85 >= 0.7
    assert "Mindmap" in resolved or "sơ đồ" in resolved.lower()


def test_slot_resolver_good_student_color():
    resolver = SlotResolver()
    user_good = UserLifetimeLedger(
        user_id="usr_002",
        penta_id="PID-2026-GOOD",
        email="good@penta.vn",
        full_name="Lê Minh Giỏi",
        ler_profile=LearningStyleLER(
            primary_style="auditory",
            learning_speed=1.5,
            at_risk_score=0.1
        )
    )
    
    template = "Học sinh: [STUDENT_NAME] | [ALERT_BADGE] | [STATUS_COLOR]"
    resolved = resolver.resolve(template, user=user_good)
    
    assert "Lê Minh Giỏi" in resolved
    assert "Xanh lá" in resolved
    assert "HOẠT ĐỘNG TỐT" in resolved


# ==========================================
# 2. Unit Tests for Knowledge Base & Self-Learning
# ==========================================
def test_knowledge_base_lookup_and_harvest():
    kb = KnowledgeBase()
    
    # 1. Tra cứu câu hỏi lịch sử có sẵn
    lookup_dp = kb.lookup("Chiến dịch Điện Biên Phủ diễn ra ngày nào?")
    assert lookup_dp is not None
    assert "1954" in lookup_dp[1]
    
    lookup_dc = kb.lookup("Tại sao lại chọn phương châm đánh chắc tiến chắc?")
    assert lookup_dc is not None
    assert "Võ Nguyên Giáp" in lookup_dc[1]
    
    # 2. Tự động nạp kiến thức mới (Harvesting)
    initial_count = kb.total_entries
    new_query = "Nguyên lý định luật Vạn vật hấp dẫn của Newton"
    new_answer = "Mọi vật trong vũ trụ đều hút nhau với một lực tỉ lệ thuận với tích hai khối lượng và tỉ lệ nghịch với bình phương khoảng cách."
    
    harvested_key = kb.harvest_knowledge(new_query, new_answer, subject="Vật lý")
    assert kb.total_entries == initial_count + 1
    
    # 3. Lần sau tra cứu câu mới nạp -> Tìm thấy ngay
    second_lookup = kb.lookup("Cho em hỏi về định luật vạn vật hấp dẫn")
    assert second_lookup is not None
    assert "khối lượng" in second_lookup[1]


# ==========================================
# 3. Integration Tests for P2P Classroom Management
# ==========================================
def test_p2p_classroom_creation_and_invitation():
    # 1. Đăng ký User A (Sẽ làm Host/Giáo viên lớp học)
    res_a = client.post("/api/auth/register", json={
        "email": "host_user@penta.vn",
        "password": "Password123!",
        "full_name": "Nguyễn Hoàng Thầy Giáo Tạm Thời"
    })
    token_a = res_a.json()["access_token"]
    user_a_id = res_a.json()["user_id"]
    
    # 2. Đăng ký User B (Học sinh tham gia lớp)
    res_b = client.post("/api/auth/register", json={
        "email": "student_b@penta.vn",
        "password": "Password123!",
        "full_name": "Trần Thị Bạn Học"
    })
    token_b = res_b.json()["access_token"]
    user_b_id = res_b.json()["user_id"]
    
    # 3. User A tự tạo phòng học "Nhóm Ôn Thi Lịch Sử 12"
    headers_a = {"Authorization": f"Bearer {token_a}"}
    create_res = client.post("/api/classrooms", json={
        "name": "Nhóm Ôn Thi Lịch Sử 12",
        "subject": "Lịch sử Việt Nam",
        "description": "Cùng nhau ôn tập chiến dịch Điện Biên Phủ"
    }, headers=headers_a)
    assert create_res.status_code == 201
    cls_data = create_res.json()
    code = cls_data["code"]
    assert code.startswith("CLS-")
    assert cls_data["is_host"] is True
    assert cls_data["host_user_id"] == user_a_id
    
    # 4. User B dùng mã mời `code` để tham gia phòng
    headers_b = {"Authorization": f"Bearer {token_b}"}
    join_res = client.post("/api/classrooms/join", json={"code": code}, headers=headers_b)
    assert join_res.status_code == 200
    join_data = join_res.json()
    assert join_data["total_members"] == 2
    assert join_data["is_host"] is False
    
    # 5. Kiểm tra danh sách lớp học của User A và User B
    my_a = client.get("/api/classrooms/my", headers=headers_a).json()
    assert len(my_a["hosted"]) == 1
    assert my_a["hosted"][0]["code"] == code
    
    my_b = client.get("/api/classrooms/my", headers=headers_b).json()
    assert len(my_b["joined"]) == 1
    assert my_b["joined"][0]["code"] == code


# ==========================================
# 4. Integration Tests for QA Chatbot Engine with Learning Loop
# ==========================================
def test_qa_chat_historical_and_self_learning_loop():
    # 1. Đăng ký học sinh
    reg = client.post("/api/auth/register", json={
        "email": "student_qa@penta.vn",
        "password": "Password123!",
        "full_name": "Đặng Tiểu Long",
        "primary_learning_style": "visual"
    })
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Hỏi câu hỏi Lịch sử có sẵn trong DB -> Phản hồi từ 'knowledge_base'
    chat_hist = client.post(
        "/api/chat",
        json={"query": "Chiến dịch Điện Biên Phủ thắng lợi ngày tháng năm nào?"},
        headers=headers
    )
    assert chat_hist.status_code == 200
    res_data = chat_hist.json()
    assert res_data["source"] == "knowledge_base"
    assert "07/05/1954" in res_data["response"]
    assert "Đặng Tiểu Long" in res_data["response"]
    
    # 3. Hỏi câu hỏi hoàn toàn mới -> Phục vụ qua Fallback & Tự động lưu (Harvesting)
    novel_query = "Tại sao hiệp định Giơ-ne-vơ lại chia đôi đất nước Việt Nam?"
    chat_novel = client.post(
        "/api/chat",
        json={"query": novel_query},
        headers=headers
    )
    assert chat_novel.status_code == 200
    novel_res = chat_novel.json()
    assert novel_res["source"] == "ai_fallback_and_harvested"
    assert "Đặng Tiểu Long" in novel_res["response"]
    
    # 4. Hỏi lại chính câu hỏi đó (hoặc từ khóa chính) -> Lúc này đã nằm trong 'knowledge_base'
    chat_repeat = client.post(
        "/api/chat",
        json={"query": "hiệp định giơ-ne-vơ"},
        headers=headers
    )
    assert chat_repeat.status_code == 200
    repeat_res = chat_repeat.json()
    assert repeat_res["source"] == "knowledge_base"
