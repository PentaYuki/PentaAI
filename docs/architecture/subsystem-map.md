# Bản đồ phân hệ

## 1. pentami-core

### Vai trò
Lõi điều phối trung tâm của ecosystem.

### Chức năng chính
- API gateway
- auth / key validation
- routing request
- context/memory orchestration
- RAG orchestration
- voice pipeline coordination
- automation dispatch

### Thư mục chính
- `pentami-core/backend/`
- `pentami-core/config/`
- `pentami-core/memory/`
- `pentami-core/rag/`
- `pentami-core/voice/`
- `pentami-core/auth/`

## 2. shared

### Vai trò
Hợp đồng dữ liệu dùng chung.

### Chức năng chính
- `UnifiedApiKeyRecord`
- `PentaChunk`
- `ChunkEmo`, `ChunkTime`, `ChunkAction`
- `VoiceConfig`

### Giá trị
Giảm xung đột giữa các module và thúc đẩy contract-first architecture.

## 3. pentaschool

### Vai trò
Ứng dụng giáo dục và AI tutor.

### Chức năng chính
- học liệu, bài giảng, tiến độ học,
- avatar AI,
- tương tác theo ngữ cảnh,
- cá nhân hóa lộ trình học.

## 4. pentakuru

### Vai trò
Quản lý tài liệu cục bộ và tri thức cá nhân.

### Chức năng chính
- index tài liệu
- OCR / extraction
- local RAG
- tự động gắn metadata

## 5. pentamarket

### Vai trò
Thương mại điện tử + tư vấn AI.

### Chức năng chính
- catalog sản phẩm
- tư vấn AI bán hàng
- Voucher / pricing / tax
- giỏ hàng / order flow

## 6. pentajob

### Vai trò
Tuyển dụng và tìm kiếm việc làm thông minh.

### Chức năng chính
- hồ sơ ứng viên
- match CV / JD
- mock interview
- hỗ trợ nghề nghiệp

## 7. pentanote

### Vai trò
Không gian ghi chú và tri thức nền tảng.

### Chức năng chính
- block-based workspace
- note management
- flashcards
- summary / mindmap / graph knowledge

## 8. mcp-playwright

### Vai trò
Automation browser cho AI agent.

### Chức năng chính
- điều hướng web
- click / fill form
- screenshot
- crawl / extract text

## 9. deploy

### Vai trò
Triển khai hạ tầng cho môi trường phát triển và vận hành.

### Chức năng chính
- PostgreSQL
- Redis
- Qdrant
- docker compose
