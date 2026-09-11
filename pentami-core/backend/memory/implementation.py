"""
Triển khai cụ thể Module Quản Lý Ngữ Cảnh & Tái Cấu Trúc Truy Vấn Đa Lượt.
Tuân thủ Điều 1 (Guru Factory Pattern) và Điều 2 (Dual-Path Q&A Rule) trong GEMINI.md.
"""

import re
from typing import Dict, Any, List, Optional
from .interface import (
    IContextManager,
    IQueryCondenser,
    ConversationTurn,
    SessionContext,
    ContextualResolution
)

class FastQueryCondenser(IQueryCondenser):
    """
    Bộ tái cấu trúc truy vấn siêu tốc:
    Nhận diện câu hỏi ngắn, câu hỏi tỉnh lược hoặc đại từ quy chiếu,
    kết hợp với turn trước đó để tạo thành câu hỏi tự thân hoàn chỉnh (Self-contained Query).
    """

    # Danh sách từ chỉ thị quan hệ quy chiếu ngữ cảnh
    COREFERENCE_INDICATORS = [
        "tai sao", "tại sao", "tai sao vay", "tại sao vậy", "sao lai", "sao lại",
        "the con", "thế còn", "the thi", "thế thì", "con cai", "còn cái",
        "bang may", "bằng mấy", "bao nhieu", "bao nhiêu", "bao tien", "bao tiền",
        "giai thich", "giải thích", "ro hon", "rõ hơn", "chi tiet hon", "chi tiết hơn",
        "tinh lai", "tính lại", "tinh tiep", "tính tiếp", "tiep theo", "tiếp theo",
        "no o dau", "nó ở đâu", "cai do", "cái đó", "bai nay", "bài này",
        "ket qua do", "kết quả đó", "co giam gia khong", "có giảm giá không",
        "ap ma duoc khong", "áp mã được không", "tai sao am", "tại sao âm"
    ]

    def is_context_dependent(self, query: str) -> bool:
        normalized = query.strip().lower()
        words = normalized.split()
        
        # 1. Câu hỏi cực ngắn (dưới 5 từ)
        if len(words) <= 4:
            return True
            
        # 2. Chứa từ khóa quy chiếu ngữ cảnh
        for ind in self.COREFERENCE_INDICATORS:
            if ind in normalized:
                return True
                
        return False

    def condense(self, raw_query: str, session: SessionContext) -> ContextualResolution:
        normalized = raw_query.strip()
        is_dep = self.is_context_dependent(normalized)
        
        # Nếu không có lịch sử hoặc câu hỏi đã đủ dài và độc lập
        if not session.history or not is_dep:
            return ContextualResolution(
                raw_query=raw_query,
                condensed_query=raw_query,
                is_short_query=False,
                inherited_subsystem=session.active_subsystem,
                inherited_formula_ref=session.active_formula_ref,
                merged_variables=session.active_variables.copy()
            )

        # Lấy turn của user gần nhất và assistant gần nhất
        last_user_turn = None
        last_asst_turn = None
        for turn in reversed(session.history):
            if turn.role == "user" and not last_user_turn:
                last_user_turn = turn
            elif turn.role == "assistant" and not last_asst_turn:
                last_asst_turn = turn
            if last_user_turn and last_asst_turn:
                break

        # Kế thừa thông tin từ turn trước
        inherited_subsystem = session.active_subsystem
        inherited_formula = session.active_formula_ref
        merged_vars = session.active_variables.copy()

        # Tái cấu trúc câu hỏi
        topic_anchor = ""
        if last_user_turn:
            topic_anchor = last_user_turn.content.strip()
            # Bỏ dấu hỏi nếu có
            if topic_anchor.endswith("?"):
                topic_anchor = topic_anchor[:-1]

        condensed = raw_query
        lower_q = raw_query.lower()

        # Case 1: Hỏi "Tại sao..." về kết quả bài toán vừa giải
        if any(w in lower_q for w in ["tại sao", "tai sao", "sao lại", "sao lai"]):
            if last_asst_turn and ("nghiệm" in last_asst_turn.content.lower() or "=" in last_asst_turn.content):
                condensed = f"Tại sao khi {topic_anchor} lại ra kết quả như vậy? ({raw_query})"
            elif topic_anchor:
                condensed = f"Đối với '{topic_anchor}', {raw_query}"

        # Case 2: Hỏi "Thế còn...", "Còn..."
        elif lower_q.startswith("thế còn") or lower_q.startswith("the con") or lower_q.startswith("còn"):
            clean_sub = re.sub(r"^(thế còn|the con|còn|con)\s*", "", lower_q).strip()
            if topic_anchor:
                condensed = f"So với '{topic_anchor}', thì {clean_sub} như thế nào?"
            else:
                condensed = raw_query

        # Case 3: Hỏi "Bằng mấy?", "Tính lại xem?", "Tính tiếp đi"
        elif any(w in lower_q for w in ["bằng mấy", "bang may", "tính lại", "tinh lai", "tính tiếp", "tinh tiep"]):
            if topic_anchor:
                condensed = f"Thực hiện lại phép tính cho '{topic_anchor}': {raw_query}"

        # Case 4: Câu cộc lốc chung
        else:
            if topic_anchor:
                condensed = f"[Về ngữ cảnh: {topic_anchor}] - {raw_query}"

        return ContextualResolution(
            raw_query=raw_query,
            condensed_query=condensed,
            is_short_query=True,
            inherited_subsystem=inherited_subsystem,
            inherited_formula_ref=inherited_formula,
            merged_variables=merged_vars
        )

class MemoryContextManager(IContextManager):
    """
    Quản lý bộ nhớ ngữ cảnh phiên hội thoại (Sliding Window & Sticky Intent).
    Hỗ trợ lưu trữ in-memory tốc độ cao với cấu trúc sẵn sàng cắm Redis.
    """

    def __init__(self, max_history_turns: int = 6):
        self._sessions: Dict[str, SessionContext] = {}
        self._condenser = FastQueryCondenser()
        self._max_history = max_history_turns

    def get_context(self, session_id: str, tenant_id: str = "default") -> SessionContext:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionContext(
                session_id=session_id,
                tenant_id=tenant_id,
                max_history_turns=self._max_history
            )
        return self._sessions[session_id]

    def save_turn(self, session_id: str, turn: ConversationTurn) -> None:
        session = self.get_context(session_id)
        session.history.append(turn)
        
        # Giữ cửa sổ trượt bộ nhớ (Sliding window)
        if len(session.history) > session.max_history_turns * 2:
            session.history = session.history[-session.max_history_turns * 2:]

        # Cập nhật Sticky Intent & State Anchor nếu có thông tin mới
        if turn.subsystem:
            session.active_subsystem = turn.subsystem
        if turn.formula_ref:
            session.active_formula_ref = turn.formula_ref
        if turn.extracted_variables:
            session.active_variables.update(turn.extracted_variables)
        if turn.persona:
            session.active_persona = turn.persona

    def resolve_query(self, session_id: str, raw_query: str) -> ContextualResolution:
        session = self.get_context(session_id)
        return self._condenser.condense(raw_query, session)

    def reset_context(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
