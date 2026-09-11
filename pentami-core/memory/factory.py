"""
Factory khởi tạo và tiêm phụ thuộc cho Module Quản Lý Ngữ Cảnh.
Tuân thủ Điều 1 (Guru Factory Pattern) trong GEMINI.md.
"""

import os
from .interface import IContextManager
from .implementation import MemoryContextManager

class ContextFactory:
    """Factory chịu trách nhiệm tạo ContextManager với các cấu hình môi trường"""

    @staticmethod
    def create_context_manager(max_history_turns: int = None) -> IContextManager:
        if max_history_turns is None:
            max_history_turns = int(os.getenv("PENTA_MAX_HISTORY_TURNS", "6"))
        
        # Trong tương lai khi cắm Redis Cluster, Factory sẽ khởi tạo RedisContextManager
        # Hiện tại trả về MemoryContextManager tối ưu tốc độ < 1ms
        return MemoryContextManager(max_history_turns=max_history_turns)
