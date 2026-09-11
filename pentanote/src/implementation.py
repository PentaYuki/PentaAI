"""
Triển khai cụ thể Động cơ Khối Pentanote (100% Notion Block Engine & Liên Kết Toàn Hệ Sinh Thái).
Tuân thủ Điều 1 (Guru Factory Pattern) trong GEMINI.md.
"""

from typing import Dict, Any, List, Optional
import uuid
import time
from .interface import (
    IPentanoteEngine,
    BlockItem,
    BlockType,
    TextSpan,
    DatabaseSchema,
    DatabaseViewType,
    EcosystemLinkData,
    EcosystemRefType
)

class PentanoteEngineImpl(IPentanoteEngine):
    """Động cơ quản lý Block Tree, Database chuẩn Notion và Liên kết Hệ Sinh Thái"""

    def __init__(self):
        self._blocks: Dict[str, BlockItem] = {}
        self._databases: Dict[str, DatabaseSchema] = {}

    def create_page(self, parent_id: str, title: str, icon: str = "📄") -> BlockItem:
        page_id = f"page_{uuid.uuid4().hex[:12]}"
        page_block = BlockItem(
            id=page_id,
            parent_id=parent_id,
            type=BlockType.CHILD_PAGE,
            content=[TextSpan(content=title, bold=True)],
            properties={"title": title, "icon": icon},
            children=[]
        )
        self._blocks[page_id] = page_block
        
        if parent_id in self._blocks:
            self._blocks[parent_id].children.append(page_id)
            
        return page_block

    def append_blocks(self, parent_id: str, blocks: List[BlockItem]) -> List[BlockItem]:
        parent = self._blocks.get(parent_id)
        saved_blocks: List[BlockItem] = []
        
        for b in blocks:
            if not b.id:
                b.id = f"blk_{uuid.uuid4().hex[:12]}"
            b.parent_id = parent_id
            b.updated_at = time.time()
            self._blocks[b.id] = b
            saved_blocks.append(b)
            
            if parent and b.id not in parent.children:
                parent.children.append(b.id)
                
        return saved_blocks

    def get_block(self, block_id: str) -> Optional[BlockItem]:
        return self._blocks.get(block_id)

    def get_children(self, block_id: str) -> List[BlockItem]:
        parent = self._blocks.get(block_id)
        if not parent:
            return []
        return [self._blocks[cid] for cid in parent.children if cid in self._blocks]

    def update_block(self, block_id: str, updates: Dict[str, Any]) -> BlockItem:
        block = self._blocks.get(block_id)
        if not block:
            raise KeyError(f"Block not found: {block_id}")
            
        if "content" in updates:
            block.content = updates["content"]
        if "properties" in updates:
            block.properties.update(updates["properties"])
        if "type" in updates:
            block.type = updates["type"]
        if "ecosystem_link" in updates:
            block.ecosystem_link = updates["ecosystem_link"]
            
        block.updated_at = time.time()
        return block

    def delete_block(self, block_id: str) -> bool:
        block = self._blocks.get(block_id)
        if not block:
            return False
            
        for cid in list(block.children):
            self.delete_block(cid)
            
        parent = self._blocks.get(block.parent_id)
        if parent and block_id in parent.children:
            parent.children.remove(block_id)
            
        del self._blocks[block_id]
        return True

    def create_database(self, parent_id: str, schema: DatabaseSchema) -> DatabaseSchema:
        if not schema.id:
            schema.id = f"db_{uuid.uuid4().hex[:12]}"
        schema.parent_id = parent_id
        self._databases[schema.id] = schema
        
        db_block = BlockItem(
            id=schema.id,
            parent_id=parent_id,
            type=BlockType.CHILD_DATABASE,
            content=[TextSpan(content=schema.title, bold=True)],
            properties={"title": schema.title}
        )
        self._blocks[schema.id] = db_block
        if parent_id in self._blocks:
            self._blocks[parent_id].children.append(schema.id)
            
        return schema

    def embed_ecosystem_block(self, parent_id: str, link_data: EcosystemLinkData) -> BlockItem:
        """Nhúng khối liên kết hệ sinh thái (Pentaschool, Pentakuru, Pentamarket, PentaJob, Playwright)"""
        block_id = f"eco_{uuid.uuid4().hex[:12]}"
        icon_map = {
            EcosystemRefType.PENTASCHOOL_LESSON: "🎓",
            EcosystemRefType.PENTAKURU_LOCAL_FILE: "📂",
            EcosystemRefType.PENTAMARKET_ITEM: "🛒",
            EcosystemRefType.PENTAJOB_CV: "💼",
            EcosystemRefType.PLAYWRIGHT_ACTION: "🌐",
            EcosystemRefType.PENTAMI_KNOWLEDGE: "🧠"
        }
        icon = icon_map.get(link_data.ref_type, "🔗")
        
        block = BlockItem(
            id=block_id,
            parent_id=parent_id,
            type=BlockType.ECOSYSTEM_EMBED,
            content=[
                TextSpan(content=f"{icon} [{link_data.ref_type.value}] {link_data.title}\n", bold=True),
                TextSpan(content=f"Tóm tắt: {link_data.summary}", italic=True)
            ],
            properties={
                "ref_type": link_data.ref_type.value,
                "ref_id": link_data.ref_id,
                "sync_status": link_data.sync_status
            },
            ecosystem_link=link_data
        )
        
        self._blocks[block_id] = block
        parent = self._blocks.get(parent_id)
        if parent:
            parent.children.append(block_id)
            
        return block

    def export_to_vector_rag(self, page_id: str) -> Dict[str, Any]:
        """Trích xuất và phẳng hóa toàn bộ cây block của trang thành tài liệu RAG nạp vào pentami-core"""
        page = self._blocks.get(page_id)
        if not page:
            raise KeyError(f"Page not found: {page_id}")
            
        page_title = page.properties.get("title", "Untitled")
        text_lines: List[str] = [f"# {page_title}"]
        
        def traverse(block_id: str):
            b = self._blocks.get(block_id)
            if not b:
                return
            line_text = "".join([span.content for span in b.content])
            if b.type == BlockType.HEADING_1:
                text_lines.append(f"\n# {line_text}")
            elif b.type == BlockType.HEADING_2:
                text_lines.append(f"\n## {line_text}")
            elif b.type == BlockType.HEADING_3:
                text_lines.append(f"\n### {line_text}")
            elif b.type == BlockType.TO_DO:
                checked = b.properties.get("checked", False)
                mark = "[x]" if checked else "[ ]"
                text_lines.append(f"- {mark} {line_text}")
            elif b.type == BlockType.BULLETED_LIST_ITEM:
                text_lines.append(f"- {line_text}")
            elif b.type == BlockType.EQUATION:
                text_lines.append(f"$$\n{line_text}\n$$")
            elif b.type == BlockType.CALLOUT:
                text_lines.append(f"> 💡 {line_text}")
            elif b.type == BlockType.ECOSYSTEM_EMBED and b.ecosystem_link:
                text_lines.append(f"\n[LIÊN KẾT HỆ SINH THÁI: {b.ecosystem_link.ref_type.value}] {b.ecosystem_link.title} - {b.ecosystem_link.summary}")
            elif line_text.strip():
                text_lines.append(line_text)
                
            for child_id in b.children:
                traverse(child_id)
                
        for child_id in page.children:
            traverse(child_id)
            
        full_text = "\n".join(text_lines)
        return {
            "page_id": page_id,
            "title": page_title,
            "full_content": full_text,
            "block_count": len(self._blocks),
            "app": "pentanote",
            "export_ts": time.time()
        }
