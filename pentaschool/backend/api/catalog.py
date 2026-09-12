from fastapi import APIRouter, Query
from ..domain.models import THONG_TIN_MON, CAP_CUA_LOP
from ..infrastructure.store import STORE

router = APIRouter(tags=["catalog"])

@router.get("/mon-hoc")
def list_mon():
    return {"ds_mon": [{"id": k, **v} for k, v in THONG_TIN_MON.items()]}

@router.get("/bai-hoc")
def list_bai(lop: int | None = Query(default=None, ge=1, le=12), mon: str | None = None):
    ds = STORE.list_bai_hoc(lop=lop, mon=mon)
    return {"tong": len(ds), "ds": [b.model_dump() for b in ds]}

@router.get("/bai-hoc/{bai_id}")
def chi_tiet(bai_id: str):
    b = STORE.get_bai_hoc(bai_id)
    if not b:
        return {"loi": "Khong tim thay bai hoc"}
    quiz = STORE.quiz_theo_bai(bai_id)
    # an dap an khi tra quiz cho hoc sinh
    quiz_an = [{**c.model_dump(exclude={"dap_an_dung"}), "so_lua_chon": len(c.lua_chon)} for c in quiz]
    return {"bai": b.model_dump(), "quiz": quiz_an, "cap": CAP_CUA_LOP.get(b.lop, "thcs")}
