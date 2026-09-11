# Penta AI

Hệ sinh thái AI đa module với `pentami-core` làm lõi điều phối, frontend desktop tĩnh, các contract dùng chung và hạ tầng local cho RAG/ứng dụng tương lai.

> **Trạng thái:** đang phát triển. README này mô tả đúng phần đã chạy được; các capability chưa có integration được ghi rõ trong roadmap.

## Nội dung

- [Tổng quan](#tổng-quan)
- [Quick start](#quick-start)
- [API hiện tại](#api-hiện-tại)
- [Cấu trúc repository](#cấu-trúc-repository)
- [Trạng thái module](#trạng-thái-module)
- [Roadmap](#roadmap)
- [Development & Release](#development--release)

## Tổng quan

```text
Browser
  -> pentami-core/backend (FastAPI :8000)
       -> frontend desktop tĩnh
       -> /api/health
       -> /api/ecosystem/apps
       -> /api/chat

Local infrastructure:
  PostgreSQL :5432 | Redis :6379 | Qdrant :6333/:6334
```

### Phạm vi hiện tại

| Thành phần | Trạng thái thực tế | Điểm bắt đầu |
| --- | --- | --- |
| `pentami-core/backend` | Backend FastAPI chạy được; định tuyến từ khóa, persona, response action và frontend tĩnh | `pentami-core/backend/main.py` |
| `shared` | Schema, protocol chunk và quản lý API key dùng chung | `shared/` |
| `deploy` | Compose cho PostgreSQL, Redis và Qdrant | `deploy/docker-compose.yml` |
| `pentami-core/frontend` | Giao diện tĩnh được FastAPI mount tại `/static` và `/` | `pentami-core/frontend/` |
| `mcp-playwright` | Controller Playwright Python; chưa có transport MCP/entrypoint server hoàn chỉnh | `mcp-playwright/src/server.py` |
| `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `pentanote` | Dataset/tài liệu và khung module; chưa có service độc lập được Compose khởi chạy | Các thư mục tương ứng |

`/api/chat` hiện phân loại intent bằng từ khóa tiếng Việt/tiếng Anh trong process. Nó chưa gọi LLM, chưa truy vấn Qdrant, chưa lưu hội thoại vào PostgreSQL/Redis và chưa gọi service vệ tinh.

## Quick start

### Yêu cầu

- Python 3.10+ và `pip`
- Docker Desktop nếu cần chạy hạ tầng
- Không commit `deploy/.env`; dùng `deploy/.env.example` làm mẫu

Backend hiện chưa có `requirements.txt` hoặc `pyproject.toml`. Cài tối thiểu để chạy local:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install fastapi uvicorn pydantic
```

Để chạy test embedding, cần cài thêm dependency mà `pentami-core/rag/embedding.py` sử dụng, sau đó cài `pytest`. Danh sách dependency chính thức nên được bổ sung trước khi đóng gói production.

### Chạy backend và frontend

```bash
source .venv/bin/activate
python pentami-core/backend/main.py
```

Kiểm tra:

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/ecosystem/apps
curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"query":"tìm file báo cáo tháng 8","persona":"serious"}'
```

Mở `http://127.0.0.1:8000/` để xem frontend và `http://127.0.0.1:8000/docs` để xem OpenAPI.

### Chạy hạ tầng tùy chọn

```bash
docker compose -f deploy/docker-compose.yml up -d
docker compose -f deploy/docker-compose.yml ps
```

Compose chỉ khởi chạy PostgreSQL, Redis và Qdrant. Backend hiện không tự kết nối các service này trong flow `/api/chat`; hãy xem chúng là hạ tầng chuẩn bị cho các bước tích hợp tiếp theo. Mật khẩu trong file Compose là giá trị phát triển, không dùng ở production.

### Kiểm thử

```bash
python3 -m pytest pentami-core/tests/test_core_components.py -q
```

Lệnh trên yêu cầu `pytest` và các dependency của embedding. Nếu môi trường chưa cài dependency, đó là lỗi thiết lập môi trường, không phải bằng chứng backend đã chạy đầy đủ.

## API hiện tại

| Method | Endpoint | Mục đích |
| --- | --- | --- |
| `GET` | `/api/health` | Trạng thái hiển thị của core |
| `GET` | `/api/ecosystem/apps` | Catalog ứng dụng |
| `POST` | `/api/chat` | Keyword intent routing và response action |
| `GET` | `/docs` | OpenAPI/Swagger |

Ví dụ request chat:

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"query":"học thuật toán","persona":"serious"}'
```

`persona` hiện hỗ trợ `cute`, `serious`, `yandere`. Response chat là JSON đồng bộ; chưa phải SSE/WebSocket streaming.

## Cấu trúc repository

```text
pentami-core/       Core FastAPI và frontend desktop
shared/             Schema, chunk protocol và helper dùng chung
deploy/             Docker Compose cho PostgreSQL, Redis, Qdrant
mcp-playwright/     Browser controller prototype
pentaschool/        Dataset/tài liệu module giáo dục
pentakuru/          Dataset/tài liệu module file assistant
pentamarket/        Dataset/tài liệu module thương mại
pentajob/           Dataset/tài liệu module tuyển dụng
pentanote/          Dataset/tài liệu module ghi chú
docs/               Kiến trúc, roadmap và reality check
```

## Trạng thái module

- **Implemented:** FastAPI core, static frontend, API catalog/chat, shared contracts, Docker Compose infrastructure.
- **Prepared:** embedding/RAG helpers, memory, voice và API key helpers.
- **Prototype:** `mcp-playwright` controller; chưa có MCP transport/entrypoint hoàn chỉnh.
- **Roadmap:** service độc lập cho các app vệ tinh, persistence, LLM integration, authentication middleware, streaming voice và RAG production.

## Roadmap

1. Thêm `pyproject.toml` hoặc `requirements.txt` có version pin và CI.
2. Tách cấu hình/secret khỏi code và thêm health probe thật cho dependency.
3. Kết nối PostgreSQL, Redis và Qdrant vào backend với tenant filtering.
4. Thay keyword router bằng intent contract có test tiếng Việt có dấu/không dấu.
5. Hoàn thiện MCP transport, URL allowlist, confirmation và audit log.
6. Tách các domain thành service độc lập khi đã có API contract và test riêng.

## Tài liệu liên quan

- [Cấu trúc repository 6 ứng dụng](./docs/repository-architecture.md)
- [Quy tắc phát triển](./GEMINI.md)
- [Kiến trúc thực tế và kế hoạch triển khai](./ARCHITECTURE.md)
- [Reality check](./docs/analysis/reality-check.md)
- [Hướng dẫn riêng của pentami-core](./pentami-core/README.md)
- [Kế hoạch GitHub và release](./docs/github-release-plan.md)

## Development & Release

Repository dùng GitHub Actions để kiểm tra Python syntax, frontend JavaScript và Docker Compose trên mỗi push/PR vào `main`.

Quy trình đóng góp:

1. Tạo branch `feature/...`, `fix/...` hoặc `docs/...`.
2. Mở pull request và điền checklist.
3. Chờ CI xanh và maintainer review.
4. Squash merge vào `main`.

Release dùng Semantic Versioning. Sau khi merge và cập nhật [CHANGELOG.md](./CHANGELOG.md), tạo tag:

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

GitHub Actions sẽ tự tạo GitHub Release từ tag `v*.*.*`. Chi tiết xem [docs/github-release-plan.md](./docs/github-release-plan.md).
