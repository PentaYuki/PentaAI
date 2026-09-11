# Tài liệu kiến trúc

Tài liệu kiến trúc chuẩn của repository nằm ở [ARCHITECTURE.md](../../ARCHITECTURE.md).

## Phân biệt hiện trạng và thiết kế

- `pentami-core/backend/main.py` là FastAPI entrypoint đang chạy được.
- `shared/` chứa contract/helper Python dùng chung.
- `deploy/docker-compose.yml` chỉ khởi chạy PostgreSQL, Redis và Qdrant; backend chưa kết nối chúng trong `/api/chat`.
- Các thư mục domain app và `mcp-playwright` hiện chưa được Compose khởi chạy như service độc lập.
- Memory, RAG, voice, authentication middleware, streaming và service-to-service calls là các capability đang cần tích hợp thêm, không mặc định là capability của API hiện tại.

## Quy tắc cập nhật

Mọi sơ đồ hoặc mô tả mới phải ghi rõ một trong ba trạng thái:

1. `implemented`: có code, entrypoint và test/smoke check;
2. `prepared`: có cấu hình hoặc helper nhưng chưa được gọi trong flow chính;
3. `roadmap`: mới là thiết kế hoặc kế hoạch.

Xem thêm [reality check](../analysis/reality-check.md) và [architecture blueprint](../architecture_blueprint.md).
