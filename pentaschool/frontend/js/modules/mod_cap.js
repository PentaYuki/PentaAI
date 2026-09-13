// ===== mod_cap.js — MODULE CHUC NANG THEO CAP (hien/ an theo lop) =====
// Y anh: chuc nang thay doi theo cap — cap nho don gian, cap lon them hoc thuat.
import { state } from "../core/ps_store.js";

// Khai bao tinh nang theo cap: cap nao duoc thay gi
export const FEATURES = {
  // Cap1: doc to + mau sac + keo tha (don gian, vui)
  doc_to: { caps: ["tieu_hoc"], ten: "🔊 Đọc to bài" },
  to_mau: { caps: ["tieu_hoc"], ten: "🎨 Tô màu chữ" },
  // Cap2: so tay + thi dau tuan (thien nhien, thi dua nhe)
  so_tay: { caps: ["thcs"], ten: "🌿 Sổ tay xanh" },
  thi_dua: { caps: ["thcs"], ten: "🏃 Đua top tuần" },
  // Cap3: cong thuc + de thi + pomodoro (hoc thuat, hien dai, xanh navy)
  cong_thuc: { caps: ["thpt"], ten: "Công thức" },
  de_thi: { caps: ["thpt"], ten: "Đề thi thử" },
  pomodoro: { caps: ["thpt"], ten: "Pomodoro 25'" },
  // Chung ca 3 cap
  video: { caps: ["tieu_hoc", "thcs", "thpt"], ten: "Video" },
  quiz: { caps: ["tieu_hoc", "thcs", "thpt"], ten: "Quiz" },
};

export function coChucNang(ten) {
  return (FEATURES[ten]?.caps || []).includes(state.cap);
}

// Ve lai cac nut chuc nang khi doi cap
export function renderCapFeatures() {
  document.querySelectorAll("[data-feature]").forEach((el) => {
    el.style.display = coChucNang(el.dataset.feature) ? "" : "none";
  });
  // doi mau chu dao: cap1 hong/vang, cap2 xanh la, cap3 xanh navy (qua CSS bien --chinh)
  document.getElementById("capBadge").textContent =
    state.cap === "tieu_hoc" ? "🌱 Cấp 1 · Vui học" :
    state.cap === "thcs" ? "🌿 Cấp 2 · Vững vàng" : "◈ Cấp 3 · Luyện thi";
}
