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

from main import app, USERS_DB, EMAIL_TO_USER_ID, LIFETIME_LEDGERS_DB
from shared.auth.jwt_auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_access_token,
)
from shared.models.user import UserRole


class SyncTestClient:
    """Helper client tương thích với httpx >= 0.28 và ASGI FastAPI app"""
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

    def put(self, url, json=None, headers=None):
        async def _req():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url=self.base_url) as ac:
                return await ac.put(url, json=json, headers=headers)
        return self._run(_req())


client = SyncTestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    """Làm sạch database in-memory trước mỗi test"""
    USERS_DB.clear()
    EMAIL_TO_USER_ID.clear()
    LIFETIME_LEDGERS_DB.clear()
    yield
    USERS_DB.clear()
    EMAIL_TO_USER_ID.clear()
    LIFETIME_LEDGERS_DB.clear()


# ==========================================
# 1. Unit Tests for JWT & Password Hashing
# ==========================================
def test_password_hashing():
    raw_pass = "Penta@SecurePass2026"
    hashed = hash_password(raw_pass)
    
    assert hashed != raw_pass
    assert "$" in hashed
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_generation_and_decode():
    user_id = "usr_123456"
    penta_id = "PID-2026-TEST"
    token = create_access_token(user_id=user_id, penta_id=penta_id, role="student")
    
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["penta_id"] == penta_id
    assert payload["role"] == "student"
    assert payload["token_type"] == "access"


def test_invalid_jwt_token():
    invalid_token = "invalid.token.string"
    assert decode_token(invalid_token) is None
    assert verify_access_token(invalid_token) is None


# ==========================================
# 2. Integration Tests for API Auth Endpoints
# ==========================================
def test_register_and_login_flow():
    # 1. Đăng ký
    register_payload = {
        "email": "student1@penta.edu.vn",
        "password": "Password123!",
        "full_name": "Nguyễn Văn Học Sinh",
        "role": "student",
        "primary_learning_style": "visual"
    }
    reg_res = client.post("/api/auth/register", json=register_payload)
    assert reg_res.status_code == 201
    data = reg_res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["penta_id"].startswith("PID-")
    
    # 2. Thử đăng ký lại trùng email -> Báo lỗi 400
    reg_dup = client.post("/api/auth/register", json=register_payload)
    assert reg_dup.status_code == 400
    
    # 3. Đăng nhập thành công
    login_payload = {
        "email": "student1@penta.edu.vn",
        "password": "Password123!"
    }
    login_res = client.post("/api/auth/login", json=login_payload)
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data
    assert login_data["user_id"] == data["user_id"]
    
    # 4. Đăng nhập sai mật khẩu -> Báo lỗi 401
    login_fail = client.post("/api/auth/login", json={
        "email": "student1@penta.edu.vn",
        "password": "WrongPassword!"
    })
    assert login_fail.status_code == 401


def test_get_my_lifetime_ledger():
    # Đăng ký tài khoản
    reg_res = client.post("/api/auth/register", json={
        "email": "lifetime_student@penta.vn",
        "password": "SecretPassword123",
        "full_name": "Trần Thị Trọn Đời",
        "primary_learning_style": "auditory"
    })
    token = reg_res.json()["access_token"]
    
    # 1. Gọi /api/user/me không có token -> 401
    unauth_res = client.get("/api/user/me")
    assert unauth_res.status_code == 401
    
    # 2. Gọi /api/user/me có Bearer Token -> 200 & trả về Lifetime Ledger
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/user/me", headers=headers)
    assert me_res.status_code == 200
    ledger = me_res.json()
    assert ledger["email"] == "lifetime_student@penta.vn"
    assert ledger["full_name"] == "Trần Thị Trọn Đời"
    assert ledger["ler_profile"]["primary_style"] == "auditory"
    assert len(ledger["milestones"]) >= 1


def test_update_ler_profile():
    reg_res = client.post("/api/auth/register", json={
        "email": "student_ler@penta.vn",
        "password": "PassWord!234",
        "full_name": "Lê Văn Tiến Bộ"
    })
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Cập nhật chỉ số LER
    ler_update = {
        "learning_speed": 1.5,
        "at_risk_score": 0.8,
        "strengths": ["Lịch sử", "Toán học"],
        "weaknesses": ["Hóa học"]
    }
    update_res = client.put("/api/user/ler", json=ler_update, headers=headers)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["learning_speed"] == 1.5
    assert updated["at_risk_score"] == 0.8
    assert "Lịch sử" in updated["strengths"]


def test_chat_with_and_without_user_context():
    # 1. Chat dưới danh nghĩa Guest (Không Token)
    guest_chat = client.post("/api/chat", json={"query": "Chiến dịch Điện Biên Phủ diễn ra năm nào?"})
    assert guest_chat.status_code == 200
    assert "Received:" in guest_chat.json()["response"]
    assert guest_chat.json()["user_context"] is None
    
    # 2. Chat dưới danh nghĩa Học sinh đã đăng nhập (Có Token + LER)
    reg_res = client.post("/api/auth/register", json={
        "email": "student_chat@penta.vn",
        "password": "PassWord!234",
        "full_name": "Phạm Minh Triết",
        "primary_learning_style": "kinesthetic"
    })
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    user_chat = client.post(
        "/api/chat",
        json={"query": "Làm sao để học tốt lịch sử?"},
        headers=headers
    )
    assert user_chat.status_code == 200
    chat_data = user_chat.json()
    assert "Phạm Minh Triết" in chat_data["response"]
    assert "kinesthetic" in chat_data["response"]
    assert chat_data["user_context"]["learning_style"] == "kinesthetic"
    assert chat_data["user_context"]["total_questions"] == 1
