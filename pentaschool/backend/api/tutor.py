from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..domain.services import goi_y_tutor

router = APIRouter(tags=["tutor"])

class HoiReq(BaseModel):
    cau_hoi: str
    mon: Optional[str] = None
    lop: Optional[int] = None

@router.post("/hoi")
def hoi(req: HoiReq):
    kq = goi_y_tutor(req.cau_hoi, req.mon, req.lop)
    return {"tra_loi": kq.model_dump()}
