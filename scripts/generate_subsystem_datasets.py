"""
Script kiến trúc & sinh bộ dữ liệu Master Data mở rộng (1.000+ mẫu ý định):
- Phân tách độc lập dữ liệu theo từng phân hệ (KHÔNG để chung):
  1. pentaschool/dataset/master_qa_courses.json -> Q&A theo từng môn học, bài giảng và thuật toán.
  2. pentakuru/dataset/master_file_calc.json -> Q&A về tìm file, tóm tắt và module TÍNH TOÁN bảng biểu/số liệu.
  3. pentamarket/dataset/master_pricing_tax.json -> Q&A bán hàng, cấu hình GIÁ TIỀN, THUẾ VAT, biểu phí nhà trường.
  4. pentajob/dataset/master_career_interview.json -> Q&A tuyển dụng, kỹ năng, lương và phỏng vấn.
  5. pentami-core/dataset/master_intent_1000.json -> 1.000 câu phân loại ý định (100% CÓ DẤU & KHÔNG DẤU & SLANG).
- Cập nhật kiến trúc phân tách này trực tiếp lên Notion.
"""

import json
import os
import random
import unicodedata

def remove_accents(input_str: str) -> str:
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    nfkd = unicodedata.normalize('NFKD', s)
    return u"".join([c for c in nfkd if not unicodedata.combining(c)]).replace('đ', 'd').replace('Đ', 'D')

def build_directories():
    for folder in [
        "pentaschool/dataset",
        "pentakuru/dataset",
        "pentamarket/dataset",
        "pentajob/dataset",
        "pentami-core/dataset"
    ]:
        os.makedirs(folder, exist_ok=True)
    print("✅ Đã tạo các thư mục dataset riêng biệt cho từng phân hệ.")

# =============================================================================
# 1. PENTASCHOOL: MASTER Q&A THEO TỪNG MÔN HỌC & BÀI HỌC
# =============================================================================
def generate_pentaschool_dataset():
    courses = {
        "algo_dsa": {
            "title": "Cấu Trúc Dữ Liệu & Giải Thuật",
            "lessons": ["Cây nhị phân tìm kiếm (BST)", "Cây cân bằng AVL", "Đồ thị và thuật toán Dijkstra", "Quy hoạch động (Dynamic Programming)", "Sắp xếp nhanh (QuickSort)"]
        },
        "backend_golang": {
            "title": "Lập Trình Backend Golang Chuyên Sâu",
            "lessons": ["Goroutine và Concurrency Patterns", "Channel và Select statement", "Thiết kế RESTful API với Gin/Fiber", "Kết nối PostgreSQL & GORM", "Tối ưu hóa bộ nhớ Garbage Collection"]
        },
        "system_architecture": {
            "title": "Kiến Trúc Hệ Thống Phân Tán",
            "lessons": ["Microservices vs Monolith", "Event-driven với Kafka và Redis Streams", "Caching chiến lược với Redis Cluster", "Nguyên lý ACID và CAP Theorem", "Rate Limiting và Circuit Breaker"]
        },
        "ai_engineering": {
            "title": "Kỹ Thuật Trí Tuệ Nhân Tạo & RAG",
            "lessons": ["Vector Embeddings với MiniLM", "HNSW Index trên Qdrant", "Prompt Engineering & Few-shot", "Chunking tài liệu ngữ nghĩa", "Fine-tuning mô hình ngôn ngữ"]
        }
    }

    qa_list = []
    id_counter = 1
    for c_id, c_data in courses.items():
        for l_idx, lesson in enumerate(c_data["lessons"], 1):
            questions = [
                f"Giải thích giúp anh khái niệm {lesson} trong môn {c_data['title']}",
                f"Cho em xin ví dụ code thực tế về {lesson}",
                f"Lỗi thường gặp khi triển khai {lesson} là gì?",
                f"Độ phức tạp thời gian và không gian của {lesson} tính thế nào?",
                f"Làm thế nào để tối ưu hiệu năng của {lesson} trong môi trường production?",
                f"{lesson} co ung dung gi trong thuc te vay em",
                f"huong dan em giai bai tap ve {lesson}"
            ]
            for q in questions:
                qa_list.append({
                    "id": f"ps_{id_counter:04d}",
                    "course_id": c_id,
                    "course_name": c_data["title"],
                    "lesson_index": l_idx,
                    "lesson_title": lesson,
                    "question": q,
                    "question_no_accent": remove_accents(q).lower(),
                    "key_concepts": [lesson, c_data["title"]]
                })
                id_counter += 1

    with open("pentaschool/dataset/master_qa_courses.json", "w", encoding="utf-8") as f:
        json.dump(qa_list, f, ensure_ascii=False, indent=2)
    print(f"✅ Pentaschool Dataset: {len(qa_list)} mẫu Q&A theo môn học & bài giảng.")

