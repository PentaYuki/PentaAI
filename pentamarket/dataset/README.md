# Pentamarket / Pentamo Datasheet & Dataset (Biểu Phí, Giá Cả & Thuế VAT)

> **Cấu trúc phân tách các thư mục quy tắc thương mại và cấu hình cho Nhà Trường (Tenant)**  
> Cho phép từng trường học hoặc đơn vị bán hàng tùy chỉnh chính sách biểu phí, mức thuế VAT riêng biệt.

---

## 🏛️ Cây Thư Mục Phân Tách

```text
pentamarket/dataset/ (hoặc datasheet/)
├── pricing_rules/          # Quy tắc định giá sản phẩm, khóa học theo từng Tenant
├── tax_vat_configs/        # CẤU HÌNH THUẾ: Mức thuế VAT 8% hoặc 10%, miễn trừ thuế giáo dục
├── school_fee_policies/    # BIỂU PHÍ NHÀ TRƯỜNG: Học phí kỳ, phụ phí giáo trình, thực hành
└── discounts_vouchers/     # Chính sách giảm giá sinh viên, học bổng trường học
```

---

## 🏷️ Chuẩn Cấu Hình Tenant (School Config Schema)

```json
{
  "tenant_id": "truong_dai_hoc_bach_khoa",
  "tax_policy": {
    "vat_rate": 0.08,
    "is_education_tax_exempt": true
  },
  "fee_structure": {
    "base_tuition_per_credit": 450000,
    "lab_fee": 1500000,
    "student_discount_percent": 0.10
  }
}
```
