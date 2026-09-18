# Penta Core Desktop Frontend & Pentastore Hub

Giao diện Desktop Workspace và Cửa Hàng Hệ Sinh Thái (**Pentastore**) cho lõi điều phối `pentami-core`.

---

## 🏛️ Cấu Trúc Thư Mục Frontend

```text
pentami-core/frontend/
├── assets/                   # Logo và hình ảnh giao diện
├── css/style.css             # Style dùng chung
├── js/
│   ├── app.js                # Entry point, chỉ khởi tạo và nối module
│   ├── config/catalog.js     # Catalog app, không chứa logic UI
│   ├── core/
│   │   ├── dom.js            # DOM registry
│   │   └── state.js          # State phiên và trạng thái desktop
│   ├── features/
│   │   ├── chat.js           # Chat và session với Penta Core
│   │   ├── desktop.js        # Màn hình app đã cài
│   │   └── store.js          # Pentastore install/uninstall
│   ├── services/core-api.js  # HTTP client tới backend
│   └── ui/toast.js           # Thành phần UI dùng chung
├── index.html                # Shell giao diện desktop
└── README.md
```

Frontend dùng native ES modules (`type="module"`), không cần bundler ở giai đoạn hiện tại. Mỗi feature nhận dependency qua function parameter/callback; tránh import trực tiếp lẫn nhau giữa các domain.

---

## 🚀 Tính Năng Chính

1. **Giao Diện Desktop OS Hiện Đại (Modern Web Architecture)**:
   - Thanh trạng thái Top Menubar hiển thị đồng hồ thời gian thực, trạng thái IAM Key, bộ chuyển đổi 3 nhân cách (**Cute, Serious, Yandere**).
   - Lưới ứng dụng Desktop dạng Mono Badges có chấm trạng thái trực tuyến.
   - Nút nổi **AI Kurumi** ở góc phải: mở một cuộc trò chuyện chung và gọi `POST /api/chat` để định tuyến tới các phân hệ.
2. **Floating Glassmorphism Dock (Mac/Android Hybrid)**:
   - Phím mở **Pentastore** với logo ngũ giác nổi bật, hiệu ứng phóng to icon khi rê chuột.
   - Các phím tắt mở nhanh các phân hệ: `pentanote`, `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `mcp_playwright`.
3. **Pentastore (Hệ Sinh Thái Penta AI)**:
   - Danh mục đầy đủ toàn bộ các phân hệ hiện tại và tương lai:
     * `pentaschool` (LMS & AI Virtual Instructor)
     * `pentanote` (100% Notion-like AI Workspace)
     * `pentakuru` (Local File Assistant & Knowledge Indexer)
     * `pentamarket` (E-Commerce & Financial VAT Engine)
     * `pentajob` (AI Talent & Voice Mock Interview)
     * `mcp_playwright` (Web Automation Engine)
     * `antigravity` (Agentic OS)
     * `pentamo`, `pentaana`, `pentabi`, `pentaiot`, `pentaali`, `stockai`, `khafood`, `kyniem`, `salto`.
   - Tìm kiếm ứng dụng theo thời gian thực và lọc theo danh mục.
   - Xem chi tiết phân hệ trên cửa sổ giao diện tương tác và cài đặt ứng dụng ra Desktop.

4. **Unified context**:
   - Frontend giữ một `session_id` trong phiên trình duyệt.
   - UI hiện chuẩn bị gửi `session_id`, `persona` và `tenant_id`, nhưng backend prototype chưa nhận các trường này.
   - Frontend chưa được `pentami-core/backend/main.py` mount hoặc phục vụ.
   - Context bridge đầy đủ giữa các domain được mô tả tại [`docs/architecture/unified-workspace.md`](../../docs/architecture/unified-workspace.md).

---

## 💻 Cách Khởi Chạy

### Cách 1: Chạy cùng FastAPI Backend (khuyến nghị)
```bash
python3 pentami-core/backend/main.py
```
Truy cập: `http://localhost:8000`

### Cách 2: Static server riêng

Không nên mở trực tiếp bằng `file://` vì ES modules có thể bị trình duyệt chặn bởi CORS. Dùng static server:

```bash
python3 -m http.server 8080 --directory pentami-core/frontend
```

Truy cập: `http://localhost:8080`. Chat API cần backend chạy riêng và cấu hình proxy/API base URL trước khi dùng.
