"""
Pentaschool P2P Classroom & Study Group Models
Mỗi User có thể tự tạo phòng học (trở thành Host/Giáo viên tạm thời) và mời các User khác tham gia qua Invite Code.
"""

import time
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ClassroomRole(str, Enum):
    HOST = "host"      # Người tạo/chủ phòng lớp học
    MEMBER = "member"  # Thành viên/học sinh tham gia


class Classroom(BaseModel):
    """Mô hình Lớp học Tự quản P2P trong Pentaschool"""
    id: str
    code: str = Field(..., description="Mã mời tham gia phòng học (VD: CLS-8921)")
    name: str = Field(..., description="Tên lớp học / nhóm học")
    subject: str = Field(default="Tự học & Thảo luận", description="Môn học: Lịch sử, Toán, Tiếng Anh, v.v.")
    description: Optional[str] = None
    host_user_id: str = Field(..., description="User ID của người tạo phòng (Host)")
    host_name: str
    host_penta_id: str
    member_user_ids: List[str] = Field(default_factory=list, description="Danh sách User ID các thành viên")
    is_active: bool = True
    created_at: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClassroomCreateRequest(BaseModel):
    name: str
    subject: Optional[str] = "Tự học & Thảo luận"
    description: Optional[str] = None


class ClassroomJoinRequest(BaseModel):
    code: str = Field(..., description="Mã phòng học do Host cung cấp")


class ClassroomResponse(BaseModel):
    id: str
    code: str
    name: str
    subject: str
    description: Optional[str] = None
    host_user_id: str
    host_name: str
    host_penta_id: str
    total_members: int
    is_host: bool = False
    created_at: float
