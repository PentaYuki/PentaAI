# PentaSchool — Lộ trình giai đoạn tiếp theo

> Cập nhật: sau khi hoàn thành 5 module LMS + 3 theme theo cấp + trang giáo viên (radiant).
> Quy ước mở rộng: thêm chức năng = thêm 1 file `mod_<ten>.js` + 1 `<section data-module>` — không sửa code cũ.

## 1. Những gì đã có (đã verify + push branch `work/pentaschool`)

| Hạng mục | Trạng thái |
|---|---|
| 5 module học sinh (home / courses / classroom / tutor / growth) + Lab | ✅ |
| 3 theme theo cấp (Cấp 1 dễ thương / Cấp 2 xanh thiên nhiên / Cấp 3 navy hiện đại) | ✅ |
| Video bài giảng — DB chỉ chứa LINK (`school_lesson_videos`) | ✅ |
| Trang giáo viên `/giao-vien` — giao diện radiant tím dùng chung 3 cấp | ✅ |
| Backend: catalog / learning / tutor / videos / **teacher** APIs | ✅ |
| DB: SQLite (dev) ↔ PostgreSQL (prod), migration `003_...sql` | ✅ |

## 2. Giai đoạn kế tiếp — thứ tự ưu tiên

### Phase 4.1 — Đăng nhập & phân quyền (ưu tiên cao nhất)
- Dùng lại `shared/auth/key_manager.py` của PentaAI.
- 3 vai trò: `hoc_sinh` / `giao_vien` / `phu_huynh`. Trang `/giao-vien` hiện đang mở (demo) → chặn khi có auth.
- Thêm bảng `school_users` (migration `004_users.sql`), JWT lưu trong cookie HttpOnly.
- Frontend: thêm `js/core/ps_auth.js` (core, không phải module).

### Phase 4.2 — Giáo viên: tạo/sửa bài học + quiz
- Backend đã có `POST /api/school/teacher/videos`; bổ sung:
  - `POST /teacher/bai-hoc` — tạo bài (nội dung + quiz) thay vì chỉ dùng seed.
  - `PUT /teacher/bai-hoc/{id}` — sửa nội dung, thêm câu hỏi.
- Frontend: tab "Bài học" trong `/giao-vien` thêm form soạn bài (mô tả + 3 câu hỏi).
- Cần migration `005_teacher_lessons.sql` (bảng `school_bai_hoc` thật thay seed cứng).

### Phase 4.3 — Báo cáo & phân tích (tab "Báo cáo" hiện là placeholder)
- `GET /teacher/bao-cao?lop=6` → % đúng sai, câu hay sai nhất, sao trung bình.
- Xem tiến độ video (`school_video_progress` đã có sẵn) → biết học sinh xem đến phút nào.
- Xuất CSV/Excel.

### Phase 4.4 — Nội dung video thật
- Seed link YouTube thật cho 14 bài (hiện chỉ 2 video demo).
- Thumbnail tự lấy từ YouTube ( dùng `img.youtube.com/vi/<id>/hqdefault.jpg`).

### Phase 4.5 — Nâng cao (sau cùng)
- Nối tutor vào AI thật (pentami-core) thay logic cứng.
- RAG tra cứu tài liệu (Qdrant đã có trong `deploy/docker-compose.yml`).
- Thi văn phòng phẩm: đề thi thử tính giờ cho Cấp 3 (Lab đã có khung Pomodoro).

## 3. Ghi chú kỹ thuật cho người tiếp theo

- **Đặt tên module**: `js/core/ps_*.js` = hạ tầng; `js/modules/mod_*.js` = tính năng; chi tiết ở `MODULE-NAMING.md`.
- **Icon theo cấp**: gọi `icon("teacher")` từ `ps_icons.js` thay vì emoji cứng.
- **Tokens**: component không ghi radius/px cứng, dùng `--r-*` từ `ps_tokens.css`.
- **Trang giáo viên** tách riêng, không phụ thuộc `body[data-cap]` (một giao diện cho cả 3 cấp).
- **DB chỉ chứa link video** — tuyệt đối không lưu blob video vào DB.
- Chạy dev: `python3 -m pentaschool.backend.main` → học sinh `http://127.0.0.1:8001/`, giáo viên `/giao-vien`.
