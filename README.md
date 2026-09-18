# Penta AI

> **Trạng thái:** prototype đang phát triển. Backend hiện chạy được ở mức API tối thiểu; các module domain, frontend integration, persistence, RAG và MCP vẫn chưa được nối vào runtime chính.

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
Client HTTP
  -> pentami-core/backend (FastAPI :8000)
       -> /api/health
       -> /api/ecosystem/apps
       -> /api/chat (echo)

Local infrastructure:
  PostgreSQL :5432 | Redis :6379 | Qdrant :6333/:6334
```

### Phạm vi hiện tại

| Thành phần | Trạng thái thực tế | Điểm bắt đầu |
| --- | --- | --- |
| `pentami-core/backend` | Backend FastAPI tối thiểu với health, app catalog và chat echo | `pentami-core/backend/main.py` |
| `shared` | Schema/protocol và helper dùng chung; chưa được API chính sử dụng | `shared/` |
| `deploy` | Compose cho PostgreSQL, Redis và Qdrant | `deploy/docker-compose.yml` |
| `pentami-core/frontend` | Có static assets/UI riêng, nhưng backend hiện chưa mount hoặc phục vụ thư mục này | `pentami-core/frontend/` |
| `mcp-playwright` | Controller Playwright Python; chưa có transport MCP/entrypoint server hoàn chỉnh | `mcp-playwright/src/server.py` |
| `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `pentanote` | Dataset/tài liệu và khung module; chưa có service độc lập được Compose khởi chạy | Các thư mục tương ứng |

`/api/chat` hiện chỉ nhận `query` và trả về chuỗi echo. Nó chưa phân loại intent, chưa gọi LLM, chưa truy vấn Qdrant, chưa lưu hội thoại vào PostgreSQL/Redis và chưa gọi service vệ tinh.

## Quick start

### Yêu cầu

- Python 3.10+ và `pip`
- Docker Desktop nếu cần chạy hạ tầng
- Không cần file `.env` cho backend prototype hiện tại. Các giá trị trong Compose chỉ dành cho local development.

Dependency tối thiểu nằm trong `pentami-core/backend/requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r pentami-core/backend/requirements.txt
```

Embedding vẫn cần các dependency ML riêng theo implementation và có thể tải model khi test lần đầu.

### Chạy backend

```bash
source .venv/bin/activate
./run_server.sh
```

Kiểm tra:

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/ecosystem/apps
curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"query":"tìm file báo cáo tháng 8"}'
```

Mở `http://127.0.0.1:8000/docs` để xem OpenAPI. Endpoint `/` chưa được backend phục vụ.

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
| `POST` | `/api/chat` | Echo nội dung `query` |
| `GET` | `/docs` | OpenAPI/Swagger |

Ví dụ request chat:

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"query":"học thuật toán"}'
```

Request chat hiện chỉ có trường bắt buộc `query`. Response là JSON đồng bộ; chưa phải SSE/WebSocket streaming.

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

- **Implemented:** FastAPI core tối thiểu, health endpoint, app catalog, chat echo và Docker Compose file.
- **Prepared:** frontend static, shared contracts, embedding/RAG helpers, memory, voice và API key helpers; chưa được nối vào API runtime.
- **Prototype:** `mcp-playwright` controller; chưa có MCP transport/entrypoint hoàn chỉnh.
- **Roadmap:** mount frontend, chat contract/routing, persistence, LLM integration, authentication middleware, streaming voice, RAG production và service độc lập.

## Roadmap

1. Pin version dependency và thêm test HTTP cho ba endpoint hiện tại.
2. Mount frontend hoặc ghi rõ lệnh serve frontend độc lập.
3. Chốt chat contract rồi mới thêm routing/response envelope.
4. Kết nối PostgreSQL, Redis và Qdrant với health probe và tenant filtering.
5. Hoàn thiện MCP transport, URL allowlist, confirmation và audit log.
6. Tách các domain thành service độc lập khi đã có API contract, entrypoint và test riêng.

## Tài liệu liên quan

- [Cấu trúc repository 6 ứng dụng](./docs/repository-architecture.md)
- [Người dùng cuối và phạm vi MCP](./docs/user-personas-and-mcp-scope.md)
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

## Status Update (18/09/2026)

Repository đã được rà soát lại. Các file trạng thái cũ ghi `100% completed` hoặc `production ready` không phản ánh code hiện tại; trạng thái chuẩn là prototype backend tối thiểu và roadmap chưa hoàn tất.
