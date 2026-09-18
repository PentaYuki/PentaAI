"""
Penta Lifetime User Identity & Learning Ledger Models
Triết lý: 'Cuốn sổ học sinh theo suốt cuộc đời'
Hệ thống chỉ có 2 role toàn cục: USER và ADMIN.
Mỗi user có thể tự tạo phòng học trong Pentaschool và đóng vai trò Host của phòng học đó.
"""

import time
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    GRADUATED = "graduated"


class LearningStyleLER(BaseModel):
    """
    LER Profile (Learning Style, Efficiency & Retention)
    Đặc tính học tập và tốc độ tiếp thu được cá nhân hóa
    """
    primary_style: str = Field(default="visual", description="visual, auditory, kinesthetic, reading_writing")
    learning_speed: float = Field(default=1.0, ge=0.1, le=3.0, description="Hệ số tốc độ tiếp thu (1.0 = chuẩn)")
    at_risk_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Chỉ số nguy cơ tụt hậu/bỏ học (0.0 - 1.0)")
    strengths: List[str] = Field(default_factory=list, description="Môn học / kỹ năng thế mạnh")
    weaknesses: List[str] = Field(default_factory=list, description="Chủ đề cần hỗ trợ thêm")
    last_evaluated_at: float = Field(default_factory=time.time)


class MilestoneRecord(BaseModel):
    """Cột mốc học tập và phát triển cá nhân theo thời gian"""
    id: str
    title: str
    category: str = Field(..., description="k12, college, career, cert, project, system")
    grade_or_level: Optional[str] = None
    achieved_at: float = Field(default_factory=time.time)
    details: Dict[str, Any] = Field(default_factory=dict)


class UserLifetimeLedger(BaseModel):
    """
    Cuốn sổ học tập trọn đời
    Lưu trữ toàn bộ lịch sử, phong cách học và thành tựu của 1 User ID duy nhất
    """
    user_id: str
    penta_id: str = Field(..., description="Mã định danh thân thiện (VD: PID-2026-0001)")
    email: str
    full_name: str
    role: UserRole = Field(default=UserRole.USER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    
    # Học tập & LER
    ler_profile: LearningStyleLER = Field(default_factory=LearningStyleLER)
    milestones: List[MilestoneRecord] = Field(default_factory=list)
    
    # Lớp học P2P (User tự làm Host phòng học hoặc tham gia phòng người khác)
    hosted_classroom_ids: List[str] = Field(default_factory=list, description="Các lớp học do user này làm Host/Chủ phòng")
    joined_classroom_ids: List[str] = Field(default_factory=list, description="Các lớp học user này tham gia")
    
    # Thống kê hoạt động
    total_questions_asked: int = 0
    total_study_minutes: int = 0
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
    ler_profile: LearningStyleLER
    milestones_count: int
    hosted_classrooms_count: int
    joined_classrooms_count: int
    created_at: float


class UpdateLERRequest(BaseModel):
    primary_style: Optional[str] = None
    learning_speed: Optional[float] = None
    at_risk_score: Optional[float] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
