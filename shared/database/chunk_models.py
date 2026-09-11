"""
Mô hình Database & DTO cho hệ thống Stream Chunks (chunk_emo, chunk_time, chunk_action).
Hỗ trợ tương thích kép (Pydantic / Dataclasses) hoạt động độc lập không phụ thuộc pip.
Trạng thái: Tạo sẵn mô hình dữ liệu, tạm dừng kích hoạt runtime (ENABLE_3D_CHUNKS = False).
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    from dataclasses import dataclass, field, asdict
    HAS_PYDANTIC = False

    class BaseModel:
        def model_dump(self) -> Dict[str, Any]:
            return asdict(self)

        def model_dump_json(self) -> str:
            return json.dumps(asdict(self), default=str)

    def Field(default=..., **kwargs):
        if "default_factory" in kwargs:
            return field(default_factory=kwargs["default_factory"])
        if default is ...:
            return field()
        if callable(default):
            return field(default_factory=default)
        return field(default=default)

def db_model(cls):
    if not HAS_PYDANTIC:
        return dataclass(cls)
    return cls

# Cờ điều khiển: Tạm dừng xử lý phức tạp tại runtime theo chỉ thị
ENABLE_3D_CHUNKS = os.getenv("ENABLE_3D_CHUNKS", "false").lower() == "true"

@db_model
class StreamSessionDB(BaseModel):
    session_id: str
    tenant_id: str
    user_id: str
    app_source: str = "pentami-core"
    is_3d_enabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

@db_model
class StreamChunkDB(BaseModel):
    chunk_id: str
    session_id: str
    message_id: str
    tenant_id: str
    chunk_index: int
    chunk_type: str  # text, emo, time, action, status
    content: Optional[str] = None
    is_paused: bool = True  # Mặc định tạm dừng
    created_at: datetime = Field(default_factory=datetime.utcnow)

@db_model
class ChunkEmoDB(BaseModel):
    id: str
    chunk_id: str
    sentiment: str = "neutral"
    target_tone: str = "friendly"
    intensity: float = 0.50
    avatar_blendshapes: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

@db_model
class ChunkTimeDB(BaseModel):
    id: str
    chunk_id: str
    audio_start_ms: int = 0
    audio_end_ms: int = 0
    phoneme_sequence: str = ""
    audio_offset_sec: float = 0.000
    temporal_decay_factor: float = 0.050
    time_context: str = "realtime_session"
    created_at: datetime = Field(default_factory=datetime.utcnow)

@db_model
class ChunkActionDB(BaseModel):
    id: str
    chunk_id: str
    action_type: str
    target_subsystem: str
    tool_to_invoke: Optional[str] = None
    action_payload: Dict[str, Any] = Field(default_factory=dict)
    require_user_confirmation: bool = True
    execution_status: str = "paused"  # Trạng thái tạm dừng
    executed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
