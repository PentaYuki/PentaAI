"""Services: cham bai + tutor giong giao vien hien hoa."""
from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any
from .models import CauHoi, KetQuaLamBai, BaiLam, HoTroTutor

FORMULA_PATH = Path(__file__).resolve().parent.parent.parent / "knowledge_base" / "formula_registry.json"


def load_formulas() -> list[dict]:
    try:
        data = json.loads(FORMULA_PATH.read_text(encoding="utf-8"))
        return data.get("formulas", [])
    except Exception:
        return []


def cham_bai(cau_list: List[CauHoi], tra_loi: Dict[str, str], hoc_sinh: str, bai_hoc_id: str, bailam_id: str) -> BaiLam:
    kq: List[KetQuaLamBai] = []
    tong = 0.0
    toi_da = 0.0
    for c in cau_list:
        toi_da += c.diem
        tl = (tra_loi.get(c.id, "") or "").strip()
        dung = tl.lower() == c.dap_an_dung.strip().lower()
        diem = c.diem if dung else 0.0
        tong += diem
        kq.append(KetQuaLamBai(cau_hoi_id=c.id, tra_loi=tl, dung=dung, diem_dat=diem))
    # nhan xet nhe nhang, nghiem tuc
    if not cau_list:
        nhan_xet = "Bài này chưa có câu hỏi, em cứ đọc bài trước nhé!"
        sao = 0
    elif tong == toi_da:
        nhan_xet = "Tuyệt vời! Em làm đúng hết rồi, giữ phong độ nhé! 🌟"
        sao = 3
    elif tong >= toi_da * 0.6:
        nhan_xet = "Em làm khá tốt! Xem lại phần giải thích để chắc hơn nhé. 💪"
        sao = 2
    elif tong > 0:
        nhan_xet = "Em đã cố gắng rồi! Đừng nản, mình ôn lại từng bước một nhé. 🌱"
        sao = 1
    else:
        nhan_xet = "Không sao đâu, ai cũng có lúc sai. Mình học lại cùng nhau nhé! 🤗"
        sao = 0
    return BaiLam(id=bailam_id, hoc_sinh=hoc_sinh, bai_hoc_id=bai_hoc_id,
                  ket_qua=kq, tong_diem=tong, tong_diem_toi_da=toi_da,
                  nhan_xet=nhan_xet, sao_thuong=sao)


def goi_y_tutor(cau_hoi_text: str, mon: str | None, lop: int | None) -> HoTroTutor:
    """Ban dau: tra loi theo mau + cong thuc co san. Sau nay noi LLM/RAG."""
    t = (cau_hoi_text or "").lower()
    formulas = load_formulas()
    lien_quan: List[str] = []
    buoc: List[str] = []
    # rule don gian
    if "delta" in t or "phương trình bậc 2" in t or "phuong trinh bac 2" in t or "x^2" in t:
        lien_quan.append("MATH_QUADRATIC_EQ_01")
        buoc = [
            "Bước 1: Xác định a, b, c trong ax²+bx+c=0",
            "Bước 2: Tính Delta = b² - 4ac",
            "Bước 3: Nếu Delta >= 0 thì tính nghiệm, nếu Delta < 0 thì vô nghiệm",
        ]
        tl = "Cô hướng dẫn em giải phương trình bậc hai từng bước nhé. Em thay số vào công thức Delta trước, rồi mới tính nghiệm."
    elif "pitago" in t or "tam giác vuông" in t or "tam giac vuong" in t:
        lien_quan.append("MATH_PYTHAGORAS_01")
        buoc = ["Bước 1: Xác định 2 cạnh góc vuông a, b", "Bước 2: Tính c² = a² + b²", "Bước 3: Lấy căn bậc hai"]
        tl = "Định lý Pitago dùng cho tam giác vuông. Em bình phương 2 cạnh góc vuông cộng lại rồi lấy căn nhé."
    elif "v = v0" in t or "vận tốc" in t or "van toc" in t or "gia tốc" in t:
        lien_quan.append("PHYS_ACCEL_01")
        buoc = ["Bước 1: Ghi v0, a, t", "Bước 2: Áp dụng v = v0 + a*t", "Bước 3: Thay số và ghi đơn vị m/s"]
        tl = "Bài chuyển động biến đổi đều, em liệt kê v0, a, t rồi thay vào công thức v = v0 + a*t nhé."
    elif "mol" in t:
        lien_quan.append("CHEM_MOLE_01")
        buoc = ["Bước 1: Ghi m và M", "Bước 2: Áp dụng n = m/M", "Bước 3: Tính và ghi mol"]
        tl = "Tính số mol theo khối lượng: n = m / M. Em chia khối lượng cho khối lượng mol nhé."
    elif "cộng" in t or "cong" in t or "+" in t:
        lien_quan.append("MATH_ADD_01")
        buoc = ["Bước 1: Đếm nhóm thứ nhất", "Bước 2: Đếm nhóm thứ hai", "Bước 3: Gộp lại và đếm tổng"]
        tl = "Phép cộng là gộp hai nhóm lại với nhau. Em đếm từng nhóm rồi gộp lại nhé!"
    else:
        tl = (
            "Cô đã nghe câu hỏi của em rồi. Em nói rõ đề bài + lớp + môn để cô hướng dẫn từng bước nhé. "
            "Cô sẽ không cho đáp án ngay mà cùng em tư duy."
        )
        buoc = ["Bước 1: Đọc kỹ đề, gạch chân dữ kiện", "Bước 2: Nhớ lại công thức liên quan", "Bước 3: Làm từng bước nhỏ"]
    # canh bao an toan
    can_gv = any(k in t for k in ["đánh nhau", "tự tử", "tu tu", "chết", "chet", "hack", "bom", "ma túy", "mua dâm"])
    return HoTroTutor(
        cau_hoi=cau_hoi_text, mon=mon, lop=lop, tra_loi=tl, cac_buoc=buoc,
        cong_thuc_lien_quan=lien_quan,
        loi_khuyen="Nếu em thấy khó quá, hãy hỏi thầy cô hoặc ba mẹ nhé. Cô luôn ở đây cùng em. 💛" if not can_gv else "Câu hỏi này nhạy cảm, em hãy hỏi thầy cô / người lớn tin cậy ngay nhé.",
        can_giao_vien=can_gv,
    )
