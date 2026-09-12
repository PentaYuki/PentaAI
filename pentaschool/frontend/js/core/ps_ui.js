// ===== ps_ui.js — CORE: toast + dieu huong module + dang ky module =====
// Quy uoc mo rong: them chuc nang = them 1 file mod_<ten>.js + 1 section data-module,
// roi goi registerModule({id, title, onShow}) — khong sua ui.js.
import { currentTheme } from "./ps_theme.js";

export function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(t._h);
  t._h = setTimeout(() => t.classList.remove("show"), 2400);
}

// Registry: noi them module moi ma khong dung cham code cu
const REGISTRY = new Map(); // id -> {id, title, onShow}
export function registerModule(def) {
  // def: {id, title: {tieu_hoc, thcs, thpt} | string, onShow?: () => void}
  REGISTRY.set(def.id, def);
}
// Module goc dang ky san (title doi theo cap)
registerModule({ id: "home", title: { tieu_hoc: "🏠 Nhà của em", thcs: "Trang chủ", thpt: "Tổng quan" } });
registerModule({ id: "courses", title: { tieu_hoc: "📚 Học bài", thcs: "Khóa học", thpt: "Học liệu" } });
registerModule({ id: "classroom", title: { tieu_hoc: "✏️ Lớp học vui", thcs: "Lớp học", thpt: "Phòng học" } });
registerModule({ id: "tutor", title: { tieu_hoc: "🦊 Hỏi cô Cáo", thcs: "Hỏi đáp", thpt: "Trợ giảng" } });
registerModule({
  id: "growth", title: { tieu_hoc: "⭐ Sao của em", thcs: "Tiến bộ", thpt: "Phân tích" },
  onShow: () => import("../modules/mod_growth.js").then((m) => m.renderGrowth()).catch(() => {}),
});

function titleOf(id, cap) {
  const d = REGISTRY.get(id);
  if (!d) return id;
  if (typeof d.title === "string") return d.title;
  return d.title[cap] || d.title.thcs || id;
}

export function showModule(name) {
  document.querySelectorAll(".module").forEach((m) =>
    m.classList.toggle("active", m.dataset.module === name)
  );
  document.querySelectorAll("[data-nav]").forEach((b) =>
    b.classList.toggle("active", b.dataset.nav === name)
  );
  const cap = currentTheme().id;
  const t = document.getElementById("tenTrang");
  if (t) t.textContent = titleOf(name, cap);
  REGISTRY.get(name)?.onShow?.();
  window.scrollTo({ top: 0, behavior: "smooth" });
}
export function bindNav() {
  document.querySelectorAll("[data-nav]").forEach((b) => {
    b.onclick = () => showModule(b.dataset.nav);
  });
}

