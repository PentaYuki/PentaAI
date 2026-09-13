// ===== mod_classroom.js — MODULE LOP HOC (video + bai + quiz, o hoc-thuat o cap3) =====
import { state, monInfo } from "../core/ps_store.js";
import { SchoolAPI } from "../core/ps_api.js";
import { toast, showModule } from "../core/ps_ui.js";
import { taiTienDo } from "./mod_home.js";
import { taiVideo, videoEmbedHTML, phutGiay } from "../core/ps_video.js";

export async function moBai(id) {
  try {
    const d = await SchoolAPI.chiTiet(id);
    if (d.loi) { toast(d.loi); return; }
    state.baiDangMo = d.bai;
    state.dapAn = {};
    const m = monInfo(d.bai.mon);
    const videos = await taiVideo(id);
    let htmlVideo = "";
    if (videos.length) {
      htmlVideo = `<div id="videoBox">${videoEmbedHTML(videos[0])}</div>
        <div class="video-list">` + videos.map((v, i) =>
          `<button data-vid="${i}" class="${i === 0 ? "active" : ""}">${state.cap === "thpt" ? "" : "🎬 "}${v.tieu_de_video || "Video " + (i + 1)} (${phutGiay(v.thoi_luong_giay)})</button>`
        ).join("") + `</div>`;
    } else if (d.bai.video_url) {
      htmlVideo = videoEmbedHTML({ video_url: d.bai.video_url, video_provider: "youtube", tieu_de_video: d.bai.tieu_de });
    }
    // cap3: muc tieu + noi dung boc trong o hoc-thuat xanh navy
    const khoiBai = state.cap === "thpt"
      ? `<div class="hoc-thuat"><b class="tieu-de">Muc tieu · Lop ${d.bai.lop} · ${m.ten}</b>${d.bai.muc_tieu || ""}</div>`
        + htmlVideo + `<div class="nd">${d.bai.noi_dung || ""}</div>`
      : `<h3>${d.bai.tieu_de}</h3><p>Muc tieu: ${d.bai.muc_tieu || ""}</p>` + htmlVideo + `<div class="nd">${d.bai.noi_dung || ""}</div>`;
    document.getElementById("ctBai").innerHTML =
      `<span class="tag">${state.cap === "thpt" ? "" : m.icon + " "}${m.ten} · Lop ${d.bai.lop}</span>` + khoiBai;
    if (videos.length > 1) {
      document.querySelectorAll("#ctBai .video-list button").forEach((b) => {
        b.onclick = () => {
          document.querySelectorAll("#ctBai .video-list button").forEach((x) => x.classList.remove("active"));
          b.classList.add("active");
          document.getElementById("videoBox").innerHTML = videoEmbedHTML(videos[parseInt(b.dataset.vid, 10)]);
        };
      });
    }
    const qb = document.getElementById("quizBox");
    qb.innerHTML = "<h3>✏️ Cùng luyện tập</h3>" +
      (d.quiz.length ? "" : "<p>Bài này đọc hiểu thôi, không có trắc nghiệm nhé!</p>");
    d.quiz.forEach((c, i) => {
      const div = document.createElement("div");
      div.className = "cau";
      div.innerHTML = `<p>Câu ${i + 1}: ${c.cau_hoi}</p>` +
        c.lua_chon.map((lc) => `<label><input type="radio" name="${c.id}" value="${lc}"> ${lc}</label>`).join("");
      qb.appendChild(div);
    });
    document.getElementById("kqBox").style.display = "none";
    showModule("classroom");
  } catch (e) { toast("Không mở được bài, thử lại nhé!"); }
}

export async function nopBai() {
  if (!state.baiDangMo) { toast("Em chọn 1 bài trước nhé!"); return; }
  const btn = document.getElementById("btnNop");
  btn.disabled = true;
  document.querySelectorAll("#quizBox input:checked").forEach((el) => { state.dapAn[el.name] = el.value; });
  try {
    const r = await SchoolAPI.nopBai({
      bai_hoc_id: state.baiDangMo.id,
      hoc_sinh: state.hocSinh,
      tra_loi: state.dapAn,
    });
    const k = r.bai_lam;
    const box = document.getElementById("kqBox");
    box.style.display = "block";
    box.className = "kq" + (k.sao_thuong <= 1 ? " sai-nhieu" : "");
    box.innerHTML = `<b>${k.nhan_xet}</b><br>Điểm: ${k.tong_diem}/${k.tong_diem_toi_da} · ⭐ +${k.sao_thuong}<br><br>` +
      (r.giai_thich || []).map((g) =>
        `📌 <b>${g.cau}</b> → Đáp án: <b>${g.dap_an}</b><br><span>${g.giai_thich}</span>`
      ).join("<br><br>");
    await taiTienDo();
    const { taiBaiHoc } = await import("./mod_courses.js");
    await taiBaiHoc();
    toast(k.sao_thuong >= 2 ? "Giỏi quá! +sao nè! 🌟" : "Cố lên, mình tiến bộ rồi! 🌱");
  } catch (e) { toast("Nộp bài lỗi, thử lại nhé!"); }
  btn.disabled = false;
}
