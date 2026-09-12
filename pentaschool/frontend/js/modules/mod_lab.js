// ===== mod_lab.js — MODULE PHONG LAB CAP3 (hoc thuat: cong thuc + pomodoro + de thi) =====
// Vi du mo rong kieu mau: them chuc nang = them 1 file mod_<ten>.js nhu file nay.
import { registerModule, toast } from "../core/ps_ui.js";
import { state } from "../core/ps_store.js";

registerModule({
  id: "lab", title: { tieu_hoc: "🔬 Góc khám phá", thcs: "Phòng lab", thpt: "Lab học thuật" },
  onShow: () => renderLab(),
});

const CONG_THUC = [
  { ten: "Delta phương trình bậc 2", ct: "Δ = b² − 4ac", vd: "x²−4=0 → a=1,b=0,c=−4 → Δ=16" },
  { ten: "Pitago", ct: "c² = a² + b²", vd: "a=3,b=4 → c=5" },
  { ten: "Vận tốc biến đổi đều", ct: "v = v₀ + a·t", vd: "v₀=2,a=3,t=4 → v=14 m/s" },
  { ten: "Số mol", ct: "n = m / M", vd: "m=8g H₂ (M=2) → n=4 mol" },
];

let phut = 25, giay = 0, timer = null;

export function renderLab() {
  const box = document.getElementById("labBox");
  if (!box) return;
  if (state.cap !== "thpt") {
    box.innerHTML = `<p>${state.cap === "tieu_hoc" ? "🦊 Góc khám phá mở thêm khi em lên cấp 2 nhé!" : "🌿 Phòng lab mở full khi lên cấp 3 nhé!"}</p>`;
    return;
  }
  box.innerHTML = `
    <div class="hoc-thuat"><b class="tieu-de">Bảng công thức trọng tâm</b>
      ${CONG_THUC.map((c) => `<div style="margin:6px 0"><b>${c.ten}</b><div class="cong-thuc">${c.ct}</div><span style="font-size:13px;color:#64748B">VD: ${c.vd}</span></div>`).join("")}
    </div>
    <div class="hoc-thuat"><b class="tieu-de">Pomodoro 25 phút — tập trung luyện đề</b>
      <div style="font-size:32px;font-weight:800" id="pomoClock">25:00</div>
      <button class="btn" id="btnPomo">Bắt đầu</button>
      <button class="btn phu" id="btnPomoRs">Reset</button>
    </div>
    <div class="hoc-thuat"><b class="tieu-de">Đề thi thử (theo bài đang mở)</b>
      <p style="font-size:13px">Vào Phòng học mở 1 bài lớp 10–12 rồi quay lại đây bấm “Tạo đề”.</p>
      <button class="btn" id="btnDe">Tạo đề từ quiz</button>
      <div id="deOut" style="margin-top:8px"></div>
    </div>`;
  document.getElementById("btnPomo").onclick = chayPomo;
  document.getElementById("btnPomoRs").onclick = () => { clearInterval(timer); phut = 25; giay = 0; veDongHo(); };
  document.getElementById("btnDe").onclick = () => {
    const b = state.baiDangMo;
    document.getElementById("deOut").innerHTML = b
      ? `<b>Đề: ${b.tieu_de}</b> — 15 phút — làm nghiêm túc như thi thật nhé! ⏱`
      : "Chưa có bài đang mở. Em mở 1 bài lớp 10–12 trước nhé!";
  };
}
function veDongHo() {
  const el = document.getElementById("pomoClock");
  if (el) el.textContent = `${String(phut).padStart(2, "0")}:${String(giay).padStart(2, "0")}`;
}
function chayPomo() {
  clearInterval(timer);
  toast("Bắt đầu 25 phút tập trung! 💪");
  timer = setInterval(() => {
    if (giay === 0) { if (phut === 0) { clearInterval(timer); toast("Hết giờ! Nghỉ 5 phút nhé! ☕"); return; } phut--; giay = 59; }
    else giay--;
    veDongHo();
  }, 1000);
}
