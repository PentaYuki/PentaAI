"""
Penta Unified API Key & IAM Manager
Quản lý vòng đời, xác thực, hashing và phân quyền Scopes cho toàn bộ hệ sinh thái Penta.
"""

import hashlib
import hmac
import secrets
import time
from typing import List, Optional, Set, Tuple

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    from dataclasses import dataclass, field, asdict
    HAS_PYDANTIC = False
    
    class BaseModel:
        def model_dump(self):
            return asdict(self)
            
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


@pydantic_or_dataclass
class APIKeyMetadata(BaseModel):
    key_id: str
    user_id: str
    tenant_id: str
    name: str
    scopes: List[str] = Field(default_factory=list)
    rate_limit_rpm: int = 120
    is_active: bool = True
    created_at: int = Field(default_factory=lambda: int(time.time()))
    expires_at: Optional[int] = None


class UnifiedKeyManager:
    """
    Quản lý sinh khóa, băm HMAC-SHA256 và kiểm tra phân quyền.
    """
    def __init__(self, master_secret: str = "penta_default_master_secret_2026"):
        self.master_secret = master_secret.encode("utf-8")

    def generate_key(self, environment: str = "live", key_type: str = "sk") -> Tuple[str, str]:
        """
        Sinh cặp:
        - raw_key: Trả về cho User đúng 1 lần duy nhất (ví dụ: penta_live_sk_8f9c1...)
        - key_hash: Lưu trong DB & Redis
        """
        random_bytes = secrets.token_hex(24) # 48 ký tự hex ngẫu nhiên
        raw_key = f"penta_{environment}_{key_type}_{random_bytes}"
        key_hash = self.hash_key(raw_key)
        return raw_key, key_hash

    def hash_key(self, raw_key: str) -> str:
        """
        Băm khóa bí mật bằng HMAC-SHA256 với Master Secret để chống Rainbow Tables.
        """
        return hmac.new(
            self.master_secret,
            raw_key.strip().encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def has_required_scopes(self, user_scopes: List[str], required_scopes: List[str]) -> bool:
        """
        Kiểm tra người dùng có đủ quyền thực hiện hành động không.
        Hỗ trợ wildcard '*' (ví dụ: 'penta:school:*' bao hàm 'penta:school:read')
        """
        user_scope_set: Set[str] = set(user_scopes)
        
        # Nếu có quyền siêu quản trị toàn hệ sinh thái
        if "penta:*" in user_scope_set or "*" in user_scope_set:
            return True

        for req in required_scopes:
            matched = False
            if req in user_scope_set:
                matched = True
            else:
                # Kiểm tra tiền tố wildcard
                parts = req.split(":")
                prefix = ""
                for part in parts[:-1]:
                    prefix = f"{prefix}{part}:" if prefix else f"{part}:"
                    if f"{prefix}*" in user_scope_set:
                        matched = True
                        break
            if not matched:
                return False
        return True
