# Tài liệu dự án Penta AI

## Mục tiêu

Tài liệu này đóng vai trò là điểm vào chuẩn hóa kiến trúc, giúp dự án phân biệt giữa:

- định nghĩa chiến lược và ý tưởng sản phẩm,
- cấu trúc kỹ thuật thực tế hiện có,
- các module cần phát triển tiếp theo,
- các hợp đồng giao tiếp dùng chung giữa các phân hệ.

## Cấu trúc tài liệu

- [architecture/README.md](architecture/README.md): mô tả kiến trúc tổng thể và nguyên tắc thiết kế.
- [architecture/system-overview.md](architecture/system-overview.md): sơ đồ hệ thống, lớp kỹ thuật và luồng dữ liệu.
- [architecture/subsystem-map.md](architecture/subsystem-map.md): bản đồ từng phân hệ và trách nhiệm của từng module.
- [analysis/reality-check.md](analysis/reality-check.md): so sánh giữa mô tả marketing và thực tế mã nguồn.

## Kiến trúc thực tế của dự án

Dự án hiện tại đang hình thành theo mô hình sau:

1. Lõi điều phối: `pentami-core`
2. Shared contracts và models: `shared`
3. Các phân hệ chức năng: `pentaschool`, `pentakuru`, `pentamarket`, `pentajob`, `pentanote`
4. Tự động hóa trình duyệt: `mcp-playwright`
5. Triển khai hạ tầng: `deploy`

## Nguyên tắc cần giữ

- Phân biệt rõ giữa mô tả dự án và code thật.
- Mỗi subsystem phải có mục tiêu, input, output và ràng buộc.
- Tài liệu không được vượt quá trạng thái thực tế của implementation.
- Dùng shared schemas làm “bản hợp đồng dữ liệu” cho toàn hệ sinh thái.

## Mục tiêu phát triển tiếp theo

- Rà soát lại từng module theo đúng thực trạng hiện có.
- Tách rõ “core”, “adapter”, “feature app”, “infra”.
- Chuẩn hóa naming convention, API contract, cấu trúc dữ liệu.
- Liên kết thư mục và doc với implementation để dễ maintain.
