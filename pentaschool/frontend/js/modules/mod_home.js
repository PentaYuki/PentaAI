// ===== mod_home.js — MODULE TRANG CHU (card cap + tien do + goi y) =====
import { state, setLop, capCuaLop } from "../core/ps_store.js";
import { SchoolAPI } from "../core/ps_api.js";
import { showModule } from "../core/ps_ui.js";
import { applyTheme, currentTheme } from "../core/ps_theme.js";
import { renderCapFeatures } from "./mod_cap.js";
import { taiBaiHoc } from "./mod_courses.js";

const CAPS = [
  { id: "tieu_hoc", icon: "🦊", ten: "Tieu hoc", mo: "Lop 1-5 · Vui + hinh anh", lopMacDinh: 3 },
  { id: "thcs", icon: "🌿", ten: "THCS", mo: "Lop 6-9 · Vung can ban", lopMacDinh: 7 },
  { id: "thpt", icon: "◈", ten: "THPT", mo: "Lop 10-12 · Luyen thi", lopMacDinh: 11 },
];

export function renderCap() {
  const box = document.getElementById("capRow");
  box.innerHTML = "";
  const cur = capCuaLop(state.lop);
  CAPS.forEach((c) => {
    const b = document.createElement("button");
    b.className = "cap" + (c.id === cur ? " active" : "");
    b.innerHTML = `<b>${c.icon} ${c.ten}</b><small>${c.mo}</small>`;
    b.onclick = async () => {
      setLop(c.lopMacDinh);
      document.getElementById("chonLop").value = String(state.lop);
      applyTheme();
      renderCap();
      renderCapFeatures();
      await taiBaiHoc();
      await taiGoiY();
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
    const t = currentTheme();
    document.getElementById("homeProgressTxt").textContent =
      state.tienDo.length === 0
        ? (state.cap === "thpt" ? "Bat dau ke hoach luyen thi nao!" : "Bat dau bai dau tien nao!")
        : `Da hoc ${state.tienDo.length} bai — ${state.cap === "tieu_hoc" ? "gioi lam! 🌟" : "tiep tuc nhe!"}`;
  } catch (e) { /* offline */ }
}

export async function taiGoiY() {
  try {
    const d = await SchoolAPI.goiY(state.hocSinh, state.lop);
    // loi chao theo theme, khong de backend ghi de theme cap1/cap3
    const box = document.getElementById("goiY");
    box.innerHTML = (d.goi_y || []).length ? "" : "<p>Chua co goi y, chon lop khac nhe!</p>";
    (d.goi_y || []).forEach((b) => {
      const el = document.createElement("div");
      el.className = "the";
      el.innerHTML = `<h3>${b.tieu_de}</h3><p>Lop ${b.lop} · ${b.thoi_luong_phut} phut</p>`;
      el.onclick = async () => {
        const { moBai } = await import("./mod_classroom.js");
        moBai(b.id);
      };
      box.appendChild(el);
    });
  } catch (e) { /* offline */ }
}
