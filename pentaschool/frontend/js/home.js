// ===== home.js — MODULE 1: TRANG CHU =====
import { state, setLop } from "./store.js";
import { SchoolAPI } from "./api.js";
import { showModule } from "./ui.js";
import { taiBaiHoc } from "./courses.js";

const CAPS = [
  { id: "tieu_hoc", icon: "🌱", ten: "Tiểu học", mo: "Lớp 1–5 · Vui + hình ảnh", lopMacDinh: 3 },
  { id: "thcs", icon: "🚀", ten: "THCS", mo: "Lớp 6–9 · Vững căn bản", lopMacDinh: 7 },
  { id: "thpt", icon: "🎯", ten: "THPT", mo: "Lớp 10–12 · Luyện thi", lopMacDinh: 11 },
];

function capCuaLop(lop) {
  if (lop <= 5) return "tieu_hoc";
  if (lop <= 9) return "thcs";
  return "thpt";
}

export function renderCap() {
  const box = document.getElementById("capRow");
  box.innerHTML = "";
  const cur = capCuaLop(state.lop);
  CAPS.forEach((c) => {
    const b = document.createElement("button");
    b.className = "cap" + (c.id === cur ? " active" : "");
    b.innerHTML = `<b>${c.icon} ${c.ten}</b><small>${c.mo}</small>`;
    b.onclick = () => {
      setLop(c.lopMacDinh);
      document.getElementById("chonLop").value = String(state.lop);
      renderCap();
      taiBaiHoc();
      taiGoiY();
      showModule("courses");
    };
    box.appendChild(b);
  });
}

export async function taiTienDo() {
  try {
    const d = await SchoolAPI.tienDo(state.hocSinh);
    state.tienDo = d.ds || [];
    state.tongSao = d.tong_sao || 0;
    document.getElementById("tongSao").textContent = state.tongSao;
    document.getElementById("statSao").textContent = state.tongSao;
    document.getElementById("statBai").textContent = state.tienDo.length;
    const pct = Math.min(100, state.tienDo.length * 10);
    document.getElementById("homeProgress").style.width = pct + "%";
    document.getElementById("homeProgressTxt").textContent =
      state.tienDo.length === 0 ? "Bắt đầu bài đầu tiên nào! 🌱" : `Đã học ${state.tienDo.length} bài — giỏi lắm!`;
  } catch (e) { /* offline: giu 0 */ }
}

export async function taiGoiY() {
  try {
    const d = await SchoolAPI.goiY(state.hocSinh, state.lop);
    if (d.loi_chao) document.getElementById("loiChao").textContent = d.loi_chao;
    const box = document.getElementById("goiY");
    box.innerHTML = (d.goi_y || []).length ? "" : "<p>Chưa có gợi ý, em chọn lớp khác nhé! 🦊</p>";
    (d.goi_y || []).forEach((b) => {
      const el = document.createElement("div");
      el.className = "the";
      el.innerHTML = `<h3>💡 ${b.tieu_de}</h3><p>Lớp ${b.lop} · ${b.thoi_luong_phut} phút</p>`;
      el.onclick = async () => {
        const { moBai } = await import("./classroom.js");
        moBai(b.id);
      };
      box.appendChild(el);
    });
  } catch (e) { /* offline */ }
}
