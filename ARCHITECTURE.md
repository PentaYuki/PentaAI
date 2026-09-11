# Kiến trúc Penta AI: hiện trạng và kế hoạch triển khai

## 1. Phạm vi tài liệu

Tài liệu này mô tả những gì có thể xác minh từ repository tại thời điểm hiện tại. Đây là kiến trúc triển khai local, chưa phải sơ đồ production.

Mô hình tổ chức repository chi tiết nằm ở [docs/repository-architecture.md](./docs/repository-architecture.md): sáu ứng dụng nghiệp vụ độc lập về ranh giới, cùng platform layer dùng chung.

## 2. Thành phần đã có

```text
                         +----------------------+
                         | Browser               |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | pentami-core/backend  |
                         | FastAPI :8000         |
                         +--+---------+----------+
                            |         |
                  /         |         \  /
           /api/health  /api/chat   frontend tĩnh
                            |
                            v
                    keyword intent routing

     Infrastructure prepared by Compose, not yet used by /api/chat:
     PostgreSQL :5432 | Redis :6379 | Qdrant :6333/:6334
```

### `pentami-core/backend`

Entrypoint là `pentami-core/backend/main.py`. Backend hiện:

- khởi tạo FastAPI và CORS;
- phục vụ frontend tại `/` và `/static` nếu thư mục frontend tồn tại;
- cung cấp `GET /api/health`;
- cung cấp catalog tĩnh ở `GET /api/ecosystem/apps`;
- phân loại `POST /api/chat` bằng danh sách từ khóa và trả về response đồng bộ;
- tạo action `navigate_app` trong response chat.

Backend chưa có persistence, queue, LLM call, Qdrant query, Redis client, database session, authentication middleware hoặc voice pipeline trong flow này.

### `pentami-core/frontend`

Frontend là static app dùng native ES modules, được backend phục vụ từ `frontend/`. Ranh giới hiện tại:

```text
js/app.js                  -> bootstrap và wiring
js/core/                   -> state + DOM registry
js/config/                 -> catalog/config tĩnh
js/services/               -> HTTP/API clients
js/features/               -> chat, desktop, store
js/ui/                     -> component UI dùng chung như toast
```

`app.js` không chứa business logic của từng feature. Feature giao tiếp qua state dùng chung, callback và service API; khi thêm module mới nên tạo thư mục trong `features/`, đăng ký ở `app.js`, và không import trực tiếp code của feature khác.

### `shared`

`shared/` chứa các contract Python dùng chung, gồm schema dữ liệu, chunk protocol và API key manager. Đây là thư viện contract/helper, không phải service chạy độc lập.

### `deploy`

`deploy/docker-compose.yml` định nghĩa ba dependency local:

| Service | Port | Mục đích dự kiến | Trạng thái tích hợp |
| --- | ---: | --- | --- |
| PostgreSQL 16 Alpine | 5432 | relational data | container có sẵn, backend chưa kết nối |
| Redis 7.2 Alpine | 6379 | cache/rate limit/pub-sub | container có sẵn, backend chưa kết nối |
| Qdrant latest | 6333/6334 | vector search | container có sẵn, backend chưa kết nối |

Tag `latest` của Qdrant nên được pin theo version trước khi triển khai production. Password trong Compose chỉ là development default.

### `mcp-playwright`

`mcp-playwright/src/server.py` cung cấp `PentaPlaywrightController` với các thao tác navigate, click, fill, extract text và screenshot. File này chưa expose MCP transport, chưa có process entrypoint và chưa được backend gọi tự động. Vì vậy chỉ ghi nhận là controller/integration prototype.

## 3. Contract API hiện tại

### `GET /api/health`

Trả về trạng thái hiển thị của core. Các giá trị service như `redis_cache` và `qdrant_rag` hiện là trạng thái cấu hình trong response, không phải health probe kết nối thật; không dùng endpoint này làm bằng chứng các dependency đang hoạt động.

### `POST /api/chat`

Request tối thiểu:

```json
{
  "query": "tìm file báo cáo tháng 8"
}
```

Các trường tùy chọn là `session_id`, `persona` (`cute`, `serious`, `yandere`) và `tenant_id`. Router hiện dùng keyword matching; các intent chính là `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `pentanote`, `mcp_playwright` và fallback `pentami_core`.

Response gồm `session_id`, `query`, `target_app`, `persona`, `reply_text`, `emotion`, `action` và `timestamp`. Đây là response JSON đồng bộ, chưa phải SSE/WebSocket hay `PentaStreamEnvelope` streaming.

## 4. Cách triển khai local

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install fastapi uvicorn pydantic
python pentami-core/backend/main.py
```

Ở terminal khác:

```bash
curl http://127.0.0.1:8000/api/health
curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"query":"học thuật toán","persona":"serious"}'
```

Khởi động dependency local khi cần:

```bash
docker compose -f deploy/docker-compose.yml up -d
docker compose -f deploy/docker-compose.yml ps
```

## 5. Khoảng trống trước production

1. Thêm `pyproject.toml` hoặc `requirements.txt` có version pin, cùng Dockerfile cho backend.
2. Tách cấu hình khỏi mã nguồn và thay password development bằng secret manager.
3. Viết health probe thật cho PostgreSQL, Redis và Qdrant.
4. Thay keyword router bằng intent contract có test tiếng Việt có dấu/không dấu.
5. Kết nối persistence và RAG với filter tenant ở query layer, kèm integration tests.
6. Thêm authentication middleware thật; hiện API key manager trong `shared` chưa có nghĩa là endpoint đã được bảo vệ.
7. Hoàn thiện MCP transport, allowlist URL, confirmation, timeout và audit log cho Playwright.
8. Chỉ sau các bước trên mới đánh giá benchmark latency, streaming voice và triển khai production.

## 6. Tài liệu nguồn

- [Runbook repository](./README.md)
- [Cấu trúc repository 6 ứng dụng](./docs/repository-architecture.md)
- [Reality check](./docs/analysis/reality-check.md)
- [Backend README](./pentami-core/README.md)
