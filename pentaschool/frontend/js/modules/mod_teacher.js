// ===== mod_teacher.js — TRANG GIAO VIEN (giao dien radiant, dung chung 3 cap) =====
// Quy uoc mo rong: them tab moi = them <section data-tv-module="ten"> + them case o switchTab.

const $ = (id) => document.getElementById(id);
const API = "/api/school";

async function getJSON(u) { const r = await fetch(u); if (!r.ok) throw new Error("Loi " + r.status); return r.json(); }
async function sendJSON(u, method, body) {
  const r = await fetch(u, { method, headers: { "Content-Type": "application/json" }, body: body ? JSON.stringify(body) : undefined });
  if (!r.ok) throw new Error("Loi " + r.status); return r.json();
}
function toast(msg) {
  const t = $("toast"); if (!t) return;
  t.textContent = msg; t.classList.add("show");
  clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 2400);
}

let DS_BAI = [];
let LESSON_MAP = {}; // id -> {tieu_de, lop}

// ---------- Tab ----------
function switchTab(name) {
  document.querySelectorAll("[data-tv-module]").forEach((m) => m.classList.toggle("active", m.dataset.tvModule === name));
  document.querySelectorAll("[data-tv]").forEach((b) => b.classList.toggle("active", b.dataset.tv === name));
  const titles = { videos: "Video bài giảng", bai: "Bài học", baocao: "Báo cáo" };
  const t = $("tvTitle"); if (t) t.textContent = titles[name] || name;
}

// ---------- Video ----------
async function taiVideo() {
  const d = await getJSON(API + "/teacher/videos");
  const tb = $("tvVideoTable");
  $("tvVideoCount").textContent = `Tổng ${d.tong} video — DB chỉ chứa LINK, không chứa file.`;
  let html = "<tr><th>ID</th><th>Bài học</th><th>Tiêu đề</th><th>Nguồn</th><th>Link</th><th></th></tr>";
  for (const v of d.ds) {
    const b = LESSON_MAP[v.lesson_id] || {};
    html += `<tr><td><code>${v.id}</code></td>
      <td>${b.tieu_de || v.lesson_id}<br><span class="tv-tag">lớp ${b.lop ?? "?"}</span></td>
      <td>${v.tieu_de_video || "—"}</td>
      <td><span class="tv-tag">${v.video_provider}</span></td>
      <td><code>${(v.video_url || v.embed_url || "—").slice(0, 48)}</code></td>
      <td><button class="tv-btn xoa" data-xoa="${v.id}">Xóa</button></td></tr>`;
  }
  if (!d.tong) html += '<tr><td colspan="6">Chưa có video nào.</td></tr>';
  tb.innerHTML = html;
  tb.querySelectorAll("[data-xoa]").forEach((b) => {
    b.onclick = async () => {
      if (!confirm("Xóa video " + b.dataset.xoa + "?")) return;
      await sendJSON(API + "/teacher/videos/" + b.dataset.xoa, "DELETE");
      toast("Đã xóa " + b.dataset.xoa); taiVideo();
    };
  });
}

async function taoVideo(e) {
  e.preventDefault();
  const body = {
    id: $("tvId").value.trim(), lesson_id: $("tvLesson").value,
    tieu_de_video: $("tvTieuDe").value.trim(), video_url: $("tvUrl").value.trim(),
    video_provider: $("tvProvider").value, thoi_luong_giay: parseInt($("tvDur").value || "0", 10),
  };
  if (!body.id || !body.lesson_id) return toast("Thiếu mã video / bài học");
  try {
    const d = await sendJSON(API + "/teacher/videos", "POST", body);
    toast("Đã lưu video: " + d.video.id);
    $("tvVideoForm").reset(); $("tvDur").value = 0;
    taiVideo();
  } catch (err) { toast("Lỗi: " + err.message); }
}

// ---------- Bai hoc ----------
async function taiBai() {
  const d = await getJSON(API + "/teacher/lessons");
  DS_BAI = d.ds; LESSON_MAP = {};
  const sel = $("tvLesson"); sel.innerHTML = "";
  const loc = $("tvLocLop");
  const lops = [...new Set(DS_BAI.map((b) => b.lop))].sort((a, b) => a - b);
  loc.innerHTML = '<option value="">Tất cả lớp</option>' + lops.map((l) => `<option value="${l}">Lớp ${l}</option>`).join("");
  for (const b of DS_BAI) {
    LESSON_MAP[b.id] = b;
    sel.insertAdjacentHTML("beforeend", `<option value="${b.id}">L${b.lop} — ${b.tieu_de}</option>`);
  }
  veBangBai();
}
function veBangBai() {
  const f = $("tvLocLop").value;
  const ds = f ? DS_BAI.filter((b) => String(b.lop) === f) : DS_BAI;
  let html = "<tr><th>ID</th><th>Lớp</th><th>Tiêu đề</th><th>Thời lượng</th><th>Độ khó</th></tr>";
  for (const b of ds) {
    html += `<tr><td><code>${b.id}</code></td><td><span class="tv-tag">L${b.lop}</span></td>
      <td>${b.tieu_de}</td><td>${b.thoi_luong_phut}'</td><td>${"★".repeat(b.do_kho || 1)}</td></tr>`;
  }
  if (!ds.length) html += '<tr><td colspan="5">Không có bài.</td></tr>';
  $("tvBaiTable").innerHTML = html;
}

// ---------- Init ----------
document.querySelectorAll("[data-tv]").forEach((b) => (b.onclick = () => switchTab(b.dataset.tv)));
$("tvVideoForm").onsubmit = taoVideo;
$("tvRefresh").onclick = () => { taiVideo(); toast("Đã tải lại"); };
$("tvLocLop").onchange = veBangBai;
taiBai().then(taiVideo).catch((e) => toast("Không tải được dữ liệu: " + e.message));