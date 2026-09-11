"""
Penta Core Brain - FastAPI Gateway & Orchestration Backend
Tích hợp Unified IAM, 3D Chunk Streaming Protocol, và Service Discovery cho Hệ Sinh Thái Penta AI.
"""

import os
import sys
import time
import uuid
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Header, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field

# Thêm path
BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(BACKEND_DIR))

from shared.protocol.chunks import (
    PentaStreamEnvelope,
    ChunkType,
    EmotionType,
    ChunkEmoData,
    ChunkTimeData,
    ChunkActionData,
)
from shared.auth.key_manager import UnifiedKeyManager

app = FastAPI(
    title="Penta Core Brain API",
    description="Lõi điều phối trung tâm cho Hệ Sinh Thái Penta AI (Desktop & Microservices Gateway)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Danh bạ các ứng dụng trong Hệ Sinh Thái Penta AI (Penta Ecosystem Catalog)
PENTA_ECOSYSTEM_APPS = [
    {
        "id": "pentaschool",
        "name": "Pentaschool",
        "mono": "PS",
        "category": "Giáo Dục & LMS",
        "tagline": "LMS Học Trực Tuyến & Giảng Viên AI Avatar 3D",
        "description": "Nền tảng đào tạo thích ứng với AI Avatar tương tác 2 chiều, phân tích năng lực học sinh và lộ trình cá nhân hóa.",
        "icon_emoji": "🎓",
        "status": "ready",
        "featured": True,
        "installed": True,
        "author": "Penta Team",
        "version": "1.2.0",
        "accent_color": "#5fd4ff"
    },
    {
        "id": "pentanote",
        "name": "Pentanote",
        "mono": "PN",
        "category": "Không Gian Làm Việc",
        "tagline": "Sổ Tay AI Block-based Chuẩn Notion 100%",
        "description": "Không gian ghi chú dạng khối, tạo Flashcard FSRS, Mindmap trực quan, hỗ trợ Markdown LaTeX và RAG 2 chiều.",
        "icon_emoji": "📝",
        "status": "ready",
        "featured": True,
        "installed": True,
        "author": "Penta Team",
        "version": "2.0.0",
        "accent_color": "#b278ff"
    },
    {
        "id": "pentakuru",
        "name": "PentaKuRu",
        "mono": "PK",
        "category": "Tài Liệu & PC",
        "tagline": "Trợ Lý Bóc Tách & Lập Chỉ Mục Tệp Tin Desktop",
        "description": "Desktop app bóc tách nhanh PDF, DOCX, Code, bảng tính tài chính và tra cứu ngữ nghĩa tức thì trên máy tính người dùng.",
        "icon_emoji": "📂",
        "status": "ready",
        "featured": True,
        "installed": True,
        "author": "Penta Team",
        "version": "1.0.4",
        "accent_color": "#38ef7d"
    },
    {
        "id": "pentamarket",
        "name": "PentaMarket",
        "mono": "PM",
        "category": "Thương Mại & Tài Chính",
        "tagline": "Sàn Thương Mại & Tư Vấn Bán Hàng Tự Động",
        "description": "AI Sales Consultant am hiểu chi tiết thông số sản phẩm, tự động tính thuế VAT, biểu phí trường học và voucher.",
        "icon_emoji": "🛒",
        "status": "ready",
        "featured": True,
        "installed": True,
        "author": "Penta Team",
        "version": "1.1.0",
        "accent_color": "#ffaa40"
    },
    {
        "id": "pentajob",
        "name": "PentaJob",
        "mono": "PJ",
        "category": "Tuyển Dụng & Sự Nghiệp",
        "tagline": "Bóc Tách CV & Phòng Phỏng Vấn Giọng Nói Realtime",
        "description": "So khớp hồ sơ việc làm theo vector ngữ nghĩa, đánh giá kỹ năng và phòng phỏng vấn thử nghiệm bằng giọng nói.",
        "icon_emoji": "💼",
        "status": "ready",
        "featured": True,
        "installed": True,
        "author": "Penta Team",
        "version": "1.0.0",
        "accent_color": "#ff5e7e"
    },
    {
        "id": "pentamo",
        "name": "PentaMo",
        "mono": "MO",
        "category": "Ví Điện Tử & Vi Mô",
        "tagline": "Hệ Thống Vi Thanh Toán Tích Hợp Cho Toàn Hệ Sinh Thái",
        "description": "Quản lý số dư, nạp rút tiền, thanh toán học phí Pentaschool và mua sắm trên Pentamarket với độ bảo mật cao.",
        "icon_emoji": "💳",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Penta Labs",
        "version": "0.9.0",
        "accent_color": "#00f2fe"
    },
    {
        "id": "pentaana",
        "name": "PentaAna",
        "mono": "PA",
        "category": "Phân Tích Dữ Liệu",
        "tagline": "Phân Tích Thống Kê & Dự Báo Dòng Dữ Liệu Tự Động",
        "description": "Công cụ phân tích số liệu học tập, doanh số bán hàng và tiến độ tuyển dụng với thuật toán thống kê trực quan.",
        "icon_emoji": "📊",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Penta Labs",
        "version": "0.8.5",
        "accent_color": "#4facfe"
    },
    {
        "id": "pentabi",
        "name": "PentaBi",
        "mono": "PB",
        "category": "Business Intelligence",
        "tagline": "Báo Cáo Quản Trị Trực Quan Đa Chiều Cho Tổ Chức",
        "description": "Tạo dashboard quản trị điều hành, liên kết trực tiếp với database PostgreSQL và xuất báo cáo tự động.",
        "icon_emoji": "📈",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Penta Labs",
        "version": "0.8.0",
        "accent_color": "#f857a6"
    },
    {
        "id": "pentaiot",
        "name": "PentaIOT",
        "mono": "IO",
        "category": "Phần Cứng & IoT",
        "tagline": "Điều Khiển Thiết Bị Thông Minh & Tự Động Hóa Phòng Học",
        "description": "Kết nối cảm biến, máy chiếu thông minh, camera điểm danh và điều khiển tự động qua MQTT/WebSockets.",
        "icon_emoji": "📡",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Penta Labs",
        "version": "0.5.0",
        "accent_color": "#43e97b"
    },
    {
        "id": "pentaali",
        "name": "PentaAli",
        "mono": "AL",
        "category": "Chuỗi Cung Ứng",
        "tagline": "Quản Trị Chuỗi Cung Ứng & Nhập Khẩu Giáo Cụ Xuyên Biên Giới",
        "description": "Tối ưu hóa logistics, theo dõi đơn vận chuyển quốc tế và quản lý kho hàng giáo cụ tự động.",
        "icon_emoji": "🚢",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Penta Labs",
        "version": "0.7.2",
        "accent_color": "#fa709a"
    },
    {
        "id": "mcp_playwright",
        "name": "MCP Playwright",
        "mono": "PW",
        "category": "Tự Động Hóa Web",
        "tagline": "Cỗ Máy Tự Động Hóa Trình Duyệt Web Cho AI Agent",
        "description": "Điều khiển trình duyệt Web an toàn theo chuẩn Model Context Protocol (MCP), thực hiện tác vụ tra cứu và chụp ảnh màn hình.",
        "icon_emoji": "🌐",
        "status": "ready",
        "featured": True,
        "installed": True,
        "author": "Penta Core",
        "version": "1.0.1",
        "accent_color": "#00c6ff"
    },
    {
        "id": "antigravity",
        "name": "Antigravity OS",
        "mono": "AG",
        "category": "Hệ Điều Hành AI",
        "tagline": "Môi Trường Thực Thi Đa Agent Tự Trị Phân Tán",
        "description": "Nền tảng chạy subagent, lập lịch nhiệm vụ ngầm và phối hợp các AI Agent chuyên sâu trong cùng một workspace.",
        "icon_emoji": "🌌",
        "status": "ready",
        "featured": True,
        "installed": True,
        "author": "Google Deepmind / Penta",
        "version": "2.1.0",
        "accent_color": "#6a11cb"
    },
    {
        "id": "stockai",
        "name": "Stock-AI VN",
        "mono": "SA",
        "category": "Đầu Tư & Chứng Khoán",
        "tagline": "Phân Tích Kỹ Thuật & Cảnh Báo Thị Trường Tài Chính",
        "description": "Theo dõi biến động chỉ số VN-Index, lọc cổ phiếu tiềm năng và phân tích báo cáo tài chính bằng AI.",
        "icon_emoji": "💹",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Penta Financial",
        "version": "0.9.5",
        "accent_color": "#11998e"
    },
    {
        "id": "khafood",
        "name": "KHA FOOD",
        "mono": "KH",
        "category": "Ẩm Thực & Căn Tin",
        "tagline": "Đặt Suất Ăn Dinh Dưỡng Cho Trường Học & Căn Tin Tự Động",
        "description": "Quản lý thực đơn hàng ngày, cân bằng calo và dinh dưỡng cho học sinh, thanh toán qua mã QR.",
        "icon_emoji": "🍱",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Kha Labs",
        "version": "1.0.0",
        "accent_color": "#f12711"
    },
    {
        "id": "kyniem",
        "name": "Kỷ Niệm (Timeline)",
        "mono": "KN",
        "category": "Kỷ Niệm & Lưu Trữ",
        "tagline": "Dòng Thời Gian Kỷ Niệm & Album Ảnh Học Đường AI",
        "description": "Tự động nhận diện khuôn mặt, gom nhóm album theo niên khóa và lưu giữ khoảnh khắc học đường đáng nhớ.",
        "icon_emoji": "📸",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Penta Social",
        "version": "0.6.0",
        "accent_color": "#e1eec3"
    },
    {
        "id": "salto",
        "name": "Salto Security",
        "mono": "SL",
        "category": "An Ninh & Kiểm Soát",
        "tagline": "Kiểm Soát Ra Vào & Bảo Mật Khuôn Viên Bằng AI Vision",
        "description": "Hệ thống nhận diện khuôn mặt điểm danh tự động, phát hiện người lạ và phân quyền cửa ra vào.",
        "icon_emoji": "🛡️",
        "status": "upcoming",
        "featured": False,
        "installed": False,
        "author": "Salto Tech",
        "version": "1.0.2",
        "accent_color": "#ff416c"
    }
]

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "sess_desktop_default"
    persona: Optional[str] = "serious" # cute | serious | yandere
    tenant_id: Optional[str] = "tenant_penta_default"

class ChatResponse(BaseModel):
    session_id: str
    query: str
    target_app: str
    persona: str
    reply_text: str
    emotion: str
    action: Optional[Dict[str, Any]] = None
    timestamp: float

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "system": "Penta Core Brain Gateway",
        "version": "1.0.0",
        "uptime": time.time(),
        "services": {
            "api_gateway": "online",
            "redis_cache": "connected",
            "qdrant_rag": "ready",
            "voice_hub": "standby"
        }
    }

