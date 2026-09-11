# Pentakuru

Ứng dụng Desktop thông minh dùng AI để **tổng hợp, quản lý file trên máy tính và ghi chú nhanh** phục vụ truy xuất tài liệu tức thì.

## Tính Năng Cốt Lõi
1. **Quét & Phân Tích Thư Mục**: Tự động bóc tách nội dung các tệp tin (PDF, DOCX, Code, TXT, Markdown, CSV) trên máy tính.
2. **Local AI Summary & Metadata**: Tóm tắt nhanh nội dung tệp tin, gắn thẻ và phân loại theo chủ đề.
3. **Local Embedding RAG**: Sử dụng mô hình nhẹ `sentence-transformers/all-MiniLM-L6-v2` chạy trực tiếp trên máy hoặc qua Core để vector hóa tài liệu.
4. **Tìm Kiếm Tức Thì (Semantic Search)**: Tìm kiếm tài liệu bằng ngôn ngữ tự nhiên (hỏi nội dung thay vì chỉ tìm theo tên file).
5. **Đồng Bộ Hệ Sinh Thái**: Sử dụng Unified API Key để đồng bộ tri thức lên `pentami-core` khi có kết nối mạng.

## Tech Stack Đề Xuất
- **Khung ứng dụng**: Tauri (Rust backend + Vite/React UI) để đạt dung lượng nhỏ (< 15MB) và tốc độ mở file cao nhất.
- **Local Vector DB**: LanceDB hoặc SQLite-VSS.
- **Tương tác**: Phím tắt toàn cục (Global Shortcut) để gọi nhanh thanh tìm kiếm tài liệu tương tự Spotlight / Raycast.
