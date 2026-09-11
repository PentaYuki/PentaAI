# Người dùng cuối và phạm vi MCP

## 1. Người dùng mục tiêu

Penta AI không phục vụ một nhóm người duy nhất. Sản phẩm nên bắt đầu bằng các workflow rõ ràng, sau đó cá nhân hóa theo vai trò.

| Nhóm | Nhu cầu chính | Ứng dụng ưu tiên | Mức hỗ trợ cần thiết |
| --- | --- | --- | --- |
| Học sinh/sinh viên | Học bài, làm bài, ghi chú, ôn tập, tìm tài liệu | `pentaschool`, `pentanote`, `pentakuru` | Cao: hướng dẫn từng bước, giải thích dễ hiểu, không tự nộp bài |
| Giáo viên/giảng viên | Soạn bài, tạo quiz, theo dõi lớp, chia sẻ tài liệu | `pentaschool`, `pentanote`, `pentakuru` | Trung bình/cao: batch action, preview trước khi xuất bản |
| Công nhân/kỹ thuật viên | Tra cứu quy trình, checklist, báo cáo ca, đào tạo an toàn | `pentakuru`, `pentanote`, `pentaschool` | Cao: giao diện ít thao tác, voice/input ngắn, offline-friendly |
| Nhân viên văn phòng | Viết tài liệu, quản lý việc, họp, báo cáo, mua sắm và tuyển dụng | `pentanote`, `pentakuru`, `pentamarket`, `pentajob` | Trung bình: automation có preview và audit |
| Người ít am hiểu máy tính | Tìm file, mở website, điền biểu mẫu, xử lý công việc cơ bản | `pentami-core`, `pentanote`, `pentamarket`, `pentajob` | Rất cao: wizard, xác nhận trước hành động, khôi phục và giải thích lỗi |

## 2. Ưu tiên trải nghiệm người dùng

1. **Một cửa vào:** người dùng bắt đầu ở `pentami-core`, không cần biết app nào xử lý yêu cầu.
2. **Trả lời theo vai trò:** cùng một yêu cầu có mức giải thích khác nhau cho học sinh, giáo viên, công nhân hoặc văn phòng.
3. **Không tự động hóa mù:** mọi thao tác gửi, mua, xóa, đăng ký, nộp bài hoặc thay đổi dữ liệu phải preview và yêu cầu xác nhận.
4. **Giảm gánh nặng kỹ thuật:** dùng hướng dẫn từng bước, trạng thái rõ ràng, nút hoàn tác và thông báo lỗi có cách xử lý.
5. **Bảo vệ dữ liệu:** không đọc hoặc tải file local nếu người dùng chưa chọn rõ phạm vi.

## 3. MCP dùng để làm gì

`mcp-playwright` là lớp **điều khiển trình duyệt web** cho các ứng dụng có workflow web. Nó nhận action contract từ `pentami-core`, thực hiện trong browser context riêng theo session, rồi trả kết quả để core hiển thị hoặc tiếp tục workflow.

### Được phép tích hợp

| Ứng dụng | Ví dụ thao tác web |
| --- | --- |
| `pentami-core` | Mở trang app, điều hướng dashboard, lấy trạng thái workflow |
| `pentaschool` | Mở lớp, tạo quiz dạng draft, xem tiến độ, chuẩn bị tài liệu |
| `pentamarket` | Tìm sản phẩm, so sánh, áp voucher dạng preview, tạo giỏ hàng |
| `pentajob` | Tìm việc, điền hồ sơ dạng draft, đặt lịch phỏng vấn |
| `pentanote` | Mở workspace, tạo trang, cập nhật block hoặc export tài liệu |

### Không được tích hợp

`pentakuru` **không dùng MCP Playwright**. Đây là ranh giới cố định vì `pentakuru` xử lý file và dữ liệu local trên máy người dùng, không phải browser automation. Các thao tác của `pentakuru` phải đi qua local permission boundary và file/indexing API riêng:

- chọn thư mục rõ ràng;
- xin quyền đọc/ghi theo hệ điều hành;
- hiển thị file nào sẽ bị đọc hoặc thay đổi;
- không cho Playwright truy cập filesystem local;
- không gửi nội dung file lên web nếu chưa có consent.

## 4. Action policy

Mỗi action MCP trong tương lai cần tối thiểu:

```json
{
  "action_id": "act_123",
  "target_app": "pentamarket",
  "tool": "playwright_fill",
  "risk": "high",
  "requires_confirmation": true,
  "session_id": "sess_123",
  "payload": {}
}
```

Phân loại rủi ro:

- `low`: mở trang, đọc tiêu đề, chụp screenshot.
- `medium`: tìm kiếm, lọc, điền dữ liệu chưa gửi.
- `high`: gửi form, đặt lịch, tạo đơn, xuất bản, nộp hồ sơ.
- `critical`: thanh toán, xóa dữ liệu, thay đổi quyền hoặc gửi dữ liệu nhạy cảm.

`high` và `critical` luôn yêu cầu xác nhận người dùng ngay trước thao tác cuối. Tất cả action phải có timeout, URL allowlist, audit event và cơ chế hủy.

## 5. Trạng thái implementation

Hiện tại `mcp-playwright` mới là Python controller prototype; chưa có MCP transport, policy engine hoặc backend integration hoàn chỉnh. Tài liệu này là phạm vi đích, không phải tuyên bố các workflow đã sẵn sàng.
