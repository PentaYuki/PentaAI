"""
Penta Core Intelligent QA & Multi-Domain Intent Routing Engine
Hệ thống Quản trị Tập trung Toàn diện cho Người Việt (Penta Life OS)
Phân hệ Trường học (Pentaschool) chỉ là một phần nhỏ; Core định tuyến chính xác đến:
- Pentaschool (Học tập & Giáo dục K12/ĐH)
- PentaJob (Nghề nghiệp, Tuyển dụng, CV, Sự nghiệp)
- PentaMarket (Thương mại, Mua bán học liệu, Giao dịch số)
- Pentanote (Ghi chép số, Sổ tay, Flashcard, Ý tưởng)
- PentaKuRu (Quản trị tài liệu PC, Desktop Assistant)
- MCP Playwright (Tự động hóa Web)
- Pentami Core (Quản trị cuộc đời tập trung, Bản sắc xã hội & Bản sắc Việt Nam)
"""

import re
import time
from typing import Dict, Any, Optional, List, Tuple, Set
from shared.models.user import UserLifetimeLedger

STOPWORDS: Set[str] = {
    "tại", "sao", "cho", "em", "tôi", "mình", "hỏi", "về", "như", "thế", "nào", "là", "gì",
    "của", "lại", "được", "có", "và", "trong", "đã", "sẽ", "những", "các",
    "bởi", "vì", "với", "hãy", "giải", "thích", "xin", "cần", "muốn"
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


class IntentRouter:
    """Bộ định tuyến ý định thông minh tới các phân hệ chuyên biệt trong Hệ sinh thái Penta"""

    @staticmethod
    def route(query: str) -> str:
        q = clean_text(query)
        
        # 1. Định tuyến Giáo dục / Học tập -> Pentaschool
        if any(k in q for k in [
            "học", "bài tập", "toán", "vật lý", "hóa học", "lịch sử", "văn học",
            "sinh học", "tiếng anh", "lms", "k12", "thi cử", "bài giảng",
            "điện biên phủ", "bạch đằng", "pythagore", "đạo hàm", "phương trình"
        ]):
            return "pentaschool"
            
        # 2. Định tuyến Nghề nghiệp / Tuyển dụng -> PentaJob
        elif any(k in q for k in [
            "cv", "việc làm", "tuyển dụng", "phỏng vấn", "lương", "job", "career",
            "nghề nghiệp", "sự nghiệp", "ứng tuyển", "nhân sự", "deal lương",
            "kinh nghiệm làm việc", "hồ sơ năng lực"
        ]):
            return "pentajob"
            
        # 3. Định tuyến Thương mại / Mua sắm / Giá cả -> PentaMarket
        elif any(k in q for k in [
            "giá", "mua", "bán", "thanh toán", "tiền", "voucher", "market", "chợ",
            "học phí", "hóa đơn", "giao dịch", "đơn hàng", "giảm giá", "sàn"
        ]):
            return "pentamarket"
            
        # 4. Định tuyến Ghi chép / Sổ tay / Ý tưởng -> Pentanote
        elif any(k in q for k in [
            "note", "ghi chú", "sổ tay", "flashcard", "mindmap", "sơ đồ tư duy",
            "ý tưởng", "sổ cá nhân", "cornell", "nhật ký"
        ]):
            return "pentanote"
            
        # 5. Định tuyến Quản lý tệp tin PC / Desktop -> PentaKuRu
        elif any(k in q for k in [
            "file", "tài liệu", "pdf", "word", "excel", "máy tính", "kuru",
            "tìm file", "ổ cứng", "desktop", "thư mục", "docx"
        ]):
            return "pentakuru"
            
        # 6. Định tuyến Tự động hóa Web -> MCP Playwright
        elif any(k in q for k in [
            "web", "playwright", "tự động hóa", "click", "mở trang", "cào dữ liệu",
            "duyệt web", "crawl", "browser"
        ]):
            return "mcp_playwright"
            
        # 7. Mặc định -> Pentami Core (Quản trị cuộc đời trung tâm)
        return "pentami_core"


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
        
        # 3. Tính toán [AVG] (Chỉ số trung bình)
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

        # 6. Thay thế biến vào Template (Hỗ trợ cả tên mới và alias)
        replacements = {
            r"\[USER_NAME\]": user_name,
            r"\[STUDENT_NAME\]": user_name,
            r"\[PENTA_ID\]": penta_id,
            r"\[AVG\]": str(avg_val),
            r"\[STATUS_COLOR\]": status_color,
            r"\[ALERT_BADGE\]": status_badge,
            r"\[LER_STYLE\]": style_vi,
            r"\[STYLE\]": style_vi,
            r"\[LER_SPEED\]": speed,
            r"\[ACTION_PLAN\]": action,
            r"\[LER_ACTION\]": action,
        }

        result = template
        for pattern, val in replacements.items():
            result = re.sub(pattern, val, result)

        return result


# Kho tri thức định hướng đa phân hệ
SEED_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    # Phân hệ Pentaschool (Giáo dục / K12 / Đại học)
    "dien_bien_phu": {
        "keywords": ["điện biên phủ", "dien bien phu", "7/5/1954", "7 tháng 5", "tướng de castries"],
        "target_app": "pentaschool",
        "subject": "Lịch sử Việt Nam",
        "template": "Chiến dịch Điện Biên Phủ toàn thắng vào ngày 07/05/1954 sau 56 ngày đêm 'khoét núi, ngủ hầm, mưa dầm, cơm vắt'. [USER_NAME] có thể ứng dụng phương pháp [STYLE] để ghi nhớ các mốc sự kiện trong phân hệ Pentaschool."
    },
    "phuong_cham_dien_bien": {
        "keywords": ["đánh chắc tiến chắc", "đánh nhanh thắng nhanh", "đổi phương châm", "võ nguyên giáp"],
        "target_app": "pentaschool",
        "subject": "Lịch sử & Chiến lược",
        "template": "Đại tướng Võ Nguyên Giáp quyết định chuyển từ 'Đánh nhanh, thắng nhanh' sang 'Đánh chắc, tiến chắc' vì phát hiện tập đoàn cứ điểm Điện Biên Phủ đã được tăng cường công sự kiên cố và pháo binh hạng nặng. Đây là bài học kinh điển về quản trị chiến lược và tư duy thực chứng cho người Việt."
    },
    "bach_dang": {
        "keywords": ["bạch đằng", "bach dang", "ngô quyền", "trần hưng đạo", "cọc gỗ"],
        "target_app": "pentaschool",
        "subject": "Lịch sử Việt Nam",
        "template": "Các trận thủy chiến trên sông Bạch Đằng (năm 938 của Ngô Quyền, năm 981 của Lê Hoàn, và năm 1288 của Trần Hưng Đạo) đều tận dụng tài tình hiện tượng thủy triều và trận địa cọc gỗ ngầm để bảo vệ độc lập dân tộc."
    },
    "pythagore": {
        "keywords": ["pythagore", "pitago", "tam giác vuông", "cạnh huyền"],
        "target_app": "pentaschool",
        "subject": "Toán học",
        "template": "Định lý Pythagore trong tam giác vuông: Bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông ($a^2 + b^2 = c^2$)."
    },
    
    # Phân hệ PentaJob (Nghề nghiệp & Việc làm)
    "cv_template_job": {
        "keywords": ["viết cv", "mẫu cv", "chuẩn bị cv", "hồ sơ xin việc", "tuyển dụng"],
        "target_app": "pentajob",
        "subject": "Tuyển dụng & Việc làm",
        "template": "Chào [USER_NAME] ([PENTA_ID])! Để xây dựng CV nổi bật trên PentaJob, bạn nên làm nổi bật các cột mốc dự án thực tế và kỹ năng cốt lõi. Đề xuất: [ACTION_PLAN]."
    },
    "interview_tips": {
        "keywords": ["phỏng vấn xin việc", "kỹ năng phỏng vấn", "deal lương", "phỏng vấn lương"],
        "target_app": "pentajob",
        "subject": "Kỹ năng Phỏng vấn",
        "template": "Khi phỏng vấn xin việc, hãy áp dụng mô hình STAR (Tình huống, Nhiệm vụ, Hành động, Kết quả) để thuyết phục nhà tuyển dụng trên phân hệ PentaJob."
    },

    # Phân hệ Pentanote (Ghi chép & Sổ tay)
    "cornell_note": {
        "keywords": ["ghi chép cornell", "phương pháp ghi chép", "sổ tay thông minh", "làm flashcard"],
        "target_app": "pentanote",
        "subject": "Phương pháp Ghi chép",
        "template": "Phương pháp ghi chép Cornell chia trang giấy làm 3 phần: Cột gợi ý (từ khóa chính), Cột ghi chép (chi tiết nội dung) và Phần tóm tắt cuối trang. Pentanote đã tích hợp sẵn mẫu này."
    },

    # Phân hệ Pentami Core (Quản trị cá nhân tập trung)
    "canh_bao_quan_tri": {
        "keywords": ["cảnh báo quản trị", "tình hình hoạt động", "nguy cơ rủi ro", "kết quả đánh giá", "chỉ số trung bình avg"],
        "target_app": "pentami_core",
        "subject": "Quản trị Cá nhân",
        "template": "Chào [USER_NAME] ([PENTA_ID])! Chỉ số đánh giá trung bình hiện tại của bạn là [AVG]. Trạng thái quản trị: [STATUS_COLOR]. Đề xuất hành động: [ACTION_PLAN]."
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

    def lookup(self, query: str) -> Optional[Tuple[str, str, str, str]]:
        """
        Tra cứu câu trả lời chuẩn trong Knowledge Base.
        Trả về: (key, template, subject, target_app) hoặc None nếu chưa có.
        """
        query_norm = clean_text(query)
        query_tokens = set(extract_content_tokens(query))
        
        # 1. Khớp cụm từ trực tiếp
        for key, data in self._store.items():
            for kw in data["keywords"]:
                kw_norm = clean_text(kw)
                if kw_norm and kw_norm in query_norm:
                    return key, data["template"], data["subject"], data.get("target_app", "pentami_core")
                    
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
                best_match = (key, data["template"], data["subject"], data.get("target_app", "pentami_core"))
                
        return best_match

    def harvest_knowledge(self, query: str, answer_template: str, subject: str = "Tự tổng hợp", target_app: str = "pentami_core") -> str:
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
            "target_app": target_app,
            "subject": subject,
            "template": answer_template,
            "harvested_at": time.time()
        }
        return key

    @property
    def total_entries(self) -> int:
        return len(self._store)


class QAEngine:
    """Engine xử lý Q&A và Định tuyến Phân Hệ Tập Trung Penta Core"""

    def __init__(self):
        self.kb = KnowledgeBase()
        self.resolver = SlotResolver()
        self.router = IntentRouter()

    def reset(self):
        self.kb.reset()

    def process_query(
        self,
        query: str,
        user: Optional[UserLifetimeLedger] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Xử lý truy vấn hỏi-đáp và định tuyến phân hệ chính xác:
        1. Nhận diện phân hệ đích (Pentaschool, PentaJob, PentaMarket, Pentanote, PentaKuRu, Core).
        2. Tra cứu Knowledge Base có sẵn.
        3. Nếu có: Điền slot và trả về với nguồn 'knowledge_base'.
        4. Nếu chưa có: Kích hoạt Fallback AI Generator theo ngữ cảnh phân hệ -> Tự động lưu vào KB -> Trả về với nguồn 'ai_fallback_and_harvested'.
        """
        routed_app = self.router.route(query)
        lookup_result = self.kb.lookup(query)
        
        if lookup_result:
            key, template, subject, target_app = lookup_result
            resolved_text = self.resolver.resolve(template, user=user, context=context)
            return {
                "response": resolved_text,
                "target_app": target_app or routed_app,
                "source": "knowledge_base",
                "subject": subject,
                "cached_key": key,
                "slots_applied": True,
            }
        
        # Fallback Generator: Sinh câu trả lời định hướng theo phân hệ
        fallback_answer, subject = self._generate_fallback_explanation(query, user, routed_app)
        resolved_text = self.resolver.resolve(fallback_answer, user=user, context=context)
        
        # Tự động nạp vào Knowledge Base cho các lần sau (Continuous Learning)
        harvested_key = self.kb.harvest_knowledge(
            query=query,
            answer_template=fallback_answer,
            subject=subject,
            target_app=routed_app
        )
        
        return {
            "response": resolved_text,
            "target_app": routed_app,
            "source": "ai_fallback_and_harvested",
            "subject": subject,
            "cached_key": harvested_key,
            "slots_applied": True,
        }

    def _generate_fallback_explanation(
        self,
        query: str,
        user: Optional[UserLifetimeLedger],
        target_app: str
    ) -> Tuple[str, str]:
        """Sinh nội dung giải thích logic phù hợp với phân hệ được định tuyến"""
        user_greeting = "Chào [USER_NAME]! " if user else ""
        
        app_contexts = {
            "pentaschool": ("Học tập & Giáo dục K12/ĐH", "về nội dung học tập và bài giảng"),
            "pentajob": ("Nghề nghiệp & Việc làm", "về cơ hội việc làm, định hướng sự nghiệp và thị trường lao động"),
            "pentamarket": ("Thương mại & Học liệu", "về giao dịch, định giá tài nguyên và học liệu số"),
            "pentanote": ("Ghi chép & Tri thức cá nhân", "về hệ thống ghi chú và quản trị ý tưởng"),
            "pentakuru": ("Quản trị Dữ liệu PC", "về tài liệu, tệp tin và tìm kiếm trên máy tính"),
            "mcp_playwright": ("Tự động hóa Trình duyệt", "về quy trình tự động hóa và thao tác web"),
            "pentami_core": ("Quản trị Cuộc đời Toàn diện", "về hoạch định mục tiêu cá nhân và quản trị tập trung"),
        }
        
        subject, desc = app_contexts.get(target_app, ("Quản trị Chung", "về yêu cầu của bạn"))
        
        explanation = (
            f"{user_greeting}Hệ thống Penta Core tiếp nhận yêu cầu {desc}: '{query}'. "
            f"[Đã định tuyến tới phân hệ chuyên trách: {target_app.upper()}]. "
            f"Về chủ đề này, theo phong cách [STYLE], bạn nên: [ACTION_PLAN] để tối ưu hiệu quả."
        )
        return explanation, subject


# Singleton instance dùng cho toàn backend
qa_engine = QAEngine()
