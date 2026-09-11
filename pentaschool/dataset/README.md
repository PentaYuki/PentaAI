# Pentaschool Datasheet & Dataset (Hệ Thống Môn Học Phổ Thông & Nâng Cao)

> **Cấu trúc dữ liệu phân tán cho toàn bộ các môn học trong nhà trường**  
> Thay vì chỉ gói gọn trong lập trình, hệ thống bao quát toàn diện các môn Khoa học Tự nhiên, Xã hội và Ngoại ngữ.

---

## 🏛️ Cây Thư Mục Các Môn Học

```text
pentaschool/dataset/ (hoặc datasheet/)
├── toan/                           # Môn Toán Học
│   ├── dai_so/                     # Đại số: Phương trình, Bất đẳng thức, Ma trận
│   ├── hinh_hoc/                   # Hình học: Không gian, Tọa độ, Vector
│   └── giai_tich/                  # Giải tích: Đạo hàm, Tích phân, Giới hạn
├── vat_ly/                         # Môn Vật Lý
│   ├── co_hoc/                     # Động học, Động lực học, Năng lượng
│   ├── nhiet_hoc/                  # Nhiệt động lực học, Chất khí
│   ├── dien_tu_hoc/                # Điện trường, Dòng điện không đổi, Cảm ứng điện từ
│   └── quang_hoc/                  # Khúc xạ, Phản xạ, Thấu kính, Sóng ánh sáng
├── hoa_hoc/                        # Môn Hóa Học
│   ├── hoa_vo_co/                  # Kim loại, Phi kim, Axit, Bazo, Muối
│   ├── hoa_huu_co/                 # Hydrocacbon, Ancol, Este, Polime
│   └── hoa_dai_cuong/              # Cấu tạo nguyên tử, Bảng tuần hoàn, Tốc độ phản ứng
├── sinh_hoc/                       # Môn Sinh Học
│   ├── sinh_hoc_te_bao/            # Cấu trúc tế bào, Phân bào, Trao đổi chất
│   ├── di_truyen_hoc/              # Quy luật Menđen, Đột biến gen, Nhiễm sắc thể
│   └── sinh_thai_hoc/              # Quần thể, Quần xã, Hệ sinh thái
├── ngu_van/                        # Môn Ngữ Văn
│   ├── van_hoc_trung_dai/          # Văn học thời phong kiến (Truyện Kiều, Chinh Phụ Ngâm...)
│   ├── van_hoc_hien_dai/           # Thơ Mới, Văn học hiện thực, Văn học cách mạng
│   └── ky_nang_lam_van/            # Nghị luận xã hội, Nghị luận văn học
├── tieng_anh/                      # Môn Tiếng Anh
│   ├── ngu_phap_grammar/           # Các thì, Câu điều kiện, Mệnh đề quan hệ
│   ├── tu_vung_vocabulary/         # Từ vựng theo chủ đề (Academic, Daily life)
│   └── luyen_thi_ielts_toeic/      # Dạng bài thi quốc tế (Reading, Listening, Writing, Speaking)
├── lich_su/                        # Môn Lịch Sử
│   ├── lich_su_viet_nam/           # Dựng nước, Giữ nước, Lịch sử kháng chiến
│   └── lich_su_the_gioi/           # Lịch sử cổ đại, cận đại và hiện đại thế giới
├── dia_ly/                         # Môn Địa Lý
│   ├── dia_ly_tu_nhien/            # Địa hình, Khí hậu, Thủy văn, Khoáng sản
│   └── dia_ly_kinh_te_xa_hoi/      # Dân cư, Các vùng kinh tế, Thương mại quốc tế
└── tin_hoc/                        # Môn Tin Học
    ├── tin_hoc_dai_cuong/          # Hệ điều hành, Mạng máy tính, Phần cứng
    └── lap_trinh_co_ban/           # Tư duy thuật toán, Pascal/C++/Python căn bản
```

---

## 📝 Chuẩn Dữ Liệu Q&A & Bài Giảng (Schema Definition)

Mỗi file dữ liệu bài giảng/câu hỏi được thêm vào sau này sẽ tuân thủ cấu trúc chuẩn:

```json
{
  "subject": "toan",
  "branch": "dai_so",
  "grade_level": 12,
  "lesson_title": "Khảo sát và vẽ đồ thị hàm số",
  "theories": [
    "Khái niệm tính đơn điệu của hàm số",
    "Quy tắc tìm cực trị bằng đạo hàm bậc một và bậc hai"
  ],
  "qa_pairs": [
    {
      "q": "Làm thế nào để tìm điểm cực đại của hàm số bậc ba?",
      "q_unaccent": "lam the nao de tim diem cuc dai cua ham so bac ba",
      "a": "Bước 1: Tính đạo hàm y'. Bước 2: Giải phương trình y' = 0. Bước 3: Lập bảng biến thiên hoặc xét dấu đạo hàm bậc hai y''(x) < 0."
    }
  ]
}
```
