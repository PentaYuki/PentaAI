"""
Penta Unified AI Stream Protocol (PUASP)
Định nghĩa cấu trúc các loại chunk: Text, Emo (Cảm xúc), Time (Thời gian/Đồng bộ), Action (Hành động).
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional
import json

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


def pydantic_or_dataclass(cls):
    if not HAS_PYDANTIC:
        return dataclass(cls)
    return cls


class ChunkType(str, Enum):
    TEXT = "text"
    EMO = "emo"
    TIME = "time"
    ACTION = "action"
    STATUS = "status"


class EmotionType(str, Enum):
    NEUTRAL = "neutral"
    JOYFUL = "joyful"
    ENCOURAGING = "encouraging"
    THOUGHTFUL = "thoughtful"
    SERIOUS = "serious"
    EMPATHETIC = "empathetic"
    SURPRISED = "surprised"


@pydantic_or_dataclass
class ChunkEmoData(BaseModel):
    """
    Dữ liệu cảm xúc để điều khiển Avatar AI (Pentaschool, Pentamarket)
    hoặc điều chỉnh sắc thái giọng nói / giao diện.
    """
    emotion: EmotionType = Field(default=EmotionType.NEUTRAL, description="Trạng thái cảm xúc chính")
    intensity: float = Field(default=1.0, description="Cường độ cảm xúc (0.0 đến 1.0)")
    gesture: Optional[str] = Field(default=None, description="Cử chỉ của Avatar: hand_wave, head_nod, lean_forward...")
    voice_pitch_multiplier: float = Field(default=1.0, description="Điều chế cao độ giọng nói ElevenLabs")
    voice_rate_multiplier: float = Field(default=1.0, description="Điều chế tốc độ giọng nói")


@pydantic_or_dataclass
class ChunkTimeData(BaseModel):
    """
    Dữ liệu mốc thời gian để đồng bộ hoàn hảo giữa giọng nói (TTS),
    khẩu hình miệng (Viseme / Lip-sync) và luồng chữ hiển thị trên màn hình.
    """
    token_index: int = Field(default=0, description="Chỉ mục của từ/cụm từ đang phát")
    cue_start_ms: int = Field(default=0, description="Thời điểm bắt đầu tính bằng mili-giây")
    duration_ms: int = Field(default=0, description="Độ dài phát âm của cụm từ")
    viseme_code: Optional[str] = Field(default=None, description="Mã khẩu hình miệng cho 3D/2D Avatar")


@pydantic_or_dataclass
class ChunkActionData(BaseModel):
    """
    Lệnh thực thi hành động tự động hóa:
    - Điều khiển UI client (chuyển slide trong Pentaschool, thêm vào giỏ hàng trong Pentamarket)
    - Kích hoạt tác vụ trình duyệt qua Playwright MCP Server
    """
    action_id: str = Field(default="", description="Mã định danh duy nhất của hành động")
    target_system: str = Field(default="pentaschool", description="Phân hệ tiếp nhận và thực thi hành động")
    command: str = Field(default="", description="Tên lệnh cần thực hiện (ví dụ: navigate, open_quiz, add_to_cart)")
    params: Dict[str, Any] = Field(default_factory=dict, description="Tham số truyền vào cho lệnh")
    require_user_confirmation: bool = Field(default=False, description="Có cần người dùng bấm xác nhận trước khi thực hiện không")


@pydantic_or_dataclass
class PentaStreamEnvelope(BaseModel):
    """
    Gói bọc (Envelope) chuẩn hóa cho mọi gói tin stream từ PentaCore tới Client.
    """
    seq: int = Field(default=0, description="Số thứ tự của gói tin trong phiên stream")
    session_id: str = Field(default="", description="ID của phiên hội thoại")
    type: ChunkType = Field(default=ChunkType.TEXT, description="Loại gói tin: text | emo | time | action | status")
    text_content: Optional[str] = Field(default=None, description="Nội dung chữ (khi type=text)")
    emo: Optional[ChunkEmoData] = Field(default=None, description="Dữ liệu cảm xúc (khi type=emo)")
    time: Optional[ChunkTimeData] = Field(default=None, description="Dữ liệu đồng bộ thời gian (khi type=time)")
    action: Optional[ChunkActionData] = Field(default=None, description="Dữ liệu hành động (khi type=action)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata bổ sung")
