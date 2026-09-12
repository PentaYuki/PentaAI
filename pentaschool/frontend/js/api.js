// ===== api.js — MODULE HA TANG: goi API backend =====
export async function getJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error("Loi mang " + r.status);
  return r.json();
}
export async function postJSON(url, body) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("Loi mang " + r.status);
  return r.json();
}
export const SchoolAPI = {
  monHoc: () => getJSON("/api/school/mon-hoc"),
  baiHoc: (lop, mon) => {
    let u = "/api/school/bai-hoc?";
    if (lop) u += "lop=" + lop + "&";
    if (mon) u += "mon=" + mon;
    return getJSON(u);
  },
  chiTiet: (id) => getJSON("/api/school/bai-hoc/" + id),
  nopBai: (payload) => postJSON("/api/school/nop-bai", payload),
  tienDo: (hs) => getJSON("/api/school/tien-do?hoc_sinh=" + encodeURIComponent(hs)),
  goiY: (hs, lop) => getJSON(`/api/school/goi-y-hom-nay?hoc_sinh=${encodeURIComponent(hs)}&lop=${lop}`),
};
export const TutorAPI = {
  hoi: (payload) => postJSON("/api/tutor/hoi", payload),
};
