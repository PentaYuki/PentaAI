"""
Hợp đồng trừu tượng (Interface) cho phân hệ Pentanote (Notion-grade Block Engine).
Hỗ trợ liên kết toàn diện với toàn bộ Hệ Sinh Thái Penta AI (Ecosystem Integration).
Tuân thủ Điều 1 (Guru Factory Pattern) và Điều 2 trong GEMINI.md.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time

class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    TO_DO = "to_do"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    TOGGLE = "toggle"
    CALLOUT = "callout"
    QUOTE = "quote"
    DIVIDER = "divider"
    CODE = "code"
    EQUATION = "equation"
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"
    COLUMN_LIST = "column_list"
    COLUMN = "column"
    CHILD_PAGE = "child_page"
    CHILD_DATABASE = "child_database"
    # Khối liên kết hệ sinh thái Penta AI
    ECOSYSTEM_EMBED = "ecosystem_embed"

class EcosystemRefType(str, Enum):
    """Các phân hệ và thực thể liên kết trong Hệ Sinh Thái Penta AI"""
    PENTASCHOOL_LESSON = "pentaschool:lesson"       # Nhúng bài giảng & tài liệu LMS
    PENTAKURU_LOCAL_FILE = "pentakuru:file"         # Tệp tin & tóm tắt từ máy tính cá nhân
    PENTAMARKET_ITEM = "pentamarket:item"           # Sản phẩm, danh mục, tài liệu
    PENTAJOB_CV = "pentajob:cv_interview"          # CV, lộ trình nghề nghiệp & mock interview
    PLAYWRIGHT_ACTION = "mcp_playwright:action"     # Snapshot web & tác vụ tự động hóa
    PENTAMI_KNOWLEDGE = "pentami:knowledge"         # Khối tri thức RAG từ Penta Core

class DatabaseViewType(str, Enum):
    TABLE = "table"
    BOARD = "board"
    GALLERY = "gallery"
    CALENDAR = "calendar"
    LIST = "list"

@dataclass
class TextSpan:
    content: str
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str = "default"

@dataclass
class EcosystemLinkData:
    ref_type: EcosystemRefType
    ref_id: str
    title: str
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    sync_status: str = "synced"

@dataclass
class BlockItem:
    id: str
    parent_id: str
    type: BlockType
    content: List[TextSpan] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    children: List[str] = field(default_factory=list)  # Danh sách ID các block con (Nested Tree)
    ecosystem_link: Optional[EcosystemLinkData] = None # Khối liên kết đa phân hệ
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

@dataclass
class DatabaseSchema:
    id: str
    parent_id: str
    title: str
    properties: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    active_views: List[DatabaseViewType] = field(default_factory=lambda: [DatabaseViewType.TABLE])

class IPentanoteEngine(ABC):
    """Giao diện động cơ quản lý không gian làm việc dạng khối chuẩn Notion 100%"""

    @abstractmethod
    def create_page(self, parent_id: str, title: str, icon: str = "📄") -> BlockItem:
        """Tạo trang mới chuẩn Notion"""
        pass

    @abstractmethod
    def append_blocks(self, parent_id: str, blocks: List[BlockItem]) -> List[BlockItem]:
        """Thêm các khối con vào trang hoặc khối cha"""
        pass

    @abstractmethod
    def get_block(self, block_id: str) -> Optional[BlockItem]:
        """Lấy thông tin chi tiết một khối"""
        pass

    @abstractmethod
    def get_children(self, block_id: str) -> List[BlockItem]:
        """Lấy danh sách các khối con cấp 1"""
        pass

    @abstractmethod
    def update_block(self, block_id: str, updates: Dict[str, Any]) -> BlockItem:
        """Cập nhật nội dung hoặc thuộc tính khối"""
        pass

    @abstractmethod
    def delete_block(self, block_id: str) -> bool:
        """Xóa khối (hỗ trợ xóa đệ quy cây con)"""
        pass

    @abstractmethod
    def create_database(self, parent_id: str, schema: DatabaseSchema) -> DatabaseSchema:
        """Tạo Database với các thuộc tính linh hoạt chuẩn Notion"""
        pass

    @abstractmethod
    def embed_ecosystem_block(self, parent_id: str, link_data: EcosystemLinkData) -> BlockItem:
        """Nhúng khối liên kết tương tác với một phân hệ bất kỳ trong hệ sinh thái"""
        pass

    @abstractmethod
    def export_to_vector_rag(self, page_id: str) -> Dict[str, Any]:
        """Đóng gói toàn bộ cây khối của trang thành tài liệu RAG nạp vào pentami-core"""
        pass
