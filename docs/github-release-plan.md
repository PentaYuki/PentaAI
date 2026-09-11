# GitHub Release Plan

## Mục tiêu

Mỗi thay đổi phải dễ review, mỗi release phải tái hiện được và người dùng phải biết rõ release đã có gì, giới hạn nào còn tồn tại.

## Quy ước nhánh

- `main`: code đã qua CI, là nhánh phát hành.
- `work/<module>`: nhánh phát triển dài hơn cho một module lớn trong monorepo.
- `feature/<scope>-<short-name>`: tính năng mới.
- `fix/<scope>-<short-name>`: sửa lỗi.
- `docs/<scope>-<short-name>`: tài liệu.
- Không push trực tiếp vào `main` sau khi bật branch protection; mọi thay đổi đi qua pull request.

### Branch map của monorepo

Các nhánh nền dưới đây dùng để tách tiến độ giữa các module. Chúng đều bắt đầu từ `main`, không phải là release branch:

| Branch | Phạm vi |
| --- | --- |
| `work/pentami-core` | FastAPI backend, frontend desktop và orchestration |
| `work/pentaschool` | Module giáo dục, dataset và knowledge base |
| `work/pentakuru` | File assistant, indexing và dataset tài liệu |
| `work/pentamarket` | Commerce, pricing, voucher và VAT |
| `work/pentajob` | Job matching, CV và mock interview |
| `work/pentanote` | Notes, flashcards và knowledge graph |
| `work/mcp-playwright` | Browser controller/MCP integration |
| `work/shared` | Schema, protocol và helper dùng chung |
| `work/deploy` | Compose, migration và môi trường triển khai |

Quy trình cho một module:

```text
main
	-> work/pentami-core
			 -> feature/pentami-core/chat-router
			 -> fix/pentami-core/health-check
```

Chỉ merge thay đổi nhỏ vào `work/<module>` qua PR. Khi module đạt mốc tích hợp, mở PR từ `work/<module>` vào `main`; không merge chéo mã nguồn nội bộ giữa các module chỉ vì chúng nằm trong cùng repository.

Không nên tạo branch cho từng thư mục `dataset/`, `assets/` hoặc từng file. Những phần đó đi cùng branch module sở hữu chúng.

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
- Branch protection nhẹ cho `work/*`: yêu cầu CI xanh và PR khi thay đổi ảnh hưởng contract/shared.
- Squash merge; tắt merge commit nếu team nhỏ.
- Dependency alerts, secret scanning và push protection.
- Discussions hoặc issue labels cho roadmap.
- Chỉ maintainer có quyền tạo tag `v*.*.*`.
