-- ==========================================================
-- PentaSchool: BANG VIDEO BAI GIANG (003)
-- Nguyen tac: DB CHI CHUA LINK, khong chua file video.
-- File video nam tren YouTube / S3 / CDN, DB chi luu URL + metadata.
-- Tuong thich PostgreSQL (production) — ban dev SQLite tu map o db.py
-- ==========================================================

-- 1. Bang bai hoc mo rong (neu chua co, tao moi; neu co, alter)
CREATE TABLE IF NOT EXISTS school_lessons (
    id VARCHAR(64) PRIMARY KEY,
    mon VARCHAR(32) NOT NULL,              -- toan, ngu_van, tieng_anh...
    lop INT NOT NULL CHECK (lop BETWEEN 1 AND 12),
    tieu_de TEXT NOT NULL,
    muc_tieu TEXT DEFAULT '',
    noi_dung TEXT DEFAULT '',
    thu_tu INT DEFAULT 1,
    do_kho INT DEFAULT 1 CHECK (do_kho BETWEEN 1 AND 3),
    thoi_luong_phut INT DEFAULT 15,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_lessons_lop ON school_lessons(lop);
CREATE INDEX IF NOT EXISTS idx_lessons_mon ON school_lessons(mon);

-- 2. BANG VIDEO BAI GIANG — chi chua link
CREATE TABLE IF NOT EXISTS school_lesson_videos (
    id VARCHAR(64) PRIMARY KEY,            -- vd: vid_lop1_cong_01
    lesson_id VARCHAR(64) NOT NULL REFERENCES school_lessons(id) ON DELETE CASCADE,
    tieu_de_video TEXT NOT NULL,           -- ten hien thi: "Co giang phep cong (5 phut)"
    -- LINK VIDEO (khong luu blob):
    video_url TEXT NOT NULL,               -- URL goc: https://youtube.com/watch?v=... / https://cdn.../video.mp4 / s3://...
    video_provider VARCHAR(16) NOT NULL DEFAULT 'youtube',
                                           -- youtube | mp4 | s3 | vimeo | drive
    video_id_or_file VARCHAR(255) DEFAULT '', -- youtube_id (dQw4w9WgXcQ) hoac object_key S3
    embed_url TEXT DEFAULT '',             -- URL nhung iframe, backend tu sinh
    thumbnail_url TEXT DEFAULT '',         -- anh bia (link CDN, khong blob)
    thoi_luong_giay INT DEFAULT 0,         -- duration de hien "5:30"
    chat_luong VARCHAR(16) DEFAULT '720p', -- 480p | 720p | 1080p
    ngon_ngu VARCHAR(8) DEFAULT 'vi',      -- vi | en | song_ngu
    co_phu_de BOOLEAN DEFAULT TRUE,        -- co subtitle khong
    thu_tu INT DEFAULT 1,                  -- video 1, 2, 3 trong 1 bai
    mien_phi BOOLEAN DEFAULT TRUE,         -- free hay premium
    trang_thai VARCHAR(16) DEFAULT 'ready',-- draft | ready | hidden
    luot_xem INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_videos_lesson ON school_lesson_videos(lesson_id);
CREATE INDEX IF NOT EXISTS idx_videos_provider ON school_lesson_videos(video_provider);

-- 3. Tien do xem video (de resume + thuong sao)
CREATE TABLE IF NOT EXISTS school_video_progress (
    hoc_sinh VARCHAR(64) NOT NULL,
    video_id VARCHAR(64) NOT NULL REFERENCES school_lesson_videos(id) ON DELETE CASCADE,
    giay_da_xem INT DEFAULT 0,
    hoan_thanh BOOLEAN DEFAULT FALSE,
    cap_nhat TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (hoc_sinh, video_id)
);

-- 4. Seed vi du: 1 bai co 2 video (link mau, thay bang link that khi co)
INSERT INTO school_lessons (id, mon, lop, tieu_de, muc_tieu, noi_dung, do_kho, thoi_luong_phut) VALUES
('lop1-toan-cong','toan',1,'Lam quen phep cong pham vi 10','Biet gop 2 nhom do vat','3 tao + 2 tao = 5 tao.',1,10),
('lop9-toan-ptbac2','toan',9,'Phuong trinh bac hai mot an','Tinh delta va tim nghiem','ax^2+bx+c=0. Delta=b^2-4ac.',3,20)
ON CONFLICT (id) DO NOTHING;

INSERT INTO school_lesson_videos (id, lesson_id, tieu_de_video, video_url, video_provider, video_id_or_file, embed_url, thumbnail_url, thoi_luong_giay, thu_tu) VALUES
('vid_cong_01','lop1-toan-cong','Co giang: gop tao (4 phut)','https://www.youtube.com/watch?v=PLACEHOLDER_LOP1','youtube','PLACEHOLDER_LOP1','https://www.youtube.com/embed/PLACEHOLDER_LOP1','','240',1),
('vid_ptbac2_01','lop9-toan-ptbac2','Thay giang: Delta va nghiem (12 phut)','https://www.youtube.com/watch?v=PLACEHOLDER_LOP9','youtube','PLACEHOLDER_LOP9','https://www.youtube.com/embed/PLACEHOLDER_LOP9','','720',1)
ON CONFLICT (id) DO NOTHING;
