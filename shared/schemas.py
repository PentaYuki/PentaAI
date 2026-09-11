"""
PentaKurumi Core Ecosystem - Shared Data Schemas & Models
Định nghĩa chuẩn dữ liệu liên thông giữa tất cả các phân hệ.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "live"


class EcosystemSystem(str, Enum):
    PENTAMI_CORE = "pentami_core"
    PENTASCHOOL = "pentaschool"
    PENTAKURU = "pentakuru"
    PENTAMARKET = "pentamarket"
    PENTAJOB = "pentajob"
    MCP_PLAYWRIGHT = "mcp_playwright"


# ==========================================
# 1. UNIFIED API KEY & IAM MODEL
# ==========================================
class UnifiedApiKeyRecord(BaseModel):
    """Mô hình lưu trữ API Key thống nhất trong hệ thống"""
    key_id: str = Field(..., description="ID định danh duy nhất của key")
    key_hash: str = Field(..., description="Hash SHA-256 / Argon2 của API Key (không lưu plaintext)")
    key_prefix: str = Field(..., description="Tiền tố hiển thị cho user (VD: penta_live_sk_a8f9...)")
    user_id: str = Field(..., description="ID người dùng sở hữu")
    environment: Environment = Field(default=Environment.PRODUCTION)
    scopes: List[str] = Field(
        default_factory=list,
        description="Danh sách quyền được phép (VD: ['penta:core:chat', 'penta:school:learn'])"
    )
    rate_limit_rpm: int = Field(default=60, description="Số request tối đa mỗi phút")
    rate_limit_tpm: int = Field(default=40000, description="Số token tối đa mỗi phút")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


# ==========================================
# 2. 3D CHUNK MODEL (EMO, TIME, ACTION)
# ==========================================
class ChunkEmo(BaseModel):
    """Chunk biểu diễn trạng thái cảm xúc, tâm trạng và tone giọng phản hồi"""
    sentiment: str = Field(..., description="positive, negative, neutral, inquisitive, frustrated")
    target_tone: str = Field(default="friendly", description="encouraging, empathetic, professional, humorous")
    intensity: float = Field(default=0.5, ge=0.0, le=1.0, description="Cường độ cảm xúc từ 0.0 đến 1.0")


class ChunkTime(BaseModel):
    """Chunk biểu diễn ngữ cảnh thời gian và độ tươi mới của tri thức"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    effective_until: Optional[datetime] = None
    temporal_decay_factor: float = Field(default=0.05, description="Tốc độ suy giảm độ liên quan theo thời gian")
    time_context: Optional[str] = Field(None, description="Ví dụ: 'realtime_session', 'archive', 'historical'")


class ChunkAction(BaseModel):
    """Chunk định nghĩa hành động kích hoạt qua MCP hoặc điều khiển giao diện"""
    action_type: str = Field(..., description="mcp_tool_call, client_ui_event, backend_job")
    target_system: EcosystemSystem = Field(...)
    tool_to_invoke: Optional[str] = Field(None, description="Tên tool MCP (VD: 'playwright_click')")
    action_payload: Dict[str, Any] = Field(default_factory=dict, description="Dữ liệu tham số truyền cho hành động")


class PentaChunk(BaseModel):
    """Mô hình dữ liệu hoàn chỉnh của một Vector Chunk trong hệ thống RAG"""
    chunk_id: str = Field(..., description="ID định danh chunk")
    source_system: EcosystemSystem = Field(...)
    document_id: str = Field(..., description="ID tài liệu gốc")
    content: str = Field(..., description="Nội dung văn bản")
    embedding: Optional[List[float]] = Field(None, description="Vector 384 dimensions từ all-MiniLM-L6-v2")
    
    # Bộ ba siêu dữ liệu đặc thù
    chunk_emo: Optional[ChunkEmo] = None
    chunk_time: Optional[ChunkTime] = None
    chunk_action: Optional[ChunkAction] = None
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ==========================================
# 3. VOICE STREAMING CONFIG
# ==========================================
class VoiceConfig(BaseModel):
    """Cấu hình cho Voice Streaming Pipeline"""
    stt_provider: str = Field(default="deepgram", description="deepgram hoặc sherpa-onnx")
    stt_model: str = Field(default="nova-2")
    stt_language: str = Field(default="vi", description="vi hoặc en")
    
    tts_provider: str = Field(default="elevenlabs")
    tts_voice_id: str = Field(default="21m00Tcm4TlvDq8ikWAM")
    tts_model_id: str = Field(default="eleven_multilingual_v2")
    tts_latency_tier: int = Field(default=1, description="Cấp độ tối ưu độ trễ (0: bình thường, 1-4: ưu tiên tốc độ cao)")
