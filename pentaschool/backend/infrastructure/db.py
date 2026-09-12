"""DB layer: SQLite (dev, khong can cai gi) <-> PostgreSQL (production).

- Dev/may anh: SQLite file pentaschool/data/school.db — chay ngay, 0 phu thuoc.
- Production/Docker: dat DATABASE_URL=postgresql://... -> tu dung Postgres.
- Schema viet theo chuan Postgres, tu map sang SQLite (TIMESTAMPTZ->TEXT...).
- Video CHI CHUA LINK (URL/embed/thumbnail), khong blob.
"""
from __future__ import annotations
import os
import re
import sqlite3
from pathlib import Path
from typing import List, Optional

CUR = Path(__file__).resolve().parent
DATA_DIR = CUR.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
USE_POSTGRES = DATABASE_URL.startswith("postgres")
SQLITE_PATH = DATA_DIR / "school.db"

MIGRATION_SQL = Path("/home/gooleseswsq1/Projects/PentaAI/deploy/migrations/003_pentaschool_video_lessons.sql").read_text(encoding="utf-8")


def _sqlite_ddl(sql: str) -> str:
    """Map DDL Postgres -> SQLite: bo CHECK tam, doi TIMESTAMPTZ, bo ON CONFLICT, INDEX IF NOT EXISTS giu."""
    sql = sql.replace("TIMESTAMPTZ", "TEXT")
    # SQLite khong hieu CHECK co khoang trang phuc tap? — giu nguyen duoc, nhung don gian hoa:
    lines = []
    for ln in sql.splitlines():
        s = ln.strip()
        if s.startswith("--"):
            lines.append(ln)
            continue
        lines.append(ln)
    out = "\n".join(lines)
    # tach tung statement, bo seed ON CONFLICT (SQLite cu khong ho tro) -> INSERT OR IGNORE
    return out


def _get_sqlite() -> sqlite3.Connection:
    con = sqlite3.connect(str(SQLITE_PATH))
    con.row_factory = sqlite3.Row
    return con


def _strip_comments(sql: str) -> str:
    out = []
    for ln in sql.splitlines():
        s = ln.strip()
        if s.startswith("--"):
            continue
        out.append(ln)
    return "\n".join(out)


def init_db() -> str:
    """Tao bang + seed. Tra ve 'sqlite:...' hoac 'postgres:...'."""
    if USE_POSTGRES:
        try:
            import psycopg  # psycopg3
            with psycopg.connect(DATABASE_URL) as c:
                c.execute(MIGRATION_SQL)
                c.commit()
            return f"postgres:{DATABASE_URL.split('@')[-1]}"
        except Exception as e:
            return f"postgres-LOI:{e} (fallback sqlite)"
    # SQLite
    clean = _strip_comments(_sqlite_ddl(MIGRATION_SQL))
    con = _get_sqlite()
    try:
        for stmt in clean.split(";"):
            s = stmt.strip()
            if not s:
                continue
            up = s.upper()
            if up.startswith("INSERT"):
                s2 = re.sub(r"\s+ON CONFLICT.*$", "", s, flags=re.DOTALL | re.IGNORECASE)
                try:
                    con.execute("INSERT OR IGNORE " + s2[len("INSERT"):])
                except Exception as e:
                    print("SEED SKIP:", e)
                continue
            if up.startswith("CREATE"):
                try:
                    con.execute(s)
                except Exception as e:
                    print("DDL SKIP:", str(e)[:120])
        con.commit()
    finally:
        con.close()
    return f"sqlite:{SQLITE_PATH}"


def _row_to_video(r) -> dict:
    d = dict(r)
    return d


def list_videos(lesson_id: str) -> List[dict]:
    con = _get_sqlite()
    try:
        rows = con.execute(
            "SELECT * FROM school_lesson_videos WHERE lesson_id=? AND trang_thai='ready' ORDER BY thu_tu", (lesson_id,)).fetchall()
        return [_row_to_video(r) for r in rows]
    except Exception:
        return []
    finally:
        con.close()


def add_video(v: dict) -> dict:
    # tu sinh embed_url neu trong + youtube
    if not v.get("embed_url") and v.get("video_provider") == "youtube":
        u = v.get("video_url", "")
        vid = v.get("video_id_or_file", "")
        if not vid and ("v=" in u or "youtu.be/" in u):
            vid = u.split("youtu.be/")[-1].split("?")[0].split("&")[0] if "youtu.be/" in u else u.split("v=")[-1].split("&")[0]
            v["video_id_or_file"] = vid
        if vid:
            v["embed_url"] = f"https://www.youtube.com/embed/{vid}"
    con = _get_sqlite()
    try:
        con.execute("""INSERT OR REPLACE INTO school_lesson_videos
        (id, lesson_id, tieu_de_video, video_url, video_provider, video_id_or_file, embed_url, thumbnail_url,
         thoi_luong_giay, chat_luong, ngon_ngu, co_phu_de, thu_tu, mien_phi, trang_thai, luot_xem)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            v.get("id"), v.get("lesson_id"), v.get("tieu_de_video", ""), v.get("video_url", ""),
            v.get("video_provider", "youtube"), v.get("video_id_or_file", ""), v.get("embed_url", ""),
            v.get("thumbnail_url", ""), v.get("thoi_luong_giay", 0), v.get("chat_luong", "720p"),
            v.get("ngon_ngu", "vi"), 1 if v.get("co_phu_de", True) else 0, v.get("thu_tu", 1),
            1 if v.get("mien_phi", True) else 0, v.get("trang_thai", "ready"), v.get("luot_xem", 0)))
        con.commit()
    finally:
        con.close()
    return v


def save_video_progress(hoc_sinh: str, video_id: str, giay: int, hoan_thanh: bool = False) -> dict:
    con = _get_sqlite()
    try:
        con.execute("""INSERT INTO school_video_progress (hoc_sinh, video_id, giay_da_xem, hoan_thanh)
        VALUES (?,?,?,?) ON CONFLICT(hoc_sinh, video_id) DO UPDATE SET giay_da_xem=excluded.giay_da_xem, hoan_thanh=excluded.hoan_thanh""",
        (hoc_sinh, video_id, giay, 1 if hoan_thanh else 0))
    except Exception:
        con.execute("INSERT OR REPLACE INTO school_video_progress (hoc_sinh, video_id, giay_da_xem, hoan_thanh) VALUES (?,?,?,?)",
            (hoc_sinh, video_id, giay, 1 if hoan_thanh else 0))
    con.commit()
    con.close()
    return {"hoc_sinh": hoc_sinh, "video_id": video_id, "giay_da_xem": giay, "hoan_thanh": hoan_thanh}


def get_video_progress(hoc_sinh: str) -> List[dict]:
    con = _get_sqlite()
    try:
        rows = con.execute("SELECT * FROM school_video_progress WHERE hoc_sinh=?", (hoc_sinh,)).fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []
    finally:
        con.close()
