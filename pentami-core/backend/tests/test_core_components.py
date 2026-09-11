"""
Bộ kiểm thử tính toàn vẹn của các thành phần hạt nhân trong Hệ Sinh Thái Penta AI.
"""

import sys
from pathlib import Path

# Thêm thư mục gốc và thư mục backend vào PYTHONPATH
BACKEND_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BACKEND_DIR.parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(ROOT_DIR / "pentami-core"))

from shared.protocol.chunks import (
    PentaStreamEnvelope,
    ChunkType,
    EmotionType,
    ChunkEmoData,
    ChunkTimeData,
    ChunkActionData,
)
from shared.auth.key_manager import UnifiedKeyManager
from rag.embedding import MiniLMEmbeddingService, PentaVectorStore


def test_chunk_protocol():
    print("[TEST] Testing 3D Chunk Protocol...")
    envelope = PentaStreamEnvelope(
        seq=1,
        session_id="sess_test_123",
        type=ChunkType.EMO,
        emo=ChunkEmoData(
            emotion=EmotionType.ENCOURAGING,
            intensity=0.9,
            gesture="head_nod"
        )
    )
    json_data = envelope.model_dump_json()
    assert "encouraging" in json_data
    assert "sess_test_123" in json_data

    # Test action chunk
    action_env = PentaStreamEnvelope(
        seq=2,
        session_id="sess_test_123",
        type=ChunkType.ACTION,
        action=ChunkActionData(
            action_id="act_001",
            target_system="pentaschool",
            command="open_course",
            params={"course_id": "cs101"}
        )
    )
    assert action_env.action.command == "open_course"
    print("  -> Chunk Protocol PASSED!")


def test_key_manager_and_scopes():
    print("[TEST] Testing Unified Key Manager & Scopes...")
    km = UnifiedKeyManager(master_secret="test_secret_key_123")
    raw_key, hashed_key = km.generate_key(environment="live", key_type="sk")
    
    assert raw_key.startswith("penta_live_sk_")
    assert len(hashed_key) == 64 # SHA-256 hex string
    
    # Hash check
    assert km.hash_key(raw_key) == hashed_key
    
    # Scope check
    user_scopes = ["penta:school:*", "penta:market:read"]
    assert km.has_required_scopes(user_scopes, ["penta:school:view_lecture"]) is True
    assert km.has_required_scopes(user_scopes, ["penta:market:read"]) is True
    assert km.has_required_scopes(user_scopes, ["penta:job:apply"]) is False
    
    # Wildcard super admin check
    admin_scopes = ["*"]
    assert km.has_required_scopes(admin_scopes, ["penta:job:apply", "action:playwright:execute"]) is True
    print("  -> Unified Key Manager & Scopes PASSED!")


def test_rag_embedding():
    print("[TEST] Testing MiniLM Embedding Service (384 dimensions)...")
    service = MiniLMEmbeddingService()
    vec = service.embed_text("Xin chào, đây là bài kiểm tra embedding cho Penta AI.")
    assert len(vec) == 384
    
    store = PentaVectorStore()
    doc = store.build_qa_document(
        tenant_id="tenant_penta_vn",
        app_id="pentaschool",
        doc_id="qa_001",
        question="Học phí khóa học là bao nhiêu?",
        answer="Khóa học hoàn toàn miễn phí cho học viên Penta."
    )
    assert doc["id"] == "qa_001"
    assert len(doc["vector"]) == 384
    assert doc["payload"]["app_id"] == "pentaschool"
    print("  -> MiniLM Embedding & Q&A Document Build PASSED!")


if __name__ == "__main__":
    test_chunk_protocol()
    test_key_manager_and_scopes()
    test_rag_embedding()
    print("\n🎉 ALL CORE COMPONENT TESTS PASSED SUCCESSFULLY!")
