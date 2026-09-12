from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..infrastructure import db as db_layer

router = APIRouter(tags=["video"])

class VideoReq(BaseModel):
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

class TienDoVideoReq(BaseModel):
    hoc_sinh: str = "em"
    video_id: str = ""
    giay_da_xem: int = 0
    hoan_thanh: bool = False

@router.get("/video")
def ds_video(lesson_id: str):
    ds = db_layer.list_videos(lesson_id)
    return {"tong": len(ds), "ds": ds, "ghi_chu": "DB chi chua link, khong chua file video"}

@router.post("/video")
def them_video(req: VideoReq):
    v = db_layer.add_video(req.model_dump())
    return {"ok": True, "video": v}

@router.post("/video-tien-do")
def luu_td(req: TienDoVideoReq):
    return {"ok": True, "tien_do": db_layer.save_video_progress(req.hoc_sinh, req.video_id, req.giay_da_xem, req.hoan_thanh)}

@router.get("/video-tien-do")
def xem_td(hoc_sinh: str = "em"):
    return {"hoc_sinh": hoc_sinh, "ds": db_layer.get_video_progress(hoc_sinh)}
