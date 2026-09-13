from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from ..domain.services import cham_bai
from ..infrastructure.store import STORE
from ..domain.models import TienDo

router = APIRouter(tags=["learning"])

class NopBaiReq(BaseModel):
    bai_hoc_id: str
    hoc_sinh: str = "em"
    tra_loi: Dict[str, str] = {}

class TienDoReq(BaseModel):
    bai_hoc_id: str
    hoc_sinh: str = "em"
    phan_tram: int = 0
    trang_thai: str = "dang_hoc"

@router.post("/nop-bai")
def nop_bai(req: NopBaiReq):
    ds_cau = STORE.quiz_theo_bai(req.bai_hoc_id)
    bid = STORE.next_id_bai_lam()
    kq = cham_bai(ds_cau, req.tra_loi, req.hoc_sinh, req.bai_hoc_id, bid)
    STORE.bai_lam[bid] = kq
    # tu cap nhat tien do
    key = f"{req.hoc_sinh}:{req.bai_hoc_id}"
    STORE.tien_do[key] = TienDo(hoc_sinh=req.hoc_sinh, bai_hoc_id=req.bai_hoc_id,
        trang_thai="da_hoc" if kq.tong_diem >= kq.tong_diem_toi_da * 0.6 else "dang_hoc",
        phan_tram=100 if kq.tong_diem >= kq.tong_diem_toi_da * 0.6 else 60,
        sao=kq.sao_thuong)
    # tra kem giai thich de hoc
    giai = [{"id": c.id, "cau": c.cau_hoi, "dap_an": c.dap_an_dung, "giai_thich": c.giai_thich} for c in ds_cau]
    return {"bai_lam": kq.model_dump(), "giai_thich": giai}

@router.post("/tien-do")
def cap_nhat(req: TienDoReq):
    key = f"{req.hoc_sinh}:{req.bai_hoc_id}"
    td = TienDo(hoc_sinh=req.hoc_sinh, bai_hoc_id=req.bai_hoc_id,
                trang_thai=req.trang_thai, phan_tram=req.phan_tram)
    STORE.tien_do[key] = td
    return {"ok": True, "tien_do": td.model_dump()}

@router.get("/tien-do")
def xem(hoc_sinh: str = "em"):
    ds = [t.model_dump() for k, t in STORE.tien_do.items() if k.startswith(hoc_sinh + ":")]
    tong_sao = sum(t["sao"] for t in ds)
    return {"hoc_sinh": hoc_sinh, "tong_sao": tong_sao, "ds": ds}

@router.get("/goi-y-hom-nay")
def goi_y(hoc_sinh: str = "em", lop: int = 6):
    # goi y don gian: bai chua hoc trong lop
    ds = STORE.list_bai_hoc(lop=lop)
    chua = [b for b in ds if f"{hoc_sinh}:{b.id}" not in STORE.tien_do]
    chon = (chua or ds)[:3]
    return {"loi_chao": f"Hom nay minh hoc 1 bai nho thoi nhe, {hoc_sinh}!",
            "goi_y": [b.model_dump() for b in chon]}
