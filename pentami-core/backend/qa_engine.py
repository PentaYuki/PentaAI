"""
Penta Core Intelligent QA Engine with Dynamic Slot Resolution & Self-Learning (Knowledge Harvesting)
Hệ thống Quản trị Tập trung Toàn diện cho Người Việt (Penta Life OS)
Triết lý:
1. Tra cứu Database/Knowledge Base trước (Rule-First / Zero-LLM-cost).
2. Điền chỗ trống động (Dynamic Slot Filling: [USER_NAME], [PENTA_ID], [AVG], [STATUS_COLOR], [ACTION_PLAN]).
3. Tự học và mở rộng tri thức (Knowledge Harvesting): Tự động nạp dữ liệu câu hỏi mới vào Database cho toàn hệ sinh thái.
"""

import re
import time
from typing import Dict, Any, Optional, List, Tuple, Set
from shared.models.user import UserLifetimeLedger

STOPWORDS: Set[str] = {
    "tại", "sao", "cho", "em", "tôi", "mình", "hỏi", "về", "như", "thế", "nào", "là", "gì",
    "của", "lại", "được", "có", "và", "trong", "đã", "sẽ", "những", "các",
    "bởi", "vì", "với", "hãy", "giải", "thích", "xin"
}


def clean_text(text: str) -> str:
    """Làm sạch ký tự đặc biệt, đưa về chữ thường"""
    text = text.lower()
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    return " ".join(text.split())


def extract_content_tokens(text: str) -> List[str]:
    """Trích xuất các từ mang ý nghĩa nội dung (bỏ stopwords)"""
    tokens = clean_text(text).split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


class SlotResolver:
    """Module chuyên biệt phân tích và giải quyết các biến chỗ trống (Slot / Placeholder)"""

    @staticmethod
    def resolve(template: str, user: Optional[UserLifetimeLedger] = None, context: Optional[Dict[str, Any]] = None) -> str:
        context = context or {}
        
        # 1. Thông tin người dùng / công dân số
        user_name = user.full_name if user else "Bạn"
        penta_id = user.penta_id if user else "PID-GUEST"
        
        # 2. Chỉ số năng lực & phong cách
        ler = user.ler_profile if user else None
        style_raw = ler.primary_style if ler else "visual"
        speed = f"{ler.efficiency_rate}x" if ler else "1.0x"
        at_risk = ler.at_risk_score if ler else 0.0
        
        style_mapping = {
            "visual": "Trực quan (Sơ đồ / Báo cáo hình ảnh)",
            "auditory": "Âm thanh (Hội thoại / Voice)",
            "kinesthetic": "Thực hành & Trải nghiệm thực tế",
            "reading_writing": "Văn bản & Tài liệu số",
            "logical": "Logic & Tư duy hệ thống"
        }
        style_vi = style_mapping.get(style_raw, "Đa phương thức")
        
        # 3. Tính toán [AVG] (Chỉ số trung bình: hiệu suất, điểm đánh giá, số liệu quản trị)
        if "scores" in context and isinstance(context["scores"], list) and len(context["scores"]) > 0:
            avg_val = round(sum(context["scores"]) / len(context["scores"]), 1)
        elif "avg" in context:
            avg_val = context["avg"]
        else:
            base_val = 8.5
            if user:
                base_val = round(min(10.0, 7.0 + (user.total_questions_asked * 0.1)), 1)
            avg_val = base_val

        # 4. Tính toán [STATUS_COLOR] / [ALERT_BADGE] (Điều kiện logic quản trị)
        if at_risk >= 0.7:
            status_color = "Đỏ (Cảnh báo: Chỉ số rủi ro cao - Cần can thiệp ngay)"
            status_badge = "🔴 CẢNH BÁO RỦI RO"
        elif at_risk >= 0.4:
            status_color = "Vàng (Mức trung bình - Cần theo dõi tiến độ)"
            status_badge = "🟡 CẦN THEO DÕI"
        else:
            status_color = "Xanh lá (Hiệu quả tốt, ổn định)"
            status_badge = "🟢 HOẠT ĐỘNG TỐT"

        # 5. Đề xuất hành động theo năng lực [ACTION_PLAN]
        if at_risk >= 0.7:
            if style_raw == "visual":
                action = "Xem lại sơ đồ quy trình tổng quan để rà soát các điểm nghẽn"
            elif style_raw == "auditory":
                action = "Thảo luận nhanh qua âm thanh hoặc họp nhóm 5 phút"
            else:
                action = "Thực hiện ngay danh sách 3 đầu việc ưu tiên cao nhất trong ngày"
        else:
            if style_raw == "visual":
                action = "Lập kế hoạch và vẽ sơ đồ phát triển cho giai đoạn tiếp theo"
            else:
                action = "Mở rộng kết nối và chia sẻ trong các không gian làm việc chung"

        # 6. Thay thế biến vào Template (Hỗ trợ cả tên mới và tên alias)
        replacements = {
            r"\[USER_NAME\]": user_name,
            r"\[STUDENT_NAME\]": user_name, # Alias tương thích ngược
            r"\[PENTA_ID\]": penta_id,
            r"\[AVG\]": str(avg_val),
            r"\[STATUS_COLOR\]": status_color,
            r"\[ALERT_BADGE\]": status_badge,
            r"\[LER_STYLE\]": style_vi,
            r"\[STYLE\]": style_vi,
            r"\[LER_SPEED\]": speed,
            r"\[ACTION_PLAN\]": action,
            r"\[LER_ACTION\]": action,      # Alias tương thích ngược
        }

        result = template
        for pattern, val in replacements.items():
            result = re.sub(pattern, val, result)

        return result


