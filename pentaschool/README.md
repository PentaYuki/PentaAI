# Pentaschool

Hệ thống quản lý học tập (LMS) thế hệ mới tích hợp **AI Giáo viên & Trợ giảng ảo**.

## Tính Năng Cốt Lõi
1. **Khóa học & Bài giảng**: Video bài giảng, tài liệu học tập, hệ thống bài tập trắc nghiệm và tự luận.
2. **AI Teacher Avatar**: Trợ giảng giọng nói tương tác trực tiếp với học viên theo thời gian thực (được điều phối từ `pentami-core`).
3. **Cá nhân hóa lộ trình**: AI phân tích lỗ hổng kiến thức qua các bài kiểm tra và gợi ý bài giảng bổ sung.
4. **Tích hợp hệ sinh thái**: Sử dụng chung tài khoản và Unified API Key của Penta Ecosystem.

## Cấu Trúc Đề Xuất
```text
pentaschool/
├── src/
│   ├── app/              # Next.js App Router (Dashboard, Courses, Quiz, Classroom)
│   ├── components/       # AI Teacher Video/Avatar, Chatbox, Audio Visualizer
│   ├── hooks/            # useVoiceSession, useEcosystemAuth
│   ├── lib/              # API Client kết nối Pentami Core
│   └── styles/           # CSS & Styling
├── public/               # Static assets
├── package.json          # Dependencies
└── README.md
```
