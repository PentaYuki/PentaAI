// ===== ps_video.js — CORE: render LINK video tu DB (khong upload file) =====

export async function taiVideo(lessonId) {
  try {
    const r = await fetch(`/api/school/video?lesson_id=${lessonId}`);
    const d = await r.json();
    return d.ds || [];
  } catch (e) { return []; }
}

// tra ve HTML nhung: youtube -> iframe, mp4/s3 -> <video>
export function videoEmbedHTML(v) {
  const src = v.embed_url || v.video_url;
  if (!src) return "<p>Video đang cập nhật, em đọc bài trước nhé! 🌱</p>";
  if (v.video_provider === "youtube" || src.includes("youtube.com/embed")) {
    return `<div class="video-wrap"><iframe src="${src}" title="${v.tieu_de_video || "Bài giảng"}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
  }
  return `<div class="video-wrap"><video src="${src}" controls preload="metadata"${v.thumbnail_url ? ` poster="${v.thumbnail_url}"` : ""}></video></div>`;
}

export function phutGiay(giay) {
  giay = giay || 0;
  const m = Math.floor(giay / 60), s = giay % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}
