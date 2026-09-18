"""
Penta Unified JWT Authentication Module
Quản lý sinh mã Token, mã hóa mật khẩu và xác thực người dùng cho toàn bộ hệ sinh thái Penta.
"""

import os
import time
import secrets
import hashlib
import hmac
from typing import Dict, Any, Optional, List
import jwt

# Cấu hình Secret & Thuật toán
JWT_SECRET_KEY = os.getenv("PENTA_JWT_SECRET", "penta_core_jwt_master_secret_key_2026_secured")
JWT_ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_SECONDS = 86400 * 7   # 7 ngày
DEFAULT_REFRESH_TOKEN_EXPIRE_SECONDS = 86400 * 30 # 30 ngày


# ==========================================
# 1. Password Hashing (PBKDF2-HMAC-SHA256)
# ==========================================
def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Mã hóa mật khẩu bằng PBKDF2-HMAC-SHA256 với 100,000 vòng lặp"""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu khớp với hash đã lưu"""
    try:
        parts = hashed_password.split("$")
        if len(parts) != 2:
            return False
        salt, expected_hash = parts
        candidate_hash = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return hmac.compare_digest(candidate_hash, expected_hash)
    except Exception:
        return False


# ==========================================
# 2. JWT Token Generation & Verification
# ==========================================
def create_access_token(
    user_id: str,
    penta_id: str,
    role: str,
    scopes: Optional[List[str]] = None,
    expires_in_seconds: int = DEFAULT_ACCESS_TOKEN_EXPIRE_SECONDS,
    custom_claims: Optional[Dict[str, Any]] = None
) -> str:
    """Tạo JWT Access Token cho User"""
    now = int(time.time())
    payload: Dict[str, Any] = {
        "sub": user_id,
        "penta_id": penta_id,
        "role": role,
        "scopes": scopes or ["penta:chat", "penta:school:read"],
        "token_type": "access",
        "iat": now,
        "exp": now + expires_in_seconds,
    }
    if custom_claims:
        payload.update(custom_claims)
        
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(
    user_id: str,
    expires_in_seconds: int = DEFAULT_REFRESH_TOKEN_EXPIRE_SECONDS
) -> str:
    """Tạo JWT Refresh Token dài hạn"""
    now = int(time.time())
    payload = {
        "sub": user_id,
        "token_type": "refresh",
        "iat": now,
        "exp": now + expires_in_seconds,
        "jti": secrets.token_hex(16)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Giải mã và kiểm tra tính hợp lệ của token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Xác thực access token cụ thể"""
    payload = decode_token(token)
    if not payload or payload.get("token_type") != "access":
        return None
    return payload
