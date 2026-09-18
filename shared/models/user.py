"""
Penta Lifetime User Identity & Centralized Life Ledger Models
Triết lý: 'Cuốn Sổ Quản Trị Cuộc Đời Trọn Đời Cho Người Việt (Penta Life OS)'
Hệ thống quản trị tập trung toàn diện cho người Việt, kết nối học tập (Pentaschool),
ghi chép (Pentanote), tài liệu cá nhân (PentaKuRu), nghề nghiệp (PentaJob), thương mại (PentaMarket).
"""

import time
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    USER = "user"    # Người dùng / Công dân số
    ADMIN = "admin"  # Quản trị viên hệ thống


class UserStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class PersonalProfileMetric(BaseModel):
    """
    Hồ sơ năng lực & Phong cách tiếp thu cá nhân hóa (Personal Evaluation & Style)
    Áp dụng đa lĩnh vực: học tập, công việc, quản lý thời gian, tư duy
    """
    primary_style: str = Field(default="visual", description="visual, auditory, kinesthetic, reading_writing, logical")
    efficiency_rate: float = Field(default=1.0, ge=0.1, le=3.0, description="Hệ số hiệu suất / tốc độ xử lý (1.0 = chuẩn)")
    learning_speed: float = Field(default=1.0, ge=0.1, le=3.0, description="Alias tương thích ngược cho tốc độ xử lý")
    at_risk_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Chỉ số rủi ro / cần hỗ trợ (0.0 - 1.0)")
    strengths: List[str] = Field(default_factory=list, description="Thế mạnh chuyên môn & kỹ năng")
    weaknesses: List[str] = Field(default_factory=list, description="Lĩnh vực cần cải thiện")
    last_evaluated_at: float = Field(default_factory=time.time)


# Giữ alias LearningStyleLER để tương thích ngược
LearningStyleLER = PersonalProfileMetric


class MilestoneRecord(BaseModel):
    """Cột mốc cuộc đời: học tập, chứng chỉ, công việc, dự án, sự kiện quan trọng"""
    id: str
    title: str
    category: str = Field(..., description="education, career, project, finance, cert, life_event, system")
    level: Optional[str] = None
    achieved_at: float = Field(default_factory=time.time)
    details: Dict[str, Any] = Field(default_factory=dict)


class UserLifetimeLedger(BaseModel):
    """
    Cuốn Sổ Quản Trị Cuộc Đời Trọn Đời (Lifetime Life Ledger)
    Định danh duy nhất toàn hệ thống cho mỗi người Việt
    """
    user_id: str
    penta_id: str = Field(..., description="Mã định danh cá nhân số (VD: PID-2026-0001)")
    email: str
    full_name: str
    role: UserRole = Field(default=UserRole.USER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    
    # Năng lực & Chỉ số cá nhân
    ler_profile: PersonalProfileMetric = Field(default_factory=PersonalProfileMetric)
    milestones: List[MilestoneRecord] = Field(default_factory=list)
    
    # Không gian P2P (Phòng học, Nhóm dự án, Không gian làm việc do user làm Host hoặc tham gia)
    hosted_classroom_ids: List[str] = Field(default_factory=list, description="Không gian/Phòng do user làm Host")
    joined_classroom_ids: List[str] = Field(default_factory=list, description="Không gian/Phòng user tham gia")
    
    # Thống kê hoạt động toàn hệ sinh thái
    total_questions_asked: int = 0
    total_active_minutes: int = 0
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


# ==========================================
# Auth Request & Response Schemas
# ==========================================
class UserRegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: Optional[UserRole] = UserRole.USER
    primary_learning_style: Optional[str] = "visual"


class UserLoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    penta_id: str
    role: str


class UserResponse(BaseModel):
    user_id: str
    penta_id: str
    email: str
    full_name: str
    role: UserRole
    status: UserStatus
    ler_profile: PersonalProfileMetric
    milestones_count: int
    hosted_spaces_count: int
    joined_spaces_count: int
    created_at: float


class UpdateLERRequest(BaseModel):
    primary_style: Optional[str] = None
    learning_speed: Optional[float] = None
    efficiency_rate: Optional[float] = None
    at_risk_score: Optional[float] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
