# Kế hoạch Web Platform Penta AI

## Mục tiêu sản phẩm

Xây dựng một web workspace duy nhất, trong đó người dùng làm việc với nhiều phân hệ mà không phải đăng nhập, mở chat hoặc xây dựng lại ngữ cảnh nhiều lần.

## Nguyên tắc

- Một identity, một session, nhiều domain.
- Core điều phối; domain app sở hữu nghiệp vụ.
- Shared chỉ chứa contract, không chứa logic nghiệp vụ của từng app.
- Frontend shell thống nhất; mỗi app có workspace view riêng.
- Tính năng chưa có implementation phải được đánh dấu roadmap.

## Kiến trúc backend

### Tầng Gateway

- FastAPI gateway tại `pentami-core`.
- Authentication và tenant isolation.
- Request ID, session ID, trace ID.
- Rate limit và audit log.

### Tầng Orchestration

- Intent router.
- Context manager.
- Task planner.
- Action policy và confirmation.
- Response envelope thống nhất.

### Tầng Domain

- School service: course, lesson, quiz, learning progress.
- Kuru service: file index, extraction, local knowledge sync.
- Market service: catalog, pricing, voucher, order.
- Job service: profile, CV, matching, interview.
- Note service: pages, blocks, flashcards, mindmap.

### Tầng dữ liệu

- PostgreSQL: identity, tenant, nghiệp vụ và audit.
- Redis: session cache, rate limit, pub/sub, short-lived context.
- Qdrant: embeddings và semantic retrieval.
- Object storage: file, audio, image và exported documents.

## Kiến trúc frontend

### Unified shell

- Top bar: tenant, app hiện tại, trạng thái hệ thống.
- Left navigation: các workspace/module.
- Main workspace: view nghiệp vụ của app hiện tại.
- AI Kurumi launcher: chat chung ở góc phải.
- Command palette: điều hướng và hành động nhanh.

### Domain views

Mỗi app cung cấp một view độc lập nhưng tuân theo shell contract:

- route và metadata,
- quyền truy cập,
- resource context,
- loading/error/empty states,
- action events.

### Context bridge

Khi người dùng đang ở một resource, frontend gửi context tối thiểu:

```json
{
  "active_app": "pentanote",
  "active_resource": {"type": "page", "id": "page_123"},
  "selection": null
}
```

AI Kurumi dùng context đó để hiểu các câu hỏi như “tóm tắt cái này”, “đưa vào khóa học”, “so sánh với sản phẩm kia” mà không buộc người dùng lặp lại ID hay tên tài liệu.

## Lộ trình triển khai

### Giai đoạn 0: Foundation

- Chốt naming và app registry.
- Chuẩn hóa shared schemas.
- Thống nhất error, auth, tenant và action contracts.
- Đặt test baseline cho core.

### Giai đoạn 1: Unified shell + chat MVP

- Hoàn thiện launcher AI Kurumi.
- Kết nối chat API.
- Session persistence.
- Intent routing tới app registry.
- Deep-link tới app sau response.

### Giai đoạn 2: Context thật

- Tích hợp `MemoryContextManager` vào API.
- Redis session store.
- Context bridge từ từng domain view.
- Conversation history có tenant isolation.
- Test chuyển ngữ cảnh giữa hai app.

### Giai đoạn 3: Sản phẩm đầu tiên

Chọn `pentakuru` hoặc `pentanote` làm vertical slice:

```text
resource -> ingest -> index -> retrieve -> chat -> action
```

Không mở rộng năm domain cùng lúc trước khi vertical slice này chạy ổn định.

### Giai đoạn 4: Pentaschool

- course/lesson/quiz,
- learning progress,
- tutor grounded trên tài liệu,
- đề xuất nội dung dựa trên kết quả học.

### Giai đoạn 5: Market và Job

- Market trước hết ở catalog/pricing, sau đó mới order/payment.
- Job trước hết ở CV parsing/matching, sau đó mới mock interview và scoring.

### Giai đoạn 6: Voice và MCP

- Voice streaming sau khi text chat và context ổn định.
- MCP chỉ mở action có allowlist, confirmation, audit log và timeout.

## Tiêu chí hoàn thành web platform MVP

- Người dùng đăng nhập một lần.
- Có thể mở ít nhất hai module trong cùng shell.
- Chat dùng một `session_id` xuyên suốt.
- Chuyển từ Note sang School mà không mất context.
- Mọi response có target app và trạng thái rõ ràng.
- Dữ liệu tenant không bị trộn.
- Có test API, test routing và test giao diện launcher.
