// ===== growth.js — MODULE 5: TIEN BO (sao + huy hieu) =====
import { state } from "../core/ps_store.js";

export function renderGrowth() {
  document.getElementById("saoTo").textContent = "⭐ " + state.tongSao;
  const box = document.getElementById("dsTienDo");
  const hh = document.getElementById("huyHieu");
  if (!state.tienDo.length) {
    box.innerHTML = "<p>Em chưa học bài nào — bắt đầu bài đầu tiên ở mục Khóa học nhé! 🌱</p>";
  } else {
    box.innerHTML = state.tienDo.map((t) =>
      `<div class="cau"><p>📖 ${t.bai_hoc_id}</p><span>${t.trang_thai === "da_hoc" ? "✅ Đã học" : "📝 Đang học"} · ${t.phan_tram}% · ⭐ ${t.sao}</span></div>`
    ).join("");
  }
  const rules = [
    { icon: "🌱", ten: "Bắt đầu", dat: state.tienDo.length >= 1 },
    { icon: "📚", ten: "Chăm chỉ (3 bài)", dat: state.tienDo.length >= 3 },
    { icon: "🌟", ten: "Tỏa sáng (5 sao)", dat: state.tongSao >= 5 },
    { icon: "🏆", ten: "Siêu sao (10 sao)", dat: state.tongSao >= 10 },
  ];
  hh.innerHTML = rules.map((r) =>
    `<div class="hh ${r.dat ? "" : "lock"}"><div style="font-size:28px">${r.icon}</div>${r.ten}<br>${r.dat ? "✅" : "🔒"}</div>`
  ).join("");
}
