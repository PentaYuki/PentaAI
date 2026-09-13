// ===== courses.js — MODULE 2: KHOA HOC (thu vien bai hoc) =====
import { state, monInfo, khoLabel } from "../core/ps_store.js";
import { SchoolAPI } from "../core/ps_api.js";
import { toast } from "../core/ps_ui.js";
import { moBai } from "./mod_classroom.js";

export async function taiMonHoc() {
  try {
    const d = await SchoolAPI.monHoc();
    const sel = document.getElementById("locMon");
    sel.innerHTML = '<option value="">Tất cả môn</option>';
    d.ds_mon.forEach((m) => {
      state.monMap[m.id] = m;
      const o = document.createElement("option");
      o.value = m.id;
      o.textContent = m.icon + " " + m.ten;
      sel.appendChild(o);
    });
  } catch (e) {
    state.monMap = { toan: { ten: "Toán", icon: "🔢", mau: "#FFB84D" } };
    toast("Chưa nối được máy chủ, em kiểm tra lại nhé!");
  }
}

export async function taiBaiHoc() {
  const mon = document.getElementById("locMon").value;
  const tk = document.getElementById("timKiem").value.toLowerCase();
  let ds = [];
  try {
    const d = await SchoolAPI.baiHoc(state.lop, mon || undefined);
    ds = d.ds || [];
  } catch (e) { ds = []; }
  state.dsBai = ds.filter(
    (b) => !tk || (b.tieu_de || "").toLowerCase().includes(tk)
  );
  renderLuoi();
}

function daHocChua(baiId) {
  return state.tienDo.some((t) => t.bai_hoc_id === baiId);
}

function renderLuoi() {
  const box = document.getElementById("luoiBai");
  box.innerHTML = state.dsBai.length ? "" : "<p>Chưa có bài ở lớp này, em thử lớp khác nhé! 🦊</p>";
  state.dsBai.forEach((b) => {
    const m = monInfo(b.mon);
    const done = daHocChua(b.id);
    const el = document.createElement("div");
    el.className = "the" + (done ? " da-hoc" : "");
    el.innerHTML =
      `<span class="mon" style="background:${m.mau}33">${m.icon} ${m.ten} · Lớp ${b.lop}</span>` +
      `<h3>${b.tieu_de} ${done ? '<span class="tick">✓ đã học</span>' : ""}</h3>` +
      `<p>${b.muc_tieu || ""}</p>` +
      `<div class="meta"><span>⏱ ${b.thoi_luong_phut} phút</span><span class="kho">${khoLabel(b.do_kho)}</span></div>`;
    el.onclick = () => moBai(b.id);
    box.appendChild(el);
  });
}
