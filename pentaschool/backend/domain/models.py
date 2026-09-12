"""PentaSchool domain models — LMS K12 (lop 1-12).

Design: than thien, don gian, khong cung nhac.
Module hoa: catalog / learning / quiz / tutor / growth / video.
"""
from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CapHoc(str, Enum):
    TIEU_HOC = "tieu_hoc"      # lop 1-5
    THCS = "thcs"              # lop 6-9
    THPT = "thpt"              # lop 10-12


CAP_CUA_LOP: Dict[int, CapHoc] = {
    1: CapHoc.TIEU_HOC, 2: CapHoc.TIEU_HOC, 3: CapHoc.TIEU_HOC,
    4: CapHoc.TIEU_HOC, 5: CapHoc.TIEU_HOC,
    6: CapHoc.THCS, 7: CapHoc.THCS, 8: CapHoc.THCS, 9: CapHoc.THCS,
    10: CapHoc.THPT, 11: CapHoc.THPT, 12: CapHoc.THPT,
}


class MonHoc(str, Enum):
    TOAN = "toan"
    TIENG_VIET = "tieng_viet"
    NGU_VAN = "ngu_van"
    TIENG_ANH = "tieng_anh"
    KHOA_HOC = "khoa_hoc"
    VAT_LY = "vat_ly"
    HOA_HOC = "hoa_hoc"
    SINH_HOC = "sinh_hoc"
    LICH_SU = "lich_su"
    DIA_LY = "dia_ly"
    TIN_HOC = "tin_hoc"


THONG_TIN_MON = {
    "toan": {"ten": "Toán", "icon": "🔢", "mau": "#FFB84D"},
    "tieng_viet": {"ten": "Tiếng Việt (Tiểu học)", "icon": "📖", "mau": "#FF8FA3"},
    "ngu_van": {"ten": "Ngữ Văn", "icon": "✍️", "mau": "#FF8FA3"},
    "tieng_anh": {"ten": "Tiếng Anh", "icon": "🌍", "mau": "#6EC6FF"},
    "khoa_hoc": {"ten": "Khoa học", "icon": "🔬", "mau": "#7ED6A5"},
    "vat_ly": {"ten": "Vật Lý", "icon": "⚡", "mau": "#B388FF"},
    "hoa_hoc": {"ten": "Hóa Học", "icon": "🧪", "mau": "#64DFDF"},
    "sinh_hoc": {"ten": "Sinh Học", "icon": "🌱", "mau": "#95D5B2"},
    "lich_su": {"ten": "Lịch Sử", "icon": "🏛️", "mau": "#E0AA6E"},
    "dia_ly": {"ten": "Địa Lý", "icon": "🗺️", "mau": "#80ED99"},
    "tin_hoc": {"ten": "Tin Học", "icon": "💻", "mau": "#90E0EF"},
}


class BaiHoc(BaseModel):
    id: str
    mon: str
    lop: int
    tieu_de: str
    muc_tieu: str = ""
    noi_dung: str = ""
    video_url: Optional[str] = None
    thoi_luong_phut: int = 15
    do_kho: int = Field(default=1, ge=1, le=3)  # 1 de, 2 vua, 3 kho
    thu_tu: int = 1


class VideoBaiGiang(BaseModel):
    """DB CHI CHUA LINK — khong bao gio chua blob video.

    - youtube: video_url = https://youtube.com/watch?v=ID, embed tu sinh
    - mp4/s3/cdn: video_url = https://cdn.../lop1-cong.mp4 (file mp4 truc tiep)
    - drive/vimeo: video_url = link share, embed_url nhap tay
    Thumbnail cung la link, khong phai blob.
    """
    id: str
    lesson_id: str
    tieu_de_video: str = ""
    video_url: str = ""
    video_provider: str = "youtube"  # youtube | mp4 | s3 | vimeo | drive
    video_id_or_file: str = ""       # youtube_id hoac object_key S3
    embed_url: str = ""              # iframe src (backend tu sinh neu trong)
    thumbnail_url: str = ""          # link anh bia
    thoi_luong_giay: int = 0
    chat_luong: str = "720p"
    ngon_ngu: str = "vi"
    co_phu_de: bool = True
    thu_tu: int = 1
    mien_phi: bool = True
    trang_thai: str = "ready"        # draft | ready | hidden
    luot_xem: int = 0

    def embed_tu_dong(self) -> str:
        """Tu sinh embed_url tu video_url neu chua co."""
        if self.embed_url:
            return self.embed_url
        u = (self.video_url or "").strip()
        if self.video_provider == "youtube":
            vid = self.video_id_or_file
            if not vid and ("v=" in u or "youtu.be/" in u):
                if "youtu.be/" in u:
                    vid = u.split("youtu.be/")[-1].split("?")[0].split("&")[0]
                else:
                    vid = u.split("v=")[-1].split("&")[0]
            if vid:
                return f"https://www.youtube.com/embed/{vid}"
        return u  # mp4/s3: frontend dung <video src=...>


class TienDoVideo(BaseModel):
    hoc_sinh: str = "em"
    video_id: str = ""
    giay_da_xem: int = 0
    hoan_thanh: bool = False


class CauHoi(BaseModel):
    id: str
    bai_hoc_id: str
    mon: str
    lop: int
    dang: str = "trac_nghiem"  # trac_nghiem | dung_sai | dien_khuyet
    cau_hoi: str
    lua_chon: List[str] = Field(default_factory=list)
    dap_an_dung: str
    giai_thich: str = ""
    diem: float = 1.0


class KetQuaLamBai(BaseModel):
    cau_hoi_id: str
    tra_loi: str
    dung: bool
    diem_dat: float


class BaiLam(BaseModel):
    id: str
    hoc_sinh: str = "em"
    bai_hoc_id: str
    ket_qua: List[KetQuaLamBai] = Field(default_factory=list)
    tong_diem: float = 0
    tong_diem_toi_da: float = 0
    nhan_xet: str = ""
    sao_thuong: int = 0


class TienDo(BaseModel):
    hoc_sinh: str = "em"
    bai_hoc_id: str
    trang_thai: str = "dang_hoc"  # chua_hoc | dang_hoc | da_hoc
    phan_tram: int = 0
    sao: int = 0


class HoTroTutor(BaseModel):
    cau_hoi: str
    mon: Optional[str] = None
    lop: Optional[int] = None
    tra_loi: str
    cac_buoc: List[str] = Field(default_factory=list)
    cong_thuc_lien_quan: List[str] = Field(default_factory=list)
    loi_khuyen: str = ""
    can_giao_vien: bool = False
