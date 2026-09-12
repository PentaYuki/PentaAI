"""In-memory store — du de chay demo, sau nay thay bang Postgres."""
from __future__ import annotations
from typing import Dict, List
from ..domain.models import BaiHoc, CauHoi, BaiLam, TienDo
from ..domain.seed import seed_bai_hoc, seed_cau_hoi


class PentaSchoolStore:
    def __init__(self) -> None:
        self.bai_hoc: Dict[str, BaiHoc] = {b.id: b for b in seed_bai_hoc()}
        self.cau_hoi: Dict[str, CauHoi] = {c.id: c for c in seed_cau_hoi()}
        self.bai_lam: Dict[str, BaiLam] = {}
        self.tien_do: Dict[str, TienDo] = {}
        self._dem_bai_lam = 0

    # catalog
    def list_bai_hoc(self, lop: int | None = None, mon: str | None = None) -> List[BaiHoc]:
        ds = list(self.bai_hoc.values())
        if lop is not None:
            ds = [b for b in ds if b.lop == lop]
        if mon:
            ds = [b for b in ds if b.mon == mon]
        return sorted(ds, key=lambda b: (b.lop, b.thu_tu))

    def get_bai_hoc(self, bai_id: str) -> BaiHoc | None:
        return self.bai_hoc.get(bai_id)

    def quiz_theo_bai(self, bai_id: str) -> List[CauHoi]:
        return [c for c in self.cau_hoi.values() if c.bai_hoc_id == bai_id]

    def next_id_bai_lam(self) -> str:
        self._dem_bai_lam += 1
        return f"bl_{self._dem_bai_lam:04d}"


STORE = PentaSchoolStore()
