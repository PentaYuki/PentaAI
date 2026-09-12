// ===== ui.js — MODULE TIEN ICH UI (toast + dieu huong module) =====
export function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(t._h);
  t._h = setTimeout(() => t.classList.remove("show"), 2400);
}
// Chuyen tab module: home | courses | classroom | tutor | growth
const TEN_TRANG = {
  home: "🏠 Trang chủ",
  courses: "📚 Khóa học",
  classroom: "✏️ Lớp học",
  tutor: "🦊 Hỏi cô Cáo",
  growth: "⭐ Tiến bộ",
};
export function showModule(name) {
  document.querySelectorAll(".module").forEach((m) =>
    m.classList.toggle("active", m.dataset.module === name)
  );
  document.querySelectorAll("[data-nav]").forEach((b) =>
    b.classList.toggle("active", b.dataset.nav === name)
  );
  const t = document.getElementById("tenTrang");
  if (t && TEN_TRANG[name]) t.textContent = TEN_TRANG[name];
  if (name === "growth") {
    import("./growth.js").then((m) => m.renderGrowth()).catch(() => {});
  }
  window.scrollTo({ top: 0, behavior: "smooth" });
}
export function bindNav() {
  document.querySelectorAll("[data-nav]").forEach((b) => {
    b.onclick = () => showModule(b.dataset.nav);
  });
}
