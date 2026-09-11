# Pentakuru Datasheet & Dataset (Quản Lý File & Module Tính Toán)

> **Cấu trúc phân tách các thư mục chức năng của Pentakuru Desktop**  
> Bao gồm tra cứu tài liệu và hệ thống module tính toán số liệu, bảng biểu phức tạp.

---

## 🏛️ Cây Thư Mục Phân Tách

```text
pentakuru/dataset/ (hoặc datasheet/)
├── file_retrieval/         # Tìm kiếm tệp tin nội bộ (PDF, DOCX, Code, TXT)
├── computational_math/     # MODULE TÍNH TOÁN: Tính tổng, trung bình, min/max từ file
├── financial_tables/       # Phân tích báo cáo tài chính, bảng lương, thuế doanh nghiệp
└── code_analysis/          # Phân tích kiến trúc mã nguồn, đếm dòng code, phát hiện rủi ro
```

---

## 📐 Chuẩn Kịch Bản Tính Toán (Computational Schema)

```json
{
  "module": "computational_math",
  "operation": "sum_column",
  "target_file_type": "xlsx",
  "prompt_patterns": [
    "Tính tổng doanh thu trong file Excel tháng 8",
    "tinh tong doanh thu trong file excel thang 8"
  ],
  "engine_type": "python_pandas_or_duckdb"
}
```
