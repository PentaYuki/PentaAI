// ===== app.js — BOOTSTRAP: noi cac module lai (khong chua logic nghiep vu) =====
import { state, setLop, setHocSinh } from "./store.js";
import { bindNav, showModule, toast } from "./ui.js";
import { renderCap, taiTienDo, taiGoiY } from "./home.js";
import { taiMonHoc, taiBaiHoc } from "./courses.js";
import { nopBai } from "./classroom.js";
import { renderChips, hoiCo } from "./tutor.js";
import { renderGrowth } from "./growth.js";

function dungHeader() {
  const cl = document.getElementById("chonLop");
  cl.innerHTML = "";
  for (let i = 1; i <= 12; i++) {
    const o = document.createElement("option");
    o.value = String(i);
    o.textContent = "Lớp " + i;
    if (i === state.lop) o.selected = true;
    cl.appendChild(o);
  }
  cl.onchange = async () => {
    setLop(cl.value);
    renderCap();
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

function bindCourses() {
  document.getElementById("locMon").onchange = taiBaiHoc;
  document.getElementById("timKiem").oninput = taiBaiHoc;
}

function bindClassroom() {
  document.getElementById("btnNop").onclick = nopBai;
  document.getElementById("btnVeKhoa").onclick = () => showModule("courses");
}

function bindTutor() {
  document.getElementById("btnHoi").onclick = hoiCo;
  document.getElementById("cauHoi").addEventListener("keydown", (e) => {
    if (e.key === "Enter") hoiCo();
  });
  document.querySelectorAll('[data-nav="growth"]').forEach((b) =>
    b.addEventListener("click", renderGrowth)
  );
}

async function init() {
  bindNav();
  dungHeader();
  bindCourses();
  bindClassroom();
  bindTutor();
  renderCap();
  renderChips();
  await taiMonHoc();
  await taiBaiHoc();
  await taiTienDo();
  await taiGoiY();
  renderGrowth();
  showModule("home");
}

document.addEventListener("DOMContentLoaded", init);
