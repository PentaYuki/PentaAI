// ===== ps_app.js — BOOTSTRAP: chi noi module, khong chua logic =====
// Them module moi: tao js/modules/mod_<ten>.js + section data-module,
// roi import o day + goi bind. Khong sua file core.
import { state, setLop, setHocSinh } from "./core/ps_store.js";
import { bindNav, showModule } from "./core/ps_ui.js";
import { applyTheme } from "./core/ps_theme.js";
import { renderCap, taiTienDo, taiGoiY } from "./modules/mod_home.js";
import { taiMonHoc, taiBaiHoc } from "./modules/mod_courses.js";
import { nopBai } from "./modules/mod_classroom.js";
import { renderChips, hoiCo } from "./modules/mod_tutor.js";
import { renderGrowth } from "./modules/mod_growth.js";
import { renderCapFeatures } from "./modules/mod_cap.js";
import "./modules/mod_lab.js";

function dungHeader() {
  const cl = document.getElementById("chonLop");
  cl.innerHTML = "";
  for (let i = 1; i <= 12; i++) {
    const o = document.createElement("option");
    o.value = String(i);
    o.textContent = "Lop " + i;
    if (i === state.lop) o.selected = true;
    cl.appendChild(o);
  }
  cl.onchange = async () => {
    setLop(cl.value);
    applyTheme();
    renderCap();
    renderCapFeatures();
    await taiBaiHoc();
    await taiGoiY();
  };
  document.getElementById("chonTen").onchange = async (e) => {
    setHocSinh(e.target.value);
    await taiTienDo();
    await taiGoiY();
    renderGrowth();
  };
}

async function init() {
  bindNav();
  dungHeader();
  document.getElementById("locMon").onchange = taiBaiHoc;
  document.getElementById("timKiem").oninput = taiBaiHoc;
  document.getElementById("btnNop").onclick = nopBai;
  document.getElementById("btnVeKhoa").onclick = () => showModule("courses");
  document.getElementById("btnHoi").onclick = hoiCo;
  document.getElementById("cauHoi").addEventListener("keydown", (e) => {
    if (e.key === "Enter") hoiCo();
  });
  applyTheme();
  renderCap();
  renderChips();
  await taiMonHoc();
  await taiBaiHoc();
  await taiTienDo();
  await taiGoiY();
  renderGrowth();
  renderCapFeatures();
  showModule("home");
}

document.addEventListener("DOMContentLoaded", init);