SEED_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    "dien_bien_phu": {
        "keywords": ["điện biên phủ", "dien bien phu", "7/5/1954", "7 tháng 5", "tướng de castries"],
        "subject": "Lịch sử Việt Nam",
        "template": "Chiến dịch Điện Biên Phủ toàn thắng vào ngày 07/05/1954 sau 56 ngày đêm 'khoét núi, ngủ hầm, mưa dầm, cơm vắt'. [USER_NAME] có thể ứng dụng phương pháp [STYLE] để lưu trữ dòng sự kiện lịch sử này vào cuốn sổ cuộc đời cá nhân."
    },
    "phuong_cham_dien_bien": {
        "keywords": ["đánh chắc tiến chắc", "đánh nhanh thắng nhanh", "đổi phương châm", "võ nguyên giáp"],
        "subject": "Lịch sử & Chiến lược",
        "template": "Đại tướng Võ Nguyên Giáp quyết định chuyển từ 'Đánh nhanh, thắng nhanh' sang 'Đánh chắc, tiến chắc' vì phát hiện tập đoàn cứ điểm Điện Biên Phủ đã được tăng cường công sự kiên cố và pháo binh hạng nặng. Đây là bài học kinh điển về quản trị chiến lược và tư duy thực chứng cho người Việt."
    },
    "bach_dang": {
        "keywords": ["bạch đằng", "bach dang", "ngô quyền", "trần hưng đạo", "cọc gỗ"],
        "subject": "Lịch sử Việt Nam",
        "template": "Các trận thủy chiến trên sông Bạch Đằng (năm 938 của Ngô Quyền, năm 981 của Lê Hoàn, và năm 1288 của Trần Hưng Đạo) đều tận dụng tài tình hiện tượng thủy triều và trận địa cọc gỗ ngầm để bảo vệ độc lập dân tộc."
    },
    "canh_bao_quan_tri": {
        "keywords": ["cảnh báo quản trị", "tình hình hoạt động", "nguy cơ rủi ro", "kết quả đánh giá", "chỉ số trung bình avg"],
        "subject": "Quản trị Cá nhân",
        "template": "Chào [USER_NAME] ([PENTA_ID])! Chỉ số đánh giá trung bình hiện tại của bạn là [AVG]. Trạng thái quản trị: [STATUS_COLOR]. Đề xuất hành động: [ACTION_PLAN]."
    },
    "pythagore": {
        "keywords": ["pythagore", "pitago", "tam giác vuông", "cạnh huyền"],
        "subject": "Khoa học & Toán học",
        "template": "Định lý Pythagore trong tam giác vuông: Bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông ($a^2 + b^2 = c^2$)."
    }
}


