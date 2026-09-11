# Tổng quan hệ thống

## 1. Kiến trúc logic

Dự án Penta AI đang triển khai theo mô hình “AI ecosystem core + domain modules”:

- `pentami-core` là bộ não trung tâm.
- `shared` là tầng hợp đồng và model chuẩn.
- `pentaschool`, `pentakuru`, ... là các ứng dụng chuyên biệt sử dụng core để xử lý trí tuệ và dữ liệu.

## 2. Các lớp chính

### 2.1. Client layer
- web browser,
- desktop UI,
- internal service callers,
- AI agents.

### 2.2. API / orchestration layer
`pentami-core/backend/main.py` hiện là entry point chính của backend. Ở đây có:

- cấu hình FastAPI,
- CORS,
- khai báo ecosystem catalog,
- routing / API exposure,
- import shared component and protocol models.

### 2.3. Service layer
Các service được tổ chức theo chức năng:

- `auth`: xác thực API key, scope, RBAC-like logic,
- `rag`: embedding và truy vấn vector,
- `memory`: ngữ cảnh và bộ nhớ hội thoại,
- `voice`: STT và TTS,
- `config`: prompt và persona,
- `dataset`: dữ liệu mẫu và intent.

### 2.4. Shared contracts layer
Tầng này rất quan trọng vì nó định nghĩa:

- model dữ liệu cho API key,
- chunk format và protocol,
- enum hệ thống,
- dữ liệu metadata của RAG.

### 2.5. Infra layer
- Redis: cache và rate limiting,
- PostgreSQL: dữ liệu nghiệp vụ,
- Qdrant: vector store,
- Docker Compose: triển khai cơ sở hạ tầng.

## 3. Luồng dữ liệu điển hình

```text
User request
    -> Client / Web / Desktop
    -> pentami-core API
    -> auth verification
    -> intent routing / task classification
    -> service call (RAG / Memory / Voice / MCP)
    -> response packaging
    -> frontend render / action trigger
```

## 4. Các ràng buộc kỹ thuật cần tuân thủ

- Không triển khai dữ liệu “marketing” mà không có module thật tương ứng.
- Mỗi subsystem cần có module gốc, không chỉ README dài.
- Sử dụng shared models để tiêu chuẩn hóa input/output.
- Tất cả action/automation nên đi qua các protocol rõ ràng thay vì hardcode.

## 5. Nhiệm vụ tiếp theo

- chuẩn hoá tên folder,
- bổ sung docs cho từng module,
- xác định phạm vi api thực sự,
- tách phần conceptual vs implementation.
