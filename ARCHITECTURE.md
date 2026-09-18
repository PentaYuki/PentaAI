
# Kiến trúc Penta AI (Cập nhật ngày 18/09/2026)

## 1. Hạ tầng (Infrastructure)
- Đã cấu hình Docker Compose với các cổng cố định:
  - PostgreSQL: 5432
  - Redis: 6379
  - Qdrant: 6333 (API), 6334 (GRPC)
- Trạng thái: Có file Compose; chưa có bằng chứng runtime trong repository rằng các service đang chạy hoặc đã được backend sử dụng.

## 2. Backend hiện tại
- `pentami-core/backend/main.py` là FastAPI entrypoint tối thiểu.
- Endpoint thực tế: `GET /api/health`, `GET /api/ecosystem/apps` và `POST /api/chat`.
- `/api/chat` chỉ nhận `query` và trả về `{"response": "Received: ..."}`.
- Backend chưa mount frontend, chưa kết nối PostgreSQL, Redis, Qdrant, LLM, RAG, memory, voice hoặc MCP.

## 3. Phân loại trạng thái
- `implemented`: FastAPI entrypoint và ba endpoint tối thiểu; Compose file ở mức cấu hình local.
- `prepared`: frontend, shared contracts, memory, RAG, voice, auth helper và datasets.
- `roadmap`: tích hợp database/cache/vector store, routing, auth middleware, persistence, streaming, MCP transport và service domain.

Không gọi hệ thống là production-ready hoặc high availability cho tới khi có healthcheck runtime, dependency wiring, test tích hợp và hướng dẫn triển khai kiểm chứng được.
