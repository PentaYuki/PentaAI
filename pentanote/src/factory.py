"""
Factory khởi tạo cho phân hệ Pentanote (Notion-grade Block Engine).
Tuân thủ Điều 1 (Guru Factory Pattern) trong GEMINI.md.
"""

from .interface import IPentanoteEngine
from .implementation import PentanoteEngineImpl

class PentanoteFactory:
    """Factory chịu trách nhiệm tạo instance của PentanoteEngine"""

    @staticmethod
    def create_engine() -> IPentanoteEngine:
        return PentanoteEngineImpl()
