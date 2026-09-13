# PentaSchool — Database & Video bài giảng

## 1. Dự án dùng database nào?

| Tầng | Database | Vai trò | Trạng thái |
|---|---|---|---|
| **Chính (quan hệ)** | **PostgreSQL 16** (`deploy/docker-compose.yml`, db `penta_ecosystem`) | users, lessons, videos (chỉ link), quiz, tiến độ | migration `003` sẵn; dev dùng SQLite tương thích, prod chỉ cần `DATABASE_URL` |
| **Dev/zero-setup** | **SQLite** (`pentaschool/data/school.db`, tự tạo) | chạy ngay không cần Docker | đang chạy, `/api/health` trả `db: sqlite:...` |
| Cache/session | **Redis :6379** | cache key, rate-limit, pub/sub | đã có container, chưa nối vào flow học |
| Vector/RAG | **Qdrant :6333/6334** | tìm kiếm ngữ nghĩa bài giảng | đã có container, roadmap |
| File video | **KHÔNG lưu trong DB** | YouTube / S3 / CDN | DB chỉ lưu URL |

> Kết luận: **PostgreSQL là DB chính**. Hiện tại code tự fallback SQLite để anh chạy demo không cần cài gì; khi deploy chỉ cần set `DATABASE_URL=postgresql://...` là dùng Postgres thật, không đổi code.

## 2. Thiết kế bảng video (DB CHỈ CHỨA LINK)

File: `deploy/migrations/003_pentaschool_video_lessons.sql`

- `school_lessons`: bài học (id, mon, lop 1-12, tieu_de, muc_tieu, noi_dung...)
- `school_lesson_videos`: **mỗi dòng = 1 link video**
  - `video_url`: URL gốc (youtube watch / mp4 CDN / s3 / drive)
  - `video_provider`: `youtube | mp4 | s3 | vimeo | drive`
  - `video_id_or_file`: youtube_id hoặc object_key S3
  - `embed_url`: iframe src — backend **tự sinh** nếu trống (youtube → `.../embed/ID`)
  - `thumbnail_url`: link ảnh bìa (không blob)
  - `thoi_luong_giay, chat_luong, ngon_ngu, co_phu_de, thu_tu, mien_phi, trang_thai, luot_xem`
- `school_video_progress`: `(hoc_sinh, video_id)` → `giay_da_xem, hoan_thanh` (resume)

Ví dụ 1 bài có 2 nguồn link:
```json
{"id":"vid_cong_01","video_provider":"youtube","video_url":"https://www.youtube.com/watch?v=...","embed_url":"https://www.youtube.com/embed/..."}
{"id":"vid_demo_mp4","video_provider":"mp4","video_url":"https://cdn.pentaschool.vn/lop1/cong.mp4"}
```

## 3. API video (đã chạy :8001)

- `GET /api/school/video?lesson_id=lop1-toan-cong`
- `POST /api/school/video` — thêm link (tự sinh embed cho youtube)
- `POST /api/school/video-tien-do` + `GET /api/school/video-tien-do?hoc_sinh=em`
- Frontend `classroom.js` tự tải video theo bài, render `iframe` (youtube) hoặc `<video>` (mp4/s3), có nút chuyển tập.

## 4. Đổi link thật / thêm video mới

```bash
curl -X POST http://127.0.0.1:8001/api/school/video -H 'Content-Type: application/json' -d '{
  "id":"vid_lop6_pso","lesson_id":"lop6-toan-phanso",
  "tieu_de_video":"Cô giảng phân số (6 phút)",
  "video_url":"https://www.youtube.com/watch?v=VIDEO_ID_THAT",
  "video_provider":"youtube","thoi_luong_giay":360}'
```

## 5. Lên Postgres production

```bash
docker compose -f deploy/docker-compose.yml up -d
DATABASE_URL=postgresql://penta_admin:penta_secure_password_2026@localhost:5432/penta_ecosystem \
  python3 -m pentaschool.backend.main
```
