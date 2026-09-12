"""API trang GIAO VIEN — xem/quan ly bai hoc + video (DB chi chua link).

Giai doan dau: khong co auth (ban demo). Khi lam auth thay doi qua shared/auth
ma khong can sua API shape (them dependency DepsLater).
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..infrastructure import db as db_layer
from ..domain import seed as seed_domain

router = APIRouter(tags=["teacher"])


class VideoIn(BaseModel):
    id: str
    lesson_id: str
    tieu_de_video: str = ""
    video_url: str = ""
    video_provider: str = "youtube"  # youtube | mp4 | s3 | vimeo | drive
    video_id_or_file: str = ""
    embed_url: str = ""
    thumbnail_url: str = ""
    thoi_luong_giay: int = 0
    thu_tu: int = 1


@router.get("/teacher/lessons")
def ds_bai(lop: int = 0, mon: str = ""):
    """Danh sach bai hoc de giao vien chon khi gan video."""
    ds = [b.model_dump() if hasattr(b, "model_dump") else dict(b) for b in seed_domain.seed_bai_hoc()]
    if lop:
        ds = [b for b in ds if b.get("lop") == lop]
    if mon:
        ds = [b for b in ds if b.get("mon") == mon]
    return {"tong": len(ds), "ds": ds}


@router.get("/teacher/videos")
def tat_ca_video(lesson_id: str = ""):
    ds = db_layer.list_all_videos(lesson_id or None)
    return {"tong": len(ds), "ds": ds, "ghi_chu": "DB chi chua link video"}


@router.post("/teacher/videos")
def tao_video(req: VideoIn):
    v = db_layer.add_video(req.model_dump())
    return {"ok": True, "video": v}


@router.delete("/teacher/videos/{video_id}")
def xoa_video(video_id: str):
    ok = db_layer.delete_video(video_id)
    return {"ok": ok, "id": video_id}