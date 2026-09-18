"""
Penta P2P Decentralized Space & Group Models
Mô hình Không gian Quản trị & Làm việc Tự quản P2P trong Hệ thống Penta Core.
Mỗi User có thể tự tạo Không gian / Phòng làm việc / Nhóm học tập (trở thành Host)
và mời các User khác tham gia qua Invite Code.
"""

import time
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SpaceRole(str, Enum):
    HOST = "host"      # Người tạo/chủ phòng không gian
    MEMBER = "member"  # Thành viên tham gia


# Alias tương thích ngược
ClassroomRole = SpaceRole


class PentaSpace(BaseModel):
    """Mô hình Không gian Tự quản P2P trong Hệ sinh thái Penta Core"""
    id: str
    code: str = Field(..., description="Mã mời tham gia không gian (VD: SPC-8921 / CLS-8921)")
    name: str = Field(..., description="Tên không gian / phòng làm việc / nhóm")
    subject: str = Field(default="Quản trị & Thảo luận chung", description="Chủ đề: Dự án, Lịch sử, Quản trị, Nghề nghiệp, v.v.")
    description: Optional[str] = None
    host_user_id: str = Field(..., description="User ID của người tạo không gian (Host)")
    host_name: str
    host_penta_id: str
    member_user_ids: List[str] = Field(default_factory=list, description="Danh sách User ID các thành viên")
    is_active: bool = True
    created_at: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Alias tương thích ngược
Classroom = PentaSpace


class SpaceCreateRequest(BaseModel):
    name: str
    subject: Optional[str] = "Quản trị & Thảo luận chung"
    description: Optional[str] = None


ClassroomCreateRequest = SpaceCreateRequest


class SpaceJoinRequest(BaseModel):
    code: str = Field(..., description="Mã không gian do Host cung cấp")


ClassroomJoinRequest = SpaceJoinRequest


class SpaceResponse(BaseModel):
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


ClassroomResponse = SpaceResponse