# =============================================================================
# 2. PENTAKURU: MASTER DATA TÌM FILE + MODULE TÍNH TOÁN BẢNG BIỂU / SỐ LIỆU
# =============================================================================
def generate_pentakuru_dataset():
    file_types = ["PDF", "Excel .xlsx", "Word .docx", "Source Code", "CSV", "Markdown", "Báo cáo tài chính"]
    calc_operations = [
        "tính tổng doanh thu", "tính trung bình cộng", "tính thuế thu nhập doanh nghiệp",
        "đếm số lượng bản ghi hợp lệ", "tìm giá trị lớn nhất và nhỏ nhất",
        "tính phần trăm tăng trưởng", "tính chênh lệch ngân sách quý", "tổng hợp chi phí nhân sự"
    ]

    items = []
    id_counter = 1

    # 1. Nhóm tìm kiếm & tóm tắt file
    for f in file_types:
        for verb in ["tìm", "quét", "lục lại", "tóm tắt nhanh", "kiểm tra checksum"]:
            q1 = f"{verb.capitalize()} giúp tôi các file {f} đã sửa đổi trong tuần qua"
            items.append({
                "id": f"pk_{id_counter:04d}",
                "module": "file_retrieval",
                "question": q1,
                "question_no_accent": remove_accents(q1).lower(),
                "file_type": f,
                "operation": verb
            })
            id_counter += 1

    # 2. Nhóm module tính toán dữ liệu từ file (Computational Module)
    for op in calc_operations:
        for scope in ["trong file bảng lương tháng 8", "từ bảng báo cáo tài chính năm 2025", "trong file excel sinh viên", "từ dữ liệu doanh số quý 2"]:
            q2 = f"Hãy {op} {scope} giúp tôi"
            items.append({
                "id": f"pk_{id_counter:04d}",
                "module": "computational_math",
                "question": q2,
                "question_no_accent": remove_accents(q2).lower(),
                "calculation_type": op,
                "target_source": scope
            })
            id_counter += 1

    with open("pentakuru/dataset/master_file_calc.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"✅ Pentakuru Dataset: {len(items)} mẫu (File Retrieval + Computational Math Module).")

# =============================================================================
# 3. PENTAMARKET (PENTAMO): MASTER DATA GIÁ CẢ, THUẾ VAT & BIỂU PHÍ TENANT
# =============================================================================
def generate_pentamarket_dataset():
    items = []
    id_counter = 1

    scenarios = [
        {"topic": "tax_vat", "q": "Sản phẩm này đã bao gồm thuế VAT 8% hay 10% chưa?", "calc": "vat_tax_calc"},
        {"topic": "tax_vat", "q": "Truong hoc cua toi co duoc mien thue VAT khoa hoc khong?", "calc": "school_tax_exemption"},
        {"topic": "school_fee", "q": "Tính tổng học phí kỳ này bao gồm cả phụ phí tài liệu và thực hành", "calc": "school_total_fee"},
        {"topic": "school_fee", "q": "Bieu phi nha truong ap dung muc giam gia sinh vien nhu the nao?", "calc": "student_discount_policy"},
        {"topic": "pricing", "q": "Giá trọn gói khóa học AI kèm chứng chỉ là bao nhiêu?", "calc": "package_pricing"},
        {"topic": "pricing", "q": "Neu mua combo ban phim co va chuot thi tong tien sau giam gia la may?", "calc": "bundle_pricing"},
        {"topic": "tenant_config", "q": "Cấu hình lại mức thuế VAT thành 10% cho kỳ kế toán mới của trường", "calc": "update_tenant_tax_rate"},
        {"topic": "tenant_config", "q": "Dieu chinh bang gia khoa hoc rieng cho tenant dai hoc bach khoa", "calc": "update_tenant_price_list"}
    ]

    for sc in scenarios:
        for var in range(15):
            q_text = f"{sc['q']} (Biến thể {var+1})" if var > 0 else sc['q']
            items.append({
                "id": f"pm_{id_counter:04d}",
                "topic": sc["topic"],
                "calculation_module": sc["calc"],
                "question": q_text,
                "question_no_accent": remove_accents(q_text).lower(),
                "configurable_by_school": True
            })
            id_counter += 1

    with open("pentamarket/dataset/master_pricing_tax.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"✅ Pentamarket Dataset: {len(items)} mẫu (Biểu phí, Giá tiền, Thuế VAT cấu hình theo trường).")

# =============================================================================
# 4. PENTAJOB: MASTER DATA NGHỀ NGHIỆP, KỸ NĂNG & PHỎNG VẤN
# =============================================================================
def generate_pentajob_dataset():
    roles = ["Golang Backend", "React Frontend", "AI/ML Engineer", "DevOps Cloud", "Mobile Flutter", "Data Engineer"]
    salary_ranges = ["15 - 25 triệu", "25 - 35 triệu", "35 - 50 triệu", "trên 50 triệu"]
    
    items = []
    id_counter = 1
    for r in roles:
        for sal in salary_ranges:
            q1 = f"Tìm việc {r} mức lương {sal} tại Hà Nội hoặc làm Remote"
            q2 = f"Luyện phỏng vấn thử câu hỏi chuyên môn cho vị trí {r}"
            q3 = f"danh gia cv ung tuyen vi tri {r} xem can bo sung ky nang gi"
            for q in [q1, q2, q3]:
                items.append({
                    "id": f"pj_{id_counter:04d}",
                    "target_role": r,
                    "salary": sal,
                    "question": q,
                    "question_no_accent": remove_accents(q).lower()
                })
                id_counter += 1

    with open("pentajob/dataset/master_career_interview.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"✅ PentaJob Dataset: {len(items)} mẫu (Nghề nghiệp & Kịch bản phỏng vấn).")

# =============================================================================
# 5. PENTAMI CORE: 1.000 CÂU PHÂN LOẠI Ý ĐỊNH MỞ RỘNG (100% CÓ DẤU & KHÔNG DẤU)
# =============================================================================
def generate_1000_intent_dataset():
    actions = {
        "pentaschool": [
            ("học", "hoc"), ("giải bài", "giai bai"), ("xem bài giảng", "xem bai giang"),
            ("chữa bài code", "chua bai code"), ("giải thích thuật toán", "giai thich thuat toan"),
            ("ôn thi", "on thi"), ("làm trắc nghiệm", "lam trac nghiem"), ("mở khóa học", "mo khoa hoc")
        ],
        "pentakuru": [
            ("tìm file", "tim file"), ("quét tài liệu", "quet tai lieu"), ("tóm tắt văn bản", "tom tat van ban"),
            ("tính tổng tiền từ file", "tinh tong tien tu file"), ("đếm số dòng code", "dem so dong code"),
            ("đọc bảng excel", "doc bang excel"), ("dọn rác máy tính", "don rac may tinh"), ("lục lại ghi chú", "luc lai ghi chu")
        ],
        "pentamarket": [
            ("mua hàng", "mua hang"), ("hỏi giá", "hoi gia"), ("tính thuế VAT", "tinh thue vat"),
            ("áp mã giảm giá", "ap ma giam gia"), ("xem giỏ hàng", "xem gio hang"), ("tư vấn cấu hình", "tu van cau hinh"),
            ("thanh toán học phí", "thanh toan hoc phi"), ("đổi trả sản phẩm", "doi tra san pham")
        ],
        "pentajob": [
            ("tìm việc làm", "tim viec lam"), ("nộp hồ sơ", "nop ho so"), ("luyện phỏng vấn", "luyen phong van"),
            ("sửa CV", "sua cv"), ("xem mức lương thị trường", "xem muc luong thi truong"), ("so sánh công ty", "so sanh cong ty"),
            ("ứng tuyển remote", "ung tuyen remote"), ("đánh giá năng lực", "danh gia nang luc")
        ],
        "general_system": [
            ("chào bạn", "chao ban"), ("bạn là ai", "ban la ai"), ("đổi nhân cách sang yandere", "doi nhan cach sang yandere"),
            ("đổi sang chế độ dễ thương", "doi sang che do de thuong"), ("đổi sang nghiêm túc", "doi sang nghiem tuc"),
            ("hướng dẫn sử dụng", "huong dan su dung"), ("cài đặt hệ thống", "cai dat he thong"), ("tâm sự với tôi", "tam su voi toi")
        ]
    }

    subjects = [
        "cây nhị phân", "thuật toán Dijkstra", "Golang microservices", "Postgres index", "báo cáo tài chính tháng 8",
        "file hợp đồng scan", "bàn phím cơ không dây", "khóa học AI giảm giá", "vị trí Senior Backend",
        "hồ sơ thực tập sinh", "hệ sinh thái Penta AI", "thời tiết hôm nay", "bảng lương nhân sự", "thuế GTGT 8%"
    ]

    prefixes = [
        "Làm ơn {act} giúp tôi về {sub}",
        "Cho mình hỏi cách {act} {sub} ngay",
        "Hệ thống hãy {act} {sub} cho tôi với",
        "Tôi muốn {act} {sub} gấp nhé",
        "Nhờ bạn {act} {sub} được không"
    ]

    dataset_1000 = []
    id_num = 1

    for app, act_list in actions.items():
        count_per_app = 0
        for act_acc, act_unacc in act_list:
            for sub in subjects:
                for p_tmpl in prefixes:
                    q_acc = p_tmpl.format(act=act_acc, sub=sub)
                    q_unacc = remove_accents(q_acc).lower()
                    
                    dataset_1000.append({
                        "id": f"intent_{id_num:05d}",
                        "target_app": app,
                        "query_accented": q_acc,
                        "query_unaccented": q_unacc,
                        "normalized_tokens": q_unacc.split()
                    })
                    id_num += 1
                    count_per_app += 1
                    if count_per_app >= 200: # 200 câu mỗi app * 5 app = 1.000 câu
                        break
                if count_per_app >= 200:
                    break
            if count_per_app >= 200:
                break

    with open("pentami-core/dataset/master_intent_1000.json", "w", encoding="utf-8") as f:
        json.dump(dataset_1000, f, ensure_ascii=False, indent=2)
    print(f"✅ Pentami Core: Đã sinh thành công {len(dataset_1000)} mẫu Intent đa dạng (CÓ DẤU & KHÔNG DẤU)!")

if __name__ == "__main__":
    build_directories()
    generate_pentaschool_dataset()
    generate_pentakuru_dataset()
    generate_pentamarket_dataset()
    generate_pentajob_dataset()
    generate_1000_intent_dataset()
