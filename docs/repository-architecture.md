# Repository Architecture

## Mục tiêu

Penta AI được tổ chức thành một monorepo gồm **6 ứng dụng nghiệp vụ** và một platform layer dùng chung. Cách này giúp phát triển cùng một repository, nhưng vẫn giữ ranh giới rõ để sau này tách thành nhiều repository hoặc service độc lập.

## Sáu ứng dụng chính

| Ứng dụng | Trách nhiệm | Branch nền |
| --- | --- | --- |
| `pentami-core` | Gateway, orchestration, intent routing, session và frontend workspace | `work/pentami-core` |
| `pentaschool` | LMS, bài học, bài tập và AI tutor | `work/pentaschool` |
| `pentakuru` | File assistant, indexing và truy vấn tài liệu | `work/pentakuru` |
| `pentamarket` | Sản phẩm, giá, voucher, VAT và đơn hàng | `work/pentamarket` |
| `pentajob` | CV, job matching và mock interview | `work/pentajob` |
| `pentanote` | Notes, flashcards, mindmap và knowledge workspace | `work/pentanote` |

## Platform layer

Đây không phải ứng dụng nghiệp vụ thứ bảy:

| Thành phần | Vai trò |
| --- | --- |
| `shared/` | Schema, API contract, event/chunk protocol và type dùng chung |
| `deploy/` | PostgreSQL, Redis, Qdrant, migration và local environment |
| `mcp-playwright/` | Browser automation adapter dùng bởi core, school, market, job và note; không dùng cho `pentakuru` |
| `docs/` | Architecture, API contract, roadmap và runbook |
| `scripts/` | Tooling, seed và đồng bộ dữ liệu; không chứa business API |

## Cấu trúc đích của mỗi ứng dụng

Khi một app bắt đầu có backend/frontend riêng, chuẩn hóa về cấu trúc sau:

```text
<app>/
├── backend/                 # API và domain logic của app
│   ├── api/                 # HTTP/WebSocket routes
│   ├── domain/              # entity, use case, business rules
│   ├── infrastructure/     # DB, cache, external adapters
│   └── main.py              # entrypoint của app
├── frontend/                # UI riêng của app, nếu có
│   ├── src/
│   └── README.md
├── contracts/               # request/response/event của app
├── tests/                   # unit và integration tests của app
├── docs/                    # API và quyết định kiến trúc của app
├── datasets/                # dữ liệu mẫu, không chứa secret hoặc PII
├── pyproject.toml           # dependency riêng, khi app có runtime riêng
└── README.md
```

Hiện tại nhiều app mới ở mức dataset/documentation. Không tạo thư mục giả chỉ để làm đẹp; chỉ thêm `backend`, `frontend` hoặc `contracts` khi capability đó thật sự bắt đầu được triển khai.

## Ranh giới phụ thuộc

```text
App frontend/backend
        |
        v
  shared contracts  --->  platform adapters
                              |-- PostgreSQL
                              |-- Redis
                              |-- Qdrant
                              |-- MCP Playwright
```

Quy tắc bắt buộc:

1. App chỉ import contract/helper ổn định từ `shared`; không import mã nguồn nội bộ của app khác.
2. App giao tiếp với `pentami-core` qua HTTP, event hoặc contract; không gọi trực tiếp function nội bộ của core.
3. `shared` không import ngược vào app và không chứa business rule riêng của một app.
4. `deploy` chỉ cung cấp hạ tầng; không đặt logic nghiệp vụ vào Docker Compose hoặc migration chung.
5. `mcp-playwright` chỉ nhận action contract được cấp quyền từ `pentami-core`; chỉ phục vụ workflow web của `pentami-core`, `pentaschool`, `pentamarket`, `pentajob` và `pentanote`.
6. `pentakuru` không được gọi Playwright. File/local automation phải đi qua permission boundary và API local riêng.
7. Mỗi app sở hữu dữ liệu nghiệp vụ của mình. Dùng `tenant_id` trong contract, nhưng chỉ tuyên bố isolation sau khi query layer có filter và test.

## Phân lớp dữ liệu

- **App data:** bảng nghiệp vụ thuộc app sở hữu, ví dụ course, product, job, note.
- **Core data:** identity, session, routing và audit.
- **Shared contract:** chỉ schema/event; không phải database dùng chung cho mọi app.
- **Knowledge data:** vector/document index có `tenant_id`, `source_app`, `document_id` và version.
- **Infrastructure data:** volume PostgreSQL/Redis/Qdrant trong `deploy`; không commit dữ liệu runtime.

## Cách phát triển theo giai đoạn

### Giai đoạn 1: Monorepo modular

- Tất cả app nằm trong repository này.
- Mỗi app có `work/<app>` và feature branch riêng.
- PR nhỏ đi vào `work/<app>`; mốc tích hợp đi vào `main`.
- CI chạy toàn repo ở hiện tại.

### Giai đoạn 2: App có thể chạy độc lập

Một app chỉ được coi là độc lập khi có:

- entrypoint riêng;
- dependency manifest riêng;
- config/environment riêng;
- health endpoint;
- test riêng;
- Dockerfile hoặc lệnh chạy rõ;
- API contract versioned.

### Giai đoạn 3: Tách repository khi cần

Chỉ tách app thành repository riêng khi có ít nhất một lý do thực tế: cadence release khác hẳn, team sở hữu riêng, pipeline/deployment riêng hoặc kích thước monorepo gây chậm. Trước khi tách, giữ `shared` thành package versioned thay vì copy code.

## Release theo ứng dụng

Trong monorepo, dùng tag có scope để biết app nào thay đổi:

```text
pentami-core/v0.2.0
pentaschool/v0.1.0
pentakuru/v0.1.0
pentamarket/v0.1.0
pentajob/v0.1.0
pentanote/v0.1.0
```

Nếu GitHub Release workflow hiện chỉ hỗ trợ tag `v*.*.*`, cần mở rộng workflow trước khi dùng tag scoped. Cho tới lúc đó, release chung dùng `v0.x.y` và CHANGELOG phải ghi rõ app bị ảnh hưởng.

## Kiểm soát thay đổi

- Thay đổi một app: sửa trong branch app và chỉ chạy/test scope đó khi đã có pipeline hỗ trợ.
- Thay đổi `shared`: yêu cầu test contract và kiểm tra các app phụ thuộc.
- Thay đổi `deploy`: yêu cầu `docker compose config`, migration check và ghi chú backward compatibility.
- Thay đổi `pentami-core`: kiểm tra API contract vì đây là điểm vào chung của hệ sinh thái.
- Breaking change phải tăng version contract hoặc ghi rõ migration trong CHANGELOG.
