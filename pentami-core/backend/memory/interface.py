"""
Interface trừu tượng cho Module Quản Lý Ngữ Cảnh & Bộ Nhớ Đa Lượt (Context & Memory Management).
Tuân thủ Điều 1 (Guru Factory Pattern) và Điều 2 (Dual-Path Q&A Rule) trong GEMINI.md.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

@dataclass
class ConversationTurn:
    role: str  # "user" | "assistant"
    content: str
    subsystem: Optional[str] = None  # "pentaschool", "pentakuru", etc.
    has_formula: bool = False
    formula_ref: Optional[str] = None
    extracted_variables: Dict[str, Any] = field(default_factory=dict)
    persona: Optional[str] = None  # "cute", "serious", "yandere"
    timestamp: float = field(default_factory=time.time)

@dataclass
class SessionContext:
    session_id: str
    tenant_id: str
    active_subsystem: str = "pentaschool"
    active_subject: Optional[str] = None  # e.g., "toan_12"
    active_formula_ref: Optional[str] = None
    active_variables: Dict[str, Any] = field(default_factory=dict)
    active_persona: str = "cute"
    history: List[ConversationTurn] = field(default_factory=list)
    max_history_turns: int = 6

@dataclass
class ContextualResolution:
    raw_query: str
    condensed_query: str  # Câu hỏi sau khi bổ sung ngữ cảnh (Self-contained query)
    is_short_query: bool  # True nếu câu hỏi cộc lốc (< 5 từ hoặc chứa từ quy chiếu)
    inherited_subsystem: str  # Phân hệ thừa hưởng từ ngữ cảnh trước
    inherited_formula_ref: Optional[str] = None
    merged_variables: Dict[str, Any] = field(default_factory=dict)

class IQueryCondenser(ABC):
    """Giao diện tái cấu trúc câu hỏi ngắn dựa trên ngữ cảnh lịch sử"""
    @abstractmethod
    def is_context_dependent(self, query: str) -> bool:
        """Kiểm tra câu hỏi có phụ thuộc ngữ cảnh trước đó hay không"""
        pass

    @abstractmethod
    def condense(self, raw_query: str, session: SessionContext) -> ContextualResolution:
        """Tái cấu trúc câu hỏi ngắn thành câu hỏi độc lập đầy đủ nghĩa"""
        pass

class IContextManager(ABC):
    """Giao diện quản lý bộ nhớ phiên và ngữ cảnh đa lượt"""
    @abstractmethod
    def get_context(self, session_id: str, tenant_id: str = "default") -> SessionContext:
        """Lấy ngữ cảnh hiện tại của phiên hội thoại"""
        pass

    @abstractmethod
    def save_turn(self, session_id: str, turn: ConversationTurn) -> None:
        """Lưu một lượt hội thoại vào cửa sổ trượt bộ nhớ"""
        pass

    @abstractmethod
    def resolve_query(self, session_id: str, raw_query: str) -> ContextualResolution:
        """Giải quyết câu hỏi ngữ cảnh trước khi đẩy vào Intent Router và RAG"""
        pass

    @abstractmethod
    def reset_context(self, session_id: str) -> None:
        """Xóa trắng ngữ cảnh phiên hội thoại"""
        pass
