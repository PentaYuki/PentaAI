# mcp-playwright

Module này hiện cung cấp `PentaPlaywrightController` tại `src/server.py`. Controller quản lý browser/page theo `session_id` và có các method async:

- `initialize()`
- `navigate(session_id, url)`
- `click(session_id, selector)`
- `fill(session_id, selector, text)`
- `extract_text(session_id, selector="body")`
- `screenshot(session_id, full_page=False)`
- `close_session(session_id)`

## Trạng thái triển khai

Đây là integration prototype/controller Python. Repository chưa có MCP SDK, transport stdio/SSE, process entrypoint, dependency manifest hoặc cấu hình allowlist URL. Vì vậy không khởi động module này như một MCP server bằng tài liệu hiện tại.

## An toàn trước khi tích hợp

Trước khi cho AI gọi controller, cần bổ sung allowlist URL, giới hạn timeout/kích thước dữ liệu, cô lập browser context, confirmation cho thao tác có side effect và audit log. Không đưa credential hoặc raw page content vào log.
