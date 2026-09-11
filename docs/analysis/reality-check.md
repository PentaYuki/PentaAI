# Reality check kiến trúc Penta AI

## 1. Kết luận ngắn gọn

Dự án có nhiều tài liệu mô tả rất “đẹp” về hệ sinh thái AI, nhưng cần phân biệt giữa:

- mô tả chiến lược/marketing,
- kiến trúc kỹ thuật thực tế hiện có,
- và các module chưa được triển khai đầy đủ.

## 2. Những điểm thực tế hiện có

### Có thật
- `pentami-core` là module trung tâm và đang có backend FastAPI.
- `shared` chứa các schema và protocol dùng chung.
- `deploy/docker-compose.yml` đã định nghĩa các service PostgreSQL, Redis và Qdrant.
- `mcp-playwright` có cấu trúc server/ folder rõ ràng.

### Cần kiểm tra lại
- Một số mô tả trong README/ARCHITECTURE mang tính “vision”, chưa chắc đã có implementation tương ứng 1-1.
- Nhiều phân hệ được mô tả như đã hoàn thiện, nhưng thực tế thư mục chỉ là khung dự án hoặc tài liệu mẫu.
- Cần nhấn mạnh phân loại: core / integration / prototype / roadmap.

## 3. Khuyến nghị

### A. Tách rõ cấp độ
1. `Vision`: mô tả hướng đi chiến lược.
2. `Architecture`: mô tả hệ thống logic và flows.
3. `Implementation`: chỉ liệt kê phần code thật có.
4. `Roadmap`: phần chưa triển khai hoặc dự kiến.

### B. Thiết lập quy tắc tài liệu
- mỗi module phải có README xác định scope,
- mỗi api phải có contract,
- mỗi dữ liệu quan trọng phải có model trong `shared`.

### C. Rà soát naming
- chuẩn hóa tên hệ thống: `pentami-core`, `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `pentanote`.
- tránh dùng tên khác nhau như `PentaKurumi`, `pentamo`, `PentaMo`, `Pentakai` không thống nhất.

## 4. Kết quả cần đạt

Sau khi chuẩn hóa:

- tài liệu sẽ đúng với trạng thái hiện tại,
- mọi người dễ hiểu đâu là core, đâu là app phụ,
- kế hoạch phát triển rõ hơn, ít rủi ro nhầm lẫn trong triển khai.

## 5. Mục tiêu cuối cùng

Dự án nên hoạt động theo mô hình rõ ràng hơn:

- `core` triển khai logic nền tảng,
- `apps` triển khai chức năng chuyên biệt,
- `shared` làm nền tảng giao tiếp,
- `deploy` quản lý môi trường,
- `docs` là tài liệu chính xác nhất.
