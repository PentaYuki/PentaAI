"""PentaSchool backend — LMS K12 (lop 1-12), 3 theme theo cap."""
from pathlib import Path
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

CUR = Path(__file__).resolve().parent
ROOT = CUR.parent.parent.parent
sys.path.insert(0, str(ROOT))

from pentaschool.backend.api import catalog, learning, tutor, videos
from pentaschool.backend.infrastructure.db import init_db

app = FastAPI(title="PentaSchool LMS K12", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"])

DB_INFO = init_db()

@app.get("/api/health")
def health():
    return {"ok": True, "app": "pentaschool", "lop": "1-12", "themes": ["tieu_hoc", "thcs", "thpt"], "db": DB_INFO}

app.include_router(catalog.router, prefix="/api/school")
app.include_router(learning.router, prefix="/api/school")
app.include_router(videos.router, prefix="/api/school")
app.include_router(tutor.router, prefix="/api/tutor")

FRONT = CUR.parent / "frontend"
if FRONT.exists():
    # static theo cau truc moi: core / modules / themes
    for sub in ["css", "js"]:
        d = FRONT / sub
        if d.exists():
            app.mount(f"/{sub}", StaticFiles(directory=str(d)), name=sub)

@app.get("/")
def index():
    f = FRONT / "index.html"
    if f.exists():
        return FileResponse(str(f))
    return {"msg": "PentaSchool backend OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
