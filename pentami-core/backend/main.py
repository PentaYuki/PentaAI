import os
import sys
import uuid
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

# Đảm bảo import được module shared từ thư mục gốc
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field

from shared.models.user import (
    UserRole,
    UserStatus,
    LearningStyleLER,
    MilestoneRecord,
    UserLifetimeLedger,
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    UpdateLERRequest,
)
from shared.auth.jwt_auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    decode_token,
)

# ==========================================
# In-Memory Database Store (Prototype Lifetime Store)
# ==========================================
# Lưu trữ User Auth: user_id -> dict(email, hashed_password, role, penta_id)
USERS_DB: Dict[str, Dict[str, Any]] = {}
# Lưu email -> user_id để tra cứu nhanh khi login
EMAIL_TO_USER_ID: Dict[str, str] = {}
# Lưu trữ Cuốn sổ học sinh trọn đời: user_id -> UserLifetimeLedger
LIFETIME_LEDGERS_DB: Dict[str, UserLifetimeLedger] = {}


def generate_penta_id() -> str:
    """Sinh mã định danh thân thiện cho học sinh (VD: PID-2026-A1B2)"""
    year = time.strftime("%Y")
    random_part = uuid.uuid4().hex[:4].upper()
    return f"PID-{year}-{random_part}"


