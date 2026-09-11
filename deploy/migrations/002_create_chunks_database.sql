-- ==========================================================
-- PENTA AI ECOSYSTEM - 3D CHUNK DATABASE SCHEMA (PRE-CREATED)
-- Chuyên biệt lưu trữ: chunk_emo, chunk_time, chunk_action
-- Trạng thái hiện tại: Đã tạo sẵn bảng, tạm dừng kích hoạt runtime (ENABLE_3D_CHUNKS=false)
-- ==========================================================

-- 1. Bảng Quản Lý Phiên Streaming Tổng Thể
CREATE TABLE IF NOT EXISTS stream_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    app_source VARCHAR(32) NOT NULL DEFAULT 'pentami-core',
    is_3d_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stream_sessions_tenant ON stream_sessions(tenant_id);

-- 2. Bảng Tổng Hợp Stream Chunks
CREATE TABLE IF NOT EXISTS stream_chunks (
    chunk_id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL REFERENCES stream_sessions(session_id) ON DELETE CASCADE,
    message_id VARCHAR(64) NOT NULL,
    tenant_id VARCHAR(64) NOT NULL,
    chunk_index INT NOT NULL,
    chunk_type VARCHAR(20) NOT NULL, -- 'text', 'emo', 'time', 'action', 'status'
    content TEXT,
    is_paused BOOLEAN DEFAULT TRUE,  -- Đánh dấu trạng thái tạm dừng
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stream_chunks_session ON stream_chunks(session_id);
CREATE INDEX IF NOT EXISTS idx_stream_chunks_type ON stream_chunks(chunk_type);
CREATE INDEX IF NOT EXISTS idx_stream_chunks_tenant ON stream_chunks(tenant_id);

-- 3. Bảng Chi Tiết Cảm Xúc (chunk_emo)
CREATE TABLE IF NOT EXISTS chunk_emo_records (
    id VARCHAR(64) PRIMARY KEY,
    chunk_id VARCHAR(64) NOT NULL REFERENCES stream_chunks(chunk_id) ON DELETE CASCADE,
    sentiment VARCHAR(32) NOT NULL DEFAULT 'neutral', -- positive, negative, neutral, inquisitive
    target_tone VARCHAR(32) NOT NULL DEFAULT 'friendly', -- cute, serious, yandere, encouraging
    intensity NUMERIC(3, 2) NOT NULL DEFAULT 0.50,
    avatar_blendshapes JSONB DEFAULT '{}'::jsonb, -- Dữ liệu viseme ARKit cho cử động mặt 3D
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunk_emo_chunk_id ON chunk_emo_records(chunk_id);

-- 4. Bảng Chi Tiết Đồng Bộ Thời Gian & Lip-Sync (chunk_time)
CREATE TABLE IF NOT EXISTS chunk_time_records (
    id VARCHAR(64) PRIMARY KEY,
    chunk_id VARCHAR(64) NOT NULL REFERENCES stream_chunks(chunk_id) ON DELETE CASCADE,
    audio_start_ms INT NOT NULL DEFAULT 0,
    audio_end_ms INT NOT NULL DEFAULT 0,
    phoneme_sequence VARCHAR(255) DEFAULT '',
    audio_offset_sec NUMERIC(6, 3) DEFAULT 0.000,
    temporal_decay_factor NUMERIC(4, 3) DEFAULT 0.050,
    time_context VARCHAR(32) DEFAULT 'realtime_session',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunk_time_chunk_id ON chunk_time_records(chunk_id);

-- 5. Bảng Hàng Đợi Hành Động Playwright & Client Events (chunk_action)
CREATE TABLE IF NOT EXISTS chunk_action_records (
    id VARCHAR(64) PRIMARY KEY,
    chunk_id VARCHAR(64) NOT NULL REFERENCES stream_chunks(chunk_id) ON DELETE CASCADE,
    action_type VARCHAR(64) NOT NULL, -- 'playwright_click', 'navigate', 'apply_voucher', 'open_note'
    target_subsystem VARCHAR(32) NOT NULL, -- 'mcp_playwright', 'pentaschool', 'pentamarket'
    tool_to_invoke VARCHAR(64),
    action_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    require_user_confirmation BOOLEAN DEFAULT TRUE,
    execution_status VARCHAR(32) NOT NULL DEFAULT 'paused', -- 'paused', 'pending', 'confirmed', 'executed', 'failed'
    executed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunk_action_chunk_id ON chunk_action_records(chunk_id);
CREATE INDEX IF NOT EXISTS idx_chunk_action_status ON chunk_action_records(execution_status);
