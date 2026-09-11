# GitHub Release Plan

## Mục tiêu

Mỗi thay đổi phải dễ review, mỗi release phải tái hiện được và người dùng phải biết rõ release đã có gì, giới hạn nào còn tồn tại.

## Quy ước nhánh

- `main`: code đã qua CI, là nhánh phát hành.
- `feature/<scope>-<short-name>`: tính năng mới.
- `fix/<scope>-<short-name>`: sửa lỗi.
- `docs/<scope>-<short-name>`: tài liệu.
- Không push trực tiếp vào `main` sau khi bật branch protection; mọi thay đổi đi qua pull request.

## Quy ước commit

Dùng Conventional Commits:

```text
feat: thêm capability
fix: sửa lỗi
refactor: thay đổi cấu trúc không đổi hành vi
docs: cập nhật tài liệu
test: thêm hoặc sửa kiểm thử
ci: thay đổi automation
chore: bảo trì
```

## Luồng pull request

1. Tạo branch từ `main`.
2. Chia thay đổi thành commit nhỏ, không chứa secret.
3. Mở PR với mục tiêu, phạm vi, kiểm tra và breaking change.
4. Chờ CI xanh và ít nhất một maintainer review.
5. Squash merge vào `main`.
6. Xóa branch sau khi merge.

## Quy trình release

### Patch: `v0.1.1`

Sửa lỗi, bảo mật hoặc tài liệu không đổi contract lớn.

### Minor: `v0.2.0`

Thêm capability tương thích ngược.

### Major: `v1.0.0`

Breaking API/schema, thay đổi migration hoặc thay đổi hành vi cần người dùng cập nhật.

### Checklist phát hành

1. Cập nhật `CHANGELOG.md` với section version và ngày.
2. Kiểm tra README, API contract và migration.
3. Chạy CI/smoke test local.
4. Merge PR vào `main`.
5. Tạo annotated tag:

```bash
git checkout main
git pull --ff-only origin main
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

6. Workflow `Release` tự tạo GitHub Release và sinh release notes từ PR/commit.
7. Kiểm tra trang Releases, asset, changelog và hướng dẫn cài đặt.

## Cấu hình GitHub nên bật

- Branch protection cho `main`: PR bắt buộc, CI bắt buộc, branch up-to-date.
- Squash merge; tắt merge commit nếu team nhỏ.
- Dependency alerts, secret scanning và push protection.
- Discussions hoặc issue labels cho roadmap.
- Chỉ maintainer có quyền tạo tag `v*.*.*`.
