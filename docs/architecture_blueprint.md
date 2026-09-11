# Architecture Blueprint

Tài liệu kiến trúc chuẩn hiện được tách theo mục đích:

- [README repository](../README.md): cài đặt và chạy local.
- [ARCHITECTURE.md](../ARCHITECTURE.md): hiện trạng code, API, dependency và khoảng trống trước production.
- [GEMINI.md](../GEMINI.md): quy tắc phát triển và tiêu chí ghi nhận capability.
- [Reality check](./analysis/reality-check.md): các điểm cần phân biệt giữa vision và implementation.

## Quy ước cập nhật

Mỗi capability mới chỉ được đưa vào phần "đã có" sau khi có đủ:

1. entrypoint hoặc API rõ ràng;
2. cấu hình/dependency có thể cài;
3. health check hoặc smoke test;
4. test cho contract chính;
5. lệnh chạy được ghi trong README.

Các sơ đồ, voice pipeline, RAG integration, unified authentication, service vệ tinh và MCP transport chưa đáp ứng đủ điều kiện trên phải nằm trong roadmap hoặc implementation note riêng, không ghi là production-ready.