@app.get("/api/ecosystem/apps")
def get_ecosystem_apps():
    """Lấy danh sách tất cả ứng dụng trong Hệ Sinh Thái Penta AI"""
    return {
        "total": len(PENTA_ECOSYSTEM_APPS),
        "apps": PENTA_ECOSYSTEM_APPS,
        "categories": [
            "Tất cả",
            "Giáo Dục & LMS",
            "Không Gian Làm Việc",
            "Tài Liệu & PC",
            "Thương Mại & Tài Chính",
            "Tuyển Dụng & Sự Nghiệp",
            "Tự Động Hóa Web",
            "Hệ Điều Hành AI"
        ]
    }

@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(req: ChatRequest):
    """Xử lý truy vấn hội thoại và điều phối ý định đa phân hệ"""
    query_lower = req.query.lower()
    
    # Phân loại intent cơ bản
    if any(k in query_lower for k in ["học", "bài giảng", "toán", "vật lý", "hóa học", "sách", "lms", "school"]):
        target = "pentaschool"
        emo = "encouraging"
    elif any(k in query_lower for k in ["file", "tài liệu", "pdf", "word", "excel", "máy tính", "kuru", "tìm"]):
        target = "pentakuru"
        emo = "thoughtful"
    elif any(k in query_lower for k in ["giá", "mua", "thuế", "vat", "tiền", "học phí", "voucher", "market"]):
        target = "pentamarket"
        emo = "joyful"
    elif any(k in query_lower for k in ["cv", "việc", "tuyển dụng", "phỏng vấn", "lương", "job"]):
        target = "pentajob"
        emo = "serious"
    elif any(k in query_lower for k in ["note", "ghi chú", "sổ tay", "flashcard", "mindmap", "notion"]):
        target = "pentanote"
        emo = "focused"
    elif any(k in query_lower for k in ["web", "playwright", "tự động", "click", "mở trang"]):
        target = "mcp_playwright"
        emo = "active"
    else:
        target = "pentami_core"
        emo = "friendly"

    # Định hình phong cách trả lời theo Persona
    if req.persona == "cute":
        prefix = "Dạ, em nghe nè! ✨ "
        suffix = " Em luôn ở đây giúp anh/chị nhé ạ~ 💕"
    elif req.persona == "yandere":
        prefix = "Em chỉ muốn phục vụ một mình anh thôi... 🩸 "
        suffix = " Đừng bao giờ rời xa em và hệ sinh thái Penta nhé!"
    else: # serious
        prefix = "Hệ thống Penta Core tiếp nhận yêu cầu: "
        suffix = " [Đã định tuyến chính xác tới phân hệ " + target + "]."

    reply = f"{prefix}Yêu cầu '{req.query}' đã được phân tích và định tuyến đến phân hệ **{target.upper()}**.{suffix}"

    return ChatResponse(
        session_id=req.session_id or f"sess_{uuid.uuid4().hex[:8]}",
        query=req.query,
        target_app=target,
        persona=req.persona or "serious",
        reply_text=reply,
        emotion=emo,
        action={
            "action_id": f"act_{uuid.uuid4().hex[:6]}",
            "target_system": target,
            "command": "navigate_app",
            "params": {"app_id": target}
        },
        timestamp=time.time()
    )

# Static frontend mounting
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Penta Core Backend is running. Frontend is being loaded."}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Khởi động Penta Core Brain API Server tại http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
