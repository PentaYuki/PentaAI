"""
Bộ quản lý Prompt Hệ Thống & Cấu hình Model duy nhất gemini-3.1-flash-lite.
Tuân thủ Điều 1 (Guru Factory Pattern) và chỉ thị sử dụng mô hình gemini-3.1-flash-lite.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Mô hình cấu hình duy nhất theo yêu cầu nghiêm ngặt của dự án
MANDATORY_GEMINI_MODEL = "gemini-3.1-flash-lite"

class SystemPromptManager:
    """Quản lý tải và nạp System Prompt cho từng phân hệ trong Hệ Sinh Thái Penta AI"""

    def __init__(self, prompt_dir: Optional[str] = None):
        if prompt_dir is None:
            self._dir = Path(__file__).resolve().parent / "system_prompts"
        else:
            self._dir = Path(prompt_dir)
        self._cache: Dict[str, str] = {}

    @property
    def model_name(self) -> str:
        return MANDATORY_GEMINI_MODEL

    def get_prompt(self, subsystem: str) -> str:
        """
        Lấy System Prompt cho phân hệ:
        pentami_core | pentaschool | pentakuru | pentamarket | pentajob | pentanote
        """
        subsystem = subsystem.replace("-", "_").lower()
        if subsystem in self._cache:
            return self._cache[subsystem]

        file_path = self._dir / f"{subsystem}.md"
        if not file_path.exists():
            raise FileNotFoundError(f"System prompt file not found: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        self._cache[subsystem] = content
        return content

    def parse_datasheet_patch(self, llm_response: str) -> Optional[Dict[str, Any]]:
        """
        Tự động bóc tách khối JSON datasheet_patch từ phản hồi của mô hình
        để hỗ trợ nâng cấp datasheet tự động.
        """
        # Tìm khối json có chứa "datasheet_patch"
        pattern = r"```json\s*(\{[\s\S]*?\"datasheet_patch\"[\s\S]*?\})\s*```"
        match = re.search(pattern, llm_response)
        if match:
            try:
                data = json.loads(match.group(1))
                return data.get("datasheet_patch")
            except Exception:
                pass

        # Thử tìm trực tiếp khối object JSON
        pattern2 = r"(\{\s*\"datasheet_patch\"\s*:\s*\{[\s\S]*?\}\s*\})"
        match2 = re.search(pattern2, llm_response)
        if match2:
            try:
                data = json.loads(match2.group(1))
                return data.get("datasheet_patch")
            except Exception:
                pass

        return None
