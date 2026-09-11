"""
Registry đăng ký Module Quản Lý Ngữ Cảnh vào danh bạ dịch vụ của Penta AI.
Tuân thủ Điều 1 (Guru Factory Pattern) trong GEMINI.md.
"""

from typing import Optional
from .interface import IContextManager
from .factory import ContextFactory

class ContextRegistry:
    """Service Registry lưu trữ instance toàn cục của ContextManager"""
    _instance: Optional[IContextManager] = None

    @classmethod
    def get_instance(cls) -> IContextManager:
        if cls._instance is None:
            cls._instance = ContextFactory.create_context_manager()
        return cls._instance

    @classmethod
    def set_instance(cls, instance: IContextManager) -> None:
        cls._instance = instance
