// ===== ps_theme.js — CORE: quan ly theme theo cap (auto theo lop) =====
// tieu_hoc: de thuong pastel hong/vang, icon to, chu tron
// thcs: thien nhien xanh la/xanh duong, truong thanh hon, it icon
// thpt: nghiem tuc + hien dai: xanh navy + anh kim, vien mong, hoc thuat
import { state } from "./ps_store.js";

export const THEMES = {
  tieu_hoc: {
    id: "tieu_hoc", ten: "Tiểu học", css: "/css/themes/theme_tieu_hoc.css",
    mascot: "🦊", chao: "Chào em! Hôm nay mình học 1 bài nho nhỏ nhé!",
    sub: "Học vui mỗi ngày · Sai cũng không sao 💛",
    nav: { home: "🏠 Nhà", courses: "📚 Học", classroom: "✏️ Lớp", tutor: "🦊 Cô Cáo", growth: "⭐ Sao" },
  },
  thcs: {
    id: "thcs", ten: "THCS", css: "/css/themes/theme_thcs.css",
    mascot: "🌿", chao: "Chào bạn! Hôm nay ôn 1 chuyên đề nhé!",
    sub: "Vững căn bản · Tự tin mỗi ngày",
    nav: { home: "Trang chủ", courses: "Khóa học", classroom: "Lớp học", tutor: "Hỏi đáp", growth: "Tiến bộ" },
  },
  thpt: {
    id: "thpt", ten: "THPT", css: "/css/themes/theme_thpt.css",
    mascot: "◈", chao: "Chào bạn. Kế hoạch ôn luyện hôm nay:",
    sub: "Luyện thi · Học thuật · Tối ưu thời gian",
    nav: { home: "Tổng quan", courses: "Học liệu", classroom: "Phòng học", tutor: "Trợ giảng", growth: "Phân tích" },
  },
};

let linkEl = null;

export function currentTheme() { return THEMES[state.cap] || THEMES.thcs; }

// Nap <link> theme dung 1 lan, doi href khi doi cap — khong reload trang
export function applyTheme() {
  const t = currentTheme();
  document.body.dataset.cap = t.id;
  if (!linkEl) {
    linkEl = document.createElement("link");
    linkEl.rel = "stylesheet";
    linkEl.id = "theme-link";
    document.head.appendChild(linkEl);
  }
  linkEl.href = t.css;
  // doi nhan nav + loi chao theo cap
  document.querySelectorAll("[data-nav]").forEach((b) => {
    const k = b.dataset.nav;
    if (t.nav[k]) {
      const ic = b.querySelector(".ic");
      b.innerHTML = (ic ? "" : "") + t.nav[k];
    }
  });
  const mc = document.getElementById("mascot");
  if (mc) mc.textContent = t.mascot;
  const ch = document.getElementById("loiChao");
  if (ch) ch.textContent = t.chao;
  const sub = document.getElementById("subBrand");
  if (sub) sub.textContent = t.sub;
  return t;
}
