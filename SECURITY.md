# Security Policy

## Báo cáo lỗ hổng

Không mở issue công khai cho secret, token, credential hoặc lỗ hổng bảo mật có thể khai thác. Hãy liên hệ maintainer của repository qua kênh bảo mật được cấu hình trên GitHub.

Khi báo cáo, cung cấp:

- thành phần và phiên bản/commit bị ảnh hưởng;
- các bước tái hiện tối thiểu;
- tác động dự kiến;
- cách giảm thiểu nếu đã biết.

Không gửi secret thật trong issue, pull request, log hoặc screenshot.

## Quy tắc secret

- Dùng biến môi trường hoặc GitHub Actions Secrets.
- Không commit `.env`, API key, token, password hoặc dữ liệu người dùng.
- Nếu secret bị lộ, thu hồi/rotate ngay rồi mới xóa khỏi source và Git history.
