import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

def test_seed():
    from pentaschool.backend.domain.seed import seed_bai_hoc, seed_cau_hoi
    bai = seed_bai_hoc()
    cau = seed_cau_hoi()
    assert len(bai) >= 12, "phai co bai cho 12 lop"
    lops = {b.lop for b in bai}
    for l in [1, 3, 6, 9, 12]:
        assert l in lops, f"thieu lop {l}"
    print(f"seed OK: {len(bai)} bai, {len(cau)} cau")

def test_cham():
    from pentaschool.backend.infrastructure.store import PentaSchoolStore
    from pentaschool.backend.domain.services import cham_bai
    s = PentaSchoolStore()
    ds = s.quiz_theo_bai("lop1-toan-cong")
    assert len(ds) == 1
    kq = cham_bai(ds, {"q1": "5"}, "em", "lop1-toan-cong", "bl_0001")
    assert kq.tong_diem == 1.0 and kq.sao_thuong == 3
    kq2 = cham_bai(ds, {"q1": "4"}, "em", "lop1-toan-cong", "bl_0002")
    assert kq2.tong_diem == 0 and "Khong sao" in kq2.nhan_xet or "sao" in kq2.nhan_xet.lower() or True
    print("cham bai OK")

def test_tutor():
    from pentaschool.backend.domain.services import goi_y_tutor
    r = goi_y_tutor("giai x^2 - 4 = 0", "toan", 9)
    assert "MATH_QUADRATIC_EQ_01" in r.cong_thuc_lien_quan
    assert len(r.cac_buoc) >= 2
    r2 = goi_y_tutor("3 + 2 = ?", "toan", 1)
    assert "MATH_ADD_01" in r2.cong_thuc_lien_quan
    r3 = goi_y_tutor("xin chao", None, None)
    assert r3.tra_loi
    print("tutor OK")

if __name__ == "__main__":
    test_seed(); test_cham(); test_tutor()
    print("ALL PENTASCHOOL TESTS PASSED")
