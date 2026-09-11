"""
Registry quản lý instance toàn cục của Pentanote Engine.
Tuân thủ Điều 1 (Guru Factory Pattern) trong GEMINI.md.
"""

from typing import Optional
from .interface import IPentanoteEngine
from .factory import PentanoteFactory

class PentanoteRegistry:
    """Service Registry quản lý instance toàn cục của Pentanote"""
    _instance: Optional[IPentanoteEngine] = None

    @classmethod
    def get_instance(cls) -> IPentanoteEngine:
        if cls._instance is None:
            cls._instance = PentanoteFactory.create_engine()
        return cls._instance

    @classmethod
    def set_instance(cls, instance: IPentanoteEngine) -> None:
        cls._instance = instance