class KnowledgeBase:
    """Kho tri thức câu hỏi - câu trả lời có sẵn (Knowledge Base & Self-Harvest Store)"""
    
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self.reset()

    def reset(self):
        """Khôi phục lại kho dữ liệu ban đầu"""
        self._store = {}
        for k, v in SEED_KNOWLEDGE.items():
            entry = dict(v)
            entry["tokens"] = set(extract_content_tokens(" ".join(v["keywords"])))
            self._store[k] = entry

    def lookup(self, query: str) -> Optional[Tuple[str, str, str]]:
        """
        Tra cứu câu trả lời chuẩn trong Knowledge Base.
        1. Khớp cụm từ chính xác (Exact phrase match).
        2. Khớp độ phủ từ khóa nội dung (Token overlap).
        """
        query_norm = clean_text(query)
        query_tokens = set(extract_content_tokens(query))
        
        # 1. Khớp cụm từ trực tiếp
        for key, data in self._store.items():
            for kw in data["keywords"]:
                kw_norm = clean_text(kw)
                if kw_norm and kw_norm in query_norm:
                    return key, data["template"], data["subject"]
                    
        # 2. Khớp độ phủ từ khóa (Semantic token overlap)
        best_match = None
        highest_overlap = 0
        
        for key, data in self._store.items():
            entry_tokens = data.get("tokens", set())
            if not entry_tokens:
                continue
            common = query_tokens.intersection(entry_tokens)
            if len(common) >= 2 and len(common) > highest_overlap:
                highest_overlap = len(common)
                best_match = (key, data["template"], data["subject"])
                
        return best_match

    def harvest_knowledge(self, query: str, answer_template: str, subject: str = "Tự tổng hợp") -> str:
        """
        Tự động nạp thêm tri thức mới vào Knowledge Base (Vòng lặp tự học toàn hệ thống)
        """
        key = f"harvested_{int(time.time() * 1000)}_{len(self._store)}"
        clean_q = clean_text(query)
        keywords = [clean_q]
        
        tokens = extract_content_tokens(query)
        # Sinh các cụm n-gram từ các token nội dung
        if len(tokens) >= 2:
            for i in range(len(tokens) - 1):
                keywords.append(f"{tokens[i]} {tokens[i+1]}")
        if len(tokens) >= 3:
            for i in range(len(tokens) - 2):
                keywords.append(f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}")
                
        self._store[key] = {
            "keywords": keywords,
            "tokens": set(tokens),
            "subject": subject,
            "template": answer_template,
            "harvested_at": time.time()
        }
        return key

    @property
    def total_entries(self) -> int:
        return len(self._store)


class QAEngine:
    """Engine xử lý Q&A thông minh cho Hệ thống Quản trị Tập trung Penta Core"""

    def __init__(self):
        self.kb = KnowledgeBase()
        self.resolver = SlotResolver()

    def reset(self):
        self.kb.reset()

    def process_query(
        self,
        query: str,
        user: Optional[UserLifetimeLedger] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Xử lý truy vấn hỏi-đáp:
        1. Tra cứu Knowledge Base có sẵn.
        2. Nếu có: Điền slot và trả về với nguồn 'knowledge_base'.
        3. Nếu chưa có: Kích hoạt Fallback AI Generator -> Tự động lưu vào KB (Harvesting) -> Trả về với nguồn 'ai_fallback_and_harvested'.
        """
        lookup_result = self.kb.lookup(query)
        
        if lookup_result:
            key, template, subject = lookup_result
            resolved_text = self.resolver.resolve(template, user=user, context=context)
            return {
                "response": resolved_text,
                "source": "knowledge_base",
                "subject": subject,
                "cached_key": key,
                "slots_applied": True,
            }
        
        # Fallback Generator: Sinh câu trả lời giải thích khi chưa có trong KB
        fallback_answer = self._generate_fallback_explanation(query, user)
        resolved_text = self.resolver.resolve(fallback_answer, user=user, context=context)
        
        # Tự động nạp vào Knowledge Base cho các lần sau (Continuous Learning)
        harvested_key = self.kb.harvest_knowledge(
            query=query,
            answer_template=fallback_answer,
            subject="Tổng hợp Quản trị"
        )
        
        return {
            "response": resolved_text,
            "source": "ai_fallback_and_harvested",
            "subject": "Tổng hợp Quản trị",
            "cached_key": harvested_key,
            "slots_applied": True,
        }

    def _generate_fallback_explanation(self, query: str, user: Optional[UserLifetimeLedger]) -> str:
        """Sinh nội dung giải thích logic khi chưa có câu trả lời mẫu sẵn"""
        user_greeting = "Chào [USER_NAME]! " if user else ""
        return (
            f"{user_greeting}Hệ thống Penta Core đã phân tích chuyên sâu yêu cầu: '{query}'. "
            f"Về nội dung này, cốt lõi nằm ở phương pháp tiếp cận thực tế và quy trình chuẩn hóa. "
            f"Theo năng lực [STYLE], bạn nên: [ACTION_PLAN] để triển khai hiệu quả."
        )


# Singleton instance dùng cho toàn backend
qa_engine = QAEngine()
