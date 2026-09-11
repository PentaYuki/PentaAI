# Penta AI Development Rules

Tài liệu này là quy tắc làm việc cho code hiện tại. Không mô tả một tính năng là "đã sẵn sàng" nếu chưa có implementation, test hoặc lệnh khởi chạy kiểm chứng được.

## 1. Nguồn sự thật

- Trạng thái code: thư mục và entrypoint thực tế trong repository.
- Hợp đồng dùng chung: `shared/`.
- Hạ tầng local: `deploy/docker-compose.yml` và `deploy/.env.example`.
- Tài liệu kiến trúc: `ARCHITECTURE.md` và `docs/analysis/reality-check.md`.
- Khi tài liệu mâu thuẫn với code, ưu tiên code rồi cập nhật tài liệu trong cùng thay đổi.

## 2. Phân lớp module

- `pentami-core/backend`: API và orchestration trung tâm.
- `pentami-core/frontend`: frontend tĩnh được backend phục vụ.
- `shared`: schema, protocol và helper dùng chung; không chứa logic nghiệp vụ của app.
- `deploy`: PostgreSQL, Redis và Qdrant cho local development.
- Các thư mục `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `pentanote`: hiện là module/dataset/tài liệu; chỉ gọi là service khi có entrypoint, dependency, health check và test riêng.
- `mcp-playwright`: hiện là controller Python. Không gọi là MCP server hoàn chỉnh cho tới khi có MCP transport và entrypoint được kiểm thử.

Không import mã nguồn nội bộ giữa các app vệ tinh. Khi cần liên kết, dùng contract trong `shared/` hoặc API/event contract đã được ghi rõ. Việc tách module không tự động có nghĩa là hệ thống đã là microservices.

## 3. API hiện tại

Backend chạy từ `pentami-core/backend/main.py` với các endpoint:

- `GET /api/health`: health response của core.
- `GET /api/ecosystem/apps`: catalog app tĩnh.
- `POST /api/chat`: nhận `query`, `session_id`, `persona`, `tenant_id`; phân loại bằng từ khóa và trả về `target_app`, `reply_text`, `emotion`, `action`.
- `GET /docs`: OpenAPI do FastAPI sinh.

`/api/chat` hiện không gọi LLM, database, Redis, Qdrant, STT/TTS hoặc service vệ tinh. Không viết tài liệu hoặc test dựa trên hành vi chưa có trong endpoint.

## 4. Dữ liệu và bảo mật

- Không commit secret thật. `deploy/.env` chỉ dành cho local; dùng `.env.example` khi chia sẻ cấu hình.
- API key phải được xử lý qua `shared/auth/key_manager.py`; không log raw key và không lưu plaintext.
- Schema chung phải đặt trong `shared/` trước khi dùng giữa module.
- `tenant_id` là trường hợp đồng dữ liệu; chỉ khẳng định isolation khi query layer thực sự áp dụng filter và có test.
- Các thao tác gây tác động bên ngoài như thanh toán, xóa dữ liệu, gửi hồ sơ hoặc browser automation cần confirmation và audit log trước khi bật production.
- Không dùng các số đo như `<1ms`, `<500ms` hoặc "zero latency" nếu chưa có benchmark, môi trường đo và ngưỡng kiểm thử được ghi lại.

## 5. Quy trình thay đổi

1. Tìm entrypoint và test gần nhất với hành vi cần sửa.
2. Sửa contract hoặc implementation nhỏ nhất có thể.
3. Thêm/cập nhật test cho hành vi mới.
4. Chạy kiểm tra phù hợp: `pytest`, import/compile check, `docker compose config --quiet` hoặc smoke test HTTP.
5. Cập nhật README/architecture nếu lệnh chạy, endpoint, trạng thái module hoặc schema thay đổi.

## 6. Roadmap phải tách khỏi hiện trạng

Các mục sau là hướng phát triển, chưa phải capability hiện tại:

- Kết nối thật tới PostgreSQL, Redis và Qdrant.
- Intent router dùng model/normalizer thay cho từ khóa.
- SSE/WebSocket streaming và voice STT/TTS.
- MCP transport hoàn chỉnh cho Playwright.
- Service độc lập cho các app vệ tinh.
- Dependency manifest và container image cho backend.

Mọi PR triển khai một mục roadmap phải bổ sung entrypoint, cấu hình, health check, test và hướng dẫn chạy tương ứng.