# ==========================================
# FastAPI Application & Dependencies
# ==========================================
app = FastAPI(
    title="Penta Core Brain Gateway",
    description="API Gateway & Lifetime Student Ledger for Penta AI Ecosystem",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "sess_default"


class ChatResponse(BaseModel):
    response: str
    user_context: Optional[Dict[str, Any]] = None


async def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[UserLifetimeLedger]:
    """Lấy thông tin User hiện tại từ JWT nếu có trong header"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    return LIFETIME_LEDGERS_DB.get(user_id)


async def get_current_user(authorization: Optional[str] = Header(None)) -> UserLifetimeLedger:
    """Bắt buộc có JWT Token hợp lệ"""
    user = await get_current_user_optional(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu xác thực JWT Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# ==========================================
# 1. Health & Ecosystem Endpoints
# ==========================================
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "system": "Penta Core Brain Gateway",
        "registered_users": len(USERS_DB),
    }


@app.get("/api/ecosystem/apps")
async def get_apps():
    return {"apps": ["Pentaschool", "Pentanote", "PentaKuRu", "PentaMarket", "PentaJob"]}


# ==========================================
# 2. Authentication & Lifetime User Endpoints
# ==========================================
@app.post("/api/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest):
    """Đăng ký tài khoản học sinh mới và khởi tạo Cuốn sổ học tập trọn đời"""
    if req.email in EMAIL_TO_USER_ID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email này đã được đăng ký trong hệ thống"
        )
    
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    penta_id = generate_penta_id()
    hashed_pwd = hash_password(req.password)
    
    # 1. Lưu thông tin xác thực
    USERS_DB[user_id] = {
        "user_id": user_id,
        "email": req.email,
        "hashed_password": hashed_pwd,
        "role": req.role.value if req.role else UserRole.STUDENT.value,
        "penta_id": penta_id,
        "full_name": req.full_name,
    }
    EMAIL_TO_USER_ID[req.email] = user_id
    
    # 2. Khởi tạo Cuốn sổ học tập trọn đời (Lifetime Ledger)
    initial_ler = LearningStyleLER(
        primary_style=req.primary_learning_style or "visual",
        learning_speed=1.0,
        at_risk_score=0.0
    )
    initial_milestone = MilestoneRecord(
        id=f"ms_{uuid.uuid4().hex[:8]}",
        title="Gia nhập Hệ sinh thái Penta",
        category="system",
        details={"event": "initial_account_created"}
    )
    
    ledger = UserLifetimeLedger(
        user_id=user_id,
        penta_id=penta_id,
        email=req.email,
        full_name=req.full_name,
        role=req.role or UserRole.STUDENT,
        status=UserStatus.ACTIVE,
        ler_profile=initial_ler,
        milestones=[initial_milestone],
        created_at=time.time(),
        updated_at=time.time()
    )
    LIFETIME_LEDGERS_DB[user_id] = ledger
    
    # 3. Tạo Token
    access_token = create_access_token(
        user_id=user_id,
        penta_id=penta_id,
        role=ledger.role.value
    )
    refresh_token = create_refresh_token(user_id=user_id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=86400 * 7,
        user_id=user_id,
        penta_id=penta_id,
        role=ledger.role.value
    )


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(req: UserLoginRequest):
    """Đăng nhập hệ thống và cấp JWT Token"""
    user_id = EMAIL_TO_USER_ID.get(req.email)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )
    
    user_record = USERS_DB.get(user_id)
    if not user_record or not verify_password(req.password, user_record["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )
        
    access_token = create_access_token(
        user_id=user_id,
        penta_id=user_record["penta_id"],
        role=user_record["role"]
    )
    refresh_token = create_refresh_token(user_id=user_id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=86400 * 7,
        user_id=user_id,
        penta_id=user_record["penta_id"],
        role=user_record["role"]
    )


@app.post("/api/auth/refresh", response_model=Dict[str, Any])
async def refresh_token(refresh_token: str):
    """Cấp lại Access Token mới từ Refresh Token"""
    payload = decode_token(refresh_token)
    if not payload or payload.get("token_type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token không hợp lệ hoặc đã hết hạn"
        )
        
    user_id = payload.get("sub")
    user_record = USERS_DB.get(user_id)
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
        
    new_access_token = create_access_token(
        user_id=user_id,
        penta_id=user_record["penta_id"],
        role=user_record["role"]
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 86400 * 7
    }


@app.get("/api/user/me", response_model=UserLifetimeLedger)
async def get_my_lifetime_ledger(current_user: UserLifetimeLedger = Depends(get_current_user)):
    """Lấy toàn bộ thông tin 'Cuốn sổ học sinh trọn đời' của người dùng hiện tại"""
    return current_user


@app.put("/api/user/ler", response_model=LearningStyleLER)
async def update_my_ler_profile(
    req: UpdateLERRequest,
    current_user: UserLifetimeLedger = Depends(get_current_user)
):
    """Cập nhật chỉ số học tập LER (tốc độ tiếp thu, phong cách học, điểm nguy cơ)"""
    if req.primary_style is not None:
        current_user.ler_profile.primary_style = req.primary_style
    if req.learning_speed is not None:
        current_user.ler_profile.learning_speed = req.learning_speed
    if req.at_risk_score is not None:
        current_user.ler_profile.at_risk_score = req.at_risk_score
    if req.strengths is not None:
        current_user.ler_profile.strengths = req.strengths
    if req.weaknesses is not None:
        current_user.ler_profile.weaknesses = req.weaknesses
    current_user.ler_profile.last_evaluated_at = time.time()
    current_user.updated_at = time.time()
    return current_user.ler_profile


# ==========================================
# 3. Intelligent Chat Endpoint (With User Context)
# ==========================================
@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Optional[UserLifetimeLedger] = Depends(get_current_user_optional)
):
    """
    Endpoint Chatbot thông minh:
    - Nếu có JWT User: Tự động ghi nhận hoạt động và cá nhân hóa phản hồi theo hồ sơ LER
    - Nếu không có JWT: Trả lời dạng khách (Guest)
    """
    if current_user:
        current_user.total_questions_asked += 1
        current_user.updated_at = time.time()
        
        # Cá nhân hóa phản hồi theo LER
        ler = current_user.ler_profile
        greeting = f"Chào {current_user.full_name} ({current_user.penta_id})!"
        
        # Kiểm tra cảnh báo nguy cơ tụt hậu
        warning_tag = ""
        if ler.at_risk_score >= 0.7:
            warning_tag = " [Cảnh báo: Cần chú ý hoàn thành bài tập tuần này]"
            
        personalized_response = (
            f"{greeting}{warning_tag} Hệ thống đã ghi nhận câu hỏi: '{request.query}'. "
            f"Phong cách học tập của bạn: {ler.primary_style} (Tốc độ: {ler.learning_speed}x)."
        )
        
        return ChatResponse(
            response=personalized_response,
            user_context={
                "user_id": current_user.user_id,
                "penta_id": current_user.penta_id,
                "learning_style": ler.primary_style,
                "total_questions": current_user.total_questions_asked,
                "at_risk_score": ler.at_risk_score,
            }
        )
        
    return ChatResponse(
        response=f"Received: {request.query}",
        user_context=None
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
