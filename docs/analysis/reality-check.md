# Reality check kiến trúc Penta AI

## 1. Kết luận ngắn gọn

Dự án có nhiều tài liệu mô tả rất “đẹp” về hệ sinh thái AI, nhưng cần phân biệt giữa:

- mô tả chiến lược/marketing,
- kiến trúc kỹ thuật thực tế hiện có,
- và các module chưa được triển khai đầy đủ.

## 2. Những điểm thực tế hiện có

### Có thật
- `pentami-core/backend/main.py` là FastAPI entrypoint tối thiểu.
- API hiện có health, app catalog và chat echo.
- `shared` chứa schema/protocol/helper, nhưng chưa được API chính gọi trong runtime.
- `deploy/docker-compose.yml` định nghĩa PostgreSQL, Redis và Qdrant cho local development.
- `mcp-playwright` có controller Python; chưa chứng minh được MCP transport/server hoàn chỉnh.

### Chưa có trong runtime chính
- Frontend chưa được FastAPI mount.
- Chat chưa có keyword/model routing, persona, response action, session hoặc tenant handling.
- Backend chưa kết nối PostgreSQL, Redis, Qdrant, LLM, RAG, memory, voice hay service domain.
- Các app vệ tinh chủ yếu là dataset/tài liệu, chưa có service độc lập trong Compose.

## 3. Khuyến nghị

### A. Tách rõ cấp độ
1. `Vision`: mô tả hướng đi chiến lược.
2. `Architecture`: mô tả hệ thống logic và flows.
3. `Implementation`: chỉ liệt kê phần code thật có.
4. `Roadmap`: phần chưa triển khai hoặc dự kiến.

### B. Thiết lập quy tắc tài liệu
- mỗi module phải có README xác định scope,
- mỗi api phải có contract,
- mỗi dữ liệu quan trọng phải có model trong `shared`.

### C. Rà soát naming
- chuẩn hóa tên hệ thống: `pentami-core`, `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `pentanote`.
- tránh dùng tên khác nhau như `PentaKurumi`, `pentamo`, `PentaMo`, `Pentakai` không thống nhất.

## 4. Kết quả cần đạt

Sau khi chuẩn hóa:

- tài liệu sẽ đúng với trạng thái hiện tại,
- mọi người dễ hiểu đâu là core, đâu là app phụ,
- kế hoạch phát triển rõ hơn, ít rủi ro nhầm lẫn trong triển khai.

## 5. Mục tiêu cuối cùng

Dự án nên hoạt động theo mô hình rõ ràng hơn:

- `core` triển khai logic nền tảng,
- `apps` triển khai chức năng chuyên biệt,
- `shared` làm nền tảng giao tiếp,
- `deploy` quản lý môi trường,
- `docs` là tài liệu chính xác nhất.
