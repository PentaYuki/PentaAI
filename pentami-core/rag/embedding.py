"""
Penta RAG Service - Embedding & Vector Retrieval Engine
Mô hình embedding: sentence-transformers/all-MiniLM-L6-v2 (384 chiều)
Vector Database: Qdrant với Payload Filtering theo tenant_id và app_id.
"""

from typing import Any, Dict, List, Optional
import math
import random

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class MiniLMEmbeddingService:
    """
    Quản lý mô hình sentence-transformers/all-MiniLM-L6-v2.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                # Fallback mock embedding for development without torch/transformers installed
                self._model = "mock"

    def embed_text(self, text: str) -> List[float]:
        """
        Vector hóa một đoạn văn bản thành vector 384 chiều.
        """
        self._load_model()
        if self._model == "mock":
            if HAS_NUMPY:
                rng = np.random.default_rng(abs(hash(text)) % (2**32))
                vec = rng.standard_normal(384).astype(np.float32)
                vec /= np.linalg.norm(vec)
                return vec.tolist()
            else:
                # Thuần Python không cần thư viện ngoài
                random.seed(abs(hash(text)) % (2**32))
                raw_vec = [random.gauss(0, 1) for _ in range(384)]
                norm = math.sqrt(sum(x * x for x in raw_vec))
                return [x / norm for x in raw_vec]
        
        vector = self._model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Vector hóa hàng loạt văn bản với tốc độ tối ưu.
        """
        self._load_model()
        if self._model == "mock":
            return [self.embed_text(t) for t in texts]
        
        vectors = self._model.encode(texts, batch_size=32, normalize_embeddings=True)
        return [v.tolist() for v in vectors]


class PentaVectorStore:
    """
    Client kết nối Qdrant Vector DB, thực thi tìm kiếm ngữ nghĩa cô lập theo Tenant và App.
    """
    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "penta_knowledge"):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.embedder = MiniLMEmbeddingService()

    def build_qa_document(
        self,
        tenant_id: str,
        app_id: str,
        doc_id: str,
        question: str,
        answer: str,
        source_context: str = "",
        extra_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Đóng gói một cặp Q&A với vector embedding và metadata phân quyền.
        """
        combined_text = f"Câu hỏi: {question}\nTrả lời: {answer}"
        vector = self.embedder.embed_text(combined_text)

        payload = {
            "tenant_id": tenant_id,
            "app_id": app_id, # "pentaschool", "pentamarket", "pentakuru", "pentajob"
            "doc_id": doc_id,
            "question": question,
            "answer": answer,
            "source_context": source_context,
            "metadata": extra_metadata or {}
        }

        return {
            "id": doc_id,
            "vector": vector,
            "payload": payload
        }
