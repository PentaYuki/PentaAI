// ===== tutor.js — MODULE 4: HOI CO CAO =====
import { state } from "./store.js";
import { TutorAPI } from "./api.js";
import { toast } from "./ui.js";

const GOI_Y_NHANH = [
  "Giải x^2 - 4 = 0 như thế nào ạ?",
  "Định lý Pitago là gì ạ?",
  "She ___ to school (go/goes)?",
  "Tính số mol khi biết khối lượng ạ?",
  "Viết đoạn văn tả con mèo ạ?",
];

export function renderChips() {
  const box = document.getElementById("quickAsk");
  box.innerHTML = "";
  GOI_Y_NHANH.forEach((q) => {
    const b = document.createElement("button");
    b.textContent = q;
    b.onclick = () => {
      document.getElementById("cauHoi").value = q;
      hoiCo();
    };
    box.appendChild(b);
  });
}

export async function hoiCo() {
  const input = document.getElementById("cauHoi");
  const q = input.value.trim();
  if (!q) { toast("Em gõ câu hỏi đã nhé!"); return; }
  const btn = document.getElementById("btnHoi");
  btn.disabled = true;
  const box = document.getElementById("tlTutor");
  box.style.display = "block";
  box.innerHTML = "🦊 Cô Cáo đang nghĩ...";
  try {
    const mon = document.getElementById("locMon").value || null;
    const r = await TutorAPI.hoi({ cau_hoi: q, mon, lop: state.lop });
    const t = r.tra_loi;
    box.innerHTML = `<b>🦊 Cô Cáo:</b> ${t.tra_loi}` +
      `<ol>${(t.cac_buoc || []).map((b) => `<li>${b}</li>`).join("")}</ol>` +
      (t.cong_thuc_lien_quan?.length ? `<p>📐 Công thức: <b>${t.cong_thuc_lien_quan.join(", ")}</b></p>` : "") +
      (t.can_giao_vien
        ? `<div class="warn">⚠️ Câu này nhạy cảm — em hỏi ngay thầy cô / ba mẹ nhé!</div>`
        : `<i>💛 ${t.loi_khuyen || ""}</i>`);
  } catch (e) {
    box.innerHTML = "Mạng hơi lag, em hỏi lại sau 1 chút nhé! 🦊";
  }
  btn.disabled = false;
}
