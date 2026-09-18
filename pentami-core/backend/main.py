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
from shared.models.classroom import (
    Classroom,
    ClassroomCreateRequest,
    ClassroomJoinRequest,
    ClassroomResponse,
)
from shared.auth.jwt_auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    decode_token,
)
from qa_engine import qa_engine

# ==========================================
# In-Memory Database Store (Prototype Lifetime Store)
# ==========================================
# Lưu trữ User Auth: user_id -> dict(email, hashed_password, role, penta_id)
USERS_DB: Dict[str, Dict[str, Any]] = {}
# Lưu email -> user_id để tra cứu nhanh khi login
EMAIL_TO_USER_ID: Dict[str, str] = {}
# Lưu trữ Cuốn sổ học sinh trọn đời: user_id -> UserLifetimeLedger
LIFETIME_LEDGERS_DB: Dict[str, UserLifetimeLedger] = {}
# Lưu trữ Lớp học P2P: classroom_id -> Classroom
CLASSROOMS_DB: Dict[str, Classroom] = {}
# Lưu mã mời: code -> classroom_id
CLASSROOM_CODE_TO_ID: Dict[str, str] = {}


def generate_penta_id() -> str:
    """Sinh mã định danh thân thiện cho học sinh (VD: PID-2026-A1B2)"""
    year = time.strftime("%Y")
    random_part = uuid.uuid4().hex[:4].upper()
    return f"PID-{year}-{random_part}"


def generate_classroom_code() -> str:
    """Sinh mã mời phòng học ngắn gọn (VD: CLS-8921)"""
    random_digits = uuid.uuid4().hex[:4].upper()
    return f"CLS-{random_digits}"


# ==========================================
# FastAPI Application & Dependencies
# ==========================================
app = FastAPI(
    title="Penta Core Brain Gateway",
    description="API Gateway, P2P Classrooms & Lifetime Student Ledger for Penta AI Ecosystem",
    version="1.1.0"
)


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "sess_default"
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    target_app: str = "pentami_core"
    source: str
    subject: Optional[str] = None
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
        "active_classrooms": len(CLASSROOMS_DB),
        "knowledge_entries": qa_engine.kb.total_entries,
    }


@app.get("/api/ecosystem/apps")
async def get_apps():
    return {"apps": ["Pentaschool", "Pentanote", "PentaKuRu", "PentaMarket", "PentaJob"]}


# ==========================================
# 2. Authentication & Lifetime User Endpoints
# ==========================================
@app.post("/api/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest):
    """Đăng ký tài khoản người dùng mới và khởi tạo Cuốn sổ học tập trọn đời"""
    if req.email in EMAIL_TO_USER_ID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email này đã được đăng ký trong hệ thống"
        )
    
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    penta_id = generate_penta_id()
    hashed_pwd = hash_password(req.password)
    assigned_role = req.role or UserRole.USER
    
    # 1. Lưu thông tin xác thực
    USERS_DB[user_id] = {
        "user_id": user_id,
        "email": req.email,
        "hashed_password": hashed_pwd,
        "role": assigned_role.value,
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
        role=assigned_role,
        status=UserStatus.ACTIVE,
        ler_profile=initial_ler,
        milestones=[initial_milestone],
        hosted_classroom_ids=[],
        joined_classroom_ids=[],
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
# 3. P2P Classroom Management (Pentaschool)
# ==========================================
@app.post("/api/classrooms", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED)
async def create_classroom(
    req: ClassroomCreateRequest,
    current_user: UserLifetimeLedger = Depends(get_current_user)
):
    """
    User tự tạo lớp học mới và trở thành Host ('Giáo viên tạm thời') của lớp đó
    """
    classroom_id = f"cls_{uuid.uuid4().hex[:8]}"
    code = generate_classroom_code()
    
    # Đảm bảo mã mời không trùng
    while code in CLASSROOM_CODE_TO_ID:
        code = generate_classroom_code()
        
    classroom = Classroom(
        id=classroom_id,
        code=code,
        name=req.name,
        subject=req.subject or "Tự học & Thảo luận",
        description=req.description,
        host_user_id=current_user.user_id,
        host_name=current_user.full_name,
        host_penta_id=current_user.penta_id,
        member_user_ids=[current_user.user_id],
        created_at=time.time()
    )
    
    CLASSROOMS_DB[classroom_id] = classroom
    CLASSROOM_CODE_TO_ID[code] = classroom_id
    
    # Cập nhật vào cuốn sổ học sinh của người tạo
    if classroom_id not in current_user.hosted_classroom_ids:
        current_user.hosted_classroom_ids.append(classroom_id)
        current_user.milestones.append(MilestoneRecord(
            id=f"ms_{uuid.uuid4().hex[:8]}",
            title=f"Khởi tạo Lớp học: {req.name}",
            category="k12",
            details={"classroom_id": classroom_id, "code": code}
        ))
        current_user.updated_at = time.time()
        
    return ClassroomResponse(
        id=classroom.id,
        code=classroom.code,
        name=classroom.name,
        subject=classroom.subject,
        description=classroom.description,
        host_user_id=classroom.host_user_id,
        host_name=classroom.host_name,
        host_penta_id=classroom.host_penta_id,
        total_members=len(classroom.member_user_ids),
        is_host=True,
        created_at=classroom.created_at
    )


@app.post("/api/classrooms/join", response_model=ClassroomResponse)
async def join_classroom(
    req: ClassroomJoinRequest,
    current_user: UserLifetimeLedger = Depends(get_current_user)
):
    """User tham gia lớp học của bạn bè thông qua Invite Code"""
    clean_code = req.code.strip().upper()
    classroom_id = CLASSROOM_CODE_TO_ID.get(clean_code)
    
    if not classroom_id or classroom_id not in CLASSROOMS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mã lớp học không tồn tại hoặc đã đóng"
        )
        
    classroom = CLASSROOMS_DB[classroom_id]
    
    if current_user.user_id not in classroom.member_user_ids:
        classroom.member_user_ids.append(current_user.user_id)
        
    if classroom_id not in current_user.joined_classroom_ids:
        current_user.joined_classroom_ids.append(classroom_id)
        current_user.milestones.append(MilestoneRecord(
            id=f"ms_{uuid.uuid4().hex[:8]}",
            title=f"Tham gia Lớp học: {classroom.name}",
            category="k12",
            details={"classroom_id": classroom_id, "host": classroom.host_name}
        ))
        current_user.updated_at = time.time()
        
    is_host = (classroom.host_user_id == current_user.user_id)
    
    return ClassroomResponse(
        id=classroom.id,
        code=classroom.code,
        name=classroom.name,
        subject=classroom.subject,
        description=classroom.description,
        host_user_id=classroom.host_user_id,
        host_name=classroom.host_name,
        host_penta_id=classroom.host_penta_id,
        total_members=len(classroom.member_user_ids),
        is_host=is_host,
        created_at=classroom.created_at
    )


