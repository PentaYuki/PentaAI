// ===== mod_tutor.js — MODULE HOI DAP (ten + giong doi theo cap) =====
import { state } from "../core/ps_store.js";
import { TutorAPI } from "../core/ps_api.js";
import { toast } from "../core/ps_ui.js";

const GOI_Y_NHANH = [
  "Giai x^2 - 4 = 0 nhu the nao a?",
  "Dinh ly Pitago la gi a?",
  "She ___ to school (go/goes)?",
];

function tenTheoCap() {
  if (state.cap === "tieu_hoc") return { ten: "Co Cao", icon: "🦊", dangNghi: "Co Cao dang nghi..." };
  if (state.cap === "thcs") return { ten: "Ban dong hanh", icon: "🌿", dangNghi: "Dang tim goi y..." };
  return { ten: "Tro giang", icon: "◈", dangNghi: "Dang phan tich..." };
}

export function renderChips() {
  const box = document.getElementById("quickAsk");
  box.innerHTML = "";
  GOI_Y_NHANH.forEach((q) => {
    const b = document.createElement("button");
    b.textContent = q;
    b.onclick = () => {
      document.getElementById("cauHoi").value = q;
      hoiCo();
    };
    box.appendChild(b);
  });
  const t = tenTheoCap();
  const tn = document.getElementById("tutorTen");
  if (tn) tn.textContent = t.ten;
  const tf = document.getElementById("tutorFace");
  if (tf) tf.textContent = t.icon;
}

export async function hoiCo() {
  const input = document.getElementById("cauHoi");
  const q = input.value.trim();
  if (!q) { toast("Nhap cau hoi da nhe!"); return; }
  const t = tenTheoCap();
  const btn = document.getElementById("btnHoi");
  btn.disabled = true;
  const box = document.getElementById("tlTutor");
  box.style.display = "block";
  box.innerHTML = t.dangNghi;
  try {
    const mon = document.getElementById("locMon").value || null;
    const r = await TutorAPI.hoi({ cau_hoi: q, mon, lop: state.lop });
    const kq = r.tra_loi;
    // cap3 boc cong thuc trong o hoc-thuat xanh navy
    const ctHTML = (kq.cong_thuc_lien_quan?.length)
      ? (state.cap === "thpt"
        ? `<div class="hoc-thuat"><b class="tieu-de">Cong thuc lien quan</b><div class="cong-thuc">${kq.cong_thuc_lien_quan.join(", ")}</div></div>`
        : `<p>Cong thuc: <b>${kq.cong_thuc_lien_quan.join(", ")}</b></p>`)
      : "";
    box.innerHTML = `<b>${t.icon} ${t.ten}:</b> ${kq.tra_loi}` +
      `<ol>${(kq.cac_buoc || []).map((b) => `<li>${b}</li>`).join("")}</ol>` + ctHTML +
      (kq.can_giao_vien
        ? `<div class="warn">Cau nay nhay cam — hoi ngay thay co / ba me nhe!</div>`
        : "");
  } catch (e) {
    box.innerHTML = "Mang hoi lag, hoi lai sau 1 chut nhe!";
  }
  btn.disabled = false;
}