@app.get("/api/classrooms/my", response_model=Dict[str, List[ClassroomResponse]])
async def get_my_classrooms(current_user: UserLifetimeLedger = Depends(get_current_user)):
    """Lấy danh sách các lớp học do user làm Host và các lớp học user đã tham gia"""
    hosted = []
    joined = []
    
    for c_id in current_user.hosted_classroom_ids:
        if c_id in CLASSROOMS_DB:
            c = CLASSROOMS_DB[c_id]
            hosted.append(ClassroomResponse(
                id=c.id,
                code=c.code,
                name=c.name,
                subject=c.subject,
                description=c.description,
                host_user_id=c.host_user_id,
                host_name=c.host_name,
                host_penta_id=c.host_penta_id,
                total_members=len(c.member_user_ids),
                is_host=True,
                created_at=c.created_at
            ))
            
    for c_id in current_user.joined_classroom_ids:
        if c_id in CLASSROOMS_DB:
            c = CLASSROOMS_DB[c_id]
            joined.append(ClassroomResponse(
                id=c.id,
                code=c.code,
                name=c.name,
                subject=c.subject,
                description=c.description,
                host_user_id=c.host_user_id,
                host_name=c.host_name,
                host_penta_id=c.host_penta_id,
                total_members=len(c.member_user_ids),
                is_host=(c.host_user_id == current_user.user_id),
                created_at=c.created_at
            ))
            
    return {"hosted": hosted, "joined": joined}


# ==========================================
# 4. Intelligent QA & Slot Filling Chat Endpoint
# ==========================================
@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Optional[UserLifetimeLedger] = Depends(get_current_user_optional)
):
    """
    Endpoint Chatbot thông minh:
    - Tra cứu Knowledge Base trước (Zero-cost)
    - Tự động điền các slot biến động: [STUDENT_NAME], [AVG], [STATUS_COLOR], [LER_ACTION]
    - Tự học & lưu ngược kiến thức mới vào Database nếu gặp câu hỏi chưa từng có
    """
    if current_user:
        current_user.total_questions_asked += 1
        current_user.updated_at = time.time()
        
    qa_result = qa_engine.process_query(
        query=request.query,
        user=current_user,
        context=request.context
    )
    
    user_ctx = None
    if current_user:
        user_ctx = {
            "user_id": current_user.user_id,
            "penta_id": current_user.penta_id,
            "learning_style": current_user.ler_profile.primary_style,
            "total_questions": current_user.total_questions_asked,
            "at_risk_score": current_user.ler_profile.at_risk_score,
        }
        
    return ChatResponse(
        response=qa_result["response"],
        target_app=qa_result.get("target_app", "pentami_core"),
        source=qa_result["source"],
        subject=qa_result.get("subject"),
        user_context=user_ctx
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
