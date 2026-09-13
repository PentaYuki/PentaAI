// ===== ps_store.js — CORE: trang thai dung chung (khong chua UI) =====
// Quy uoc: moi module chi doc/ghi qua store, khong giu bien global rieng.
export const state = {
  hocSinh: "em",
  lop: 6,
  cap: "thcs", // tieu_hoc | thcs | thpt — tu dong theo lop
  monMap: {},
  dsBai: [],
  baiDangMo: null,
  dapAn: {},
  tienDo: [],
  tongSao: 0,
};

export function capCuaLop(lop) {
  lop = parseInt(lop, 10);
  if (lop <= 5) return "tieu_hoc";
  if (lop <= 9) return "thcs";
  return "thpt";
}

export function setLop(lop) {
  state.lop = parseInt(lop, 10);
  state.cap = capCuaLop(state.lop);
}
export function setHocSinh(ten) { state.hocSinh = ten; }
export function monInfo(mon) {
  return state.monMap[mon] || { ten: mon, icon: "📚", mau: "#FFD97D" };
}
export function khoLabel(k) {
  // cap3 dung chu nghiem tuc hon, cap1 nhieu icon hon
  if (state.cap === "thpt") return k === 1 ? "Cơ bản" : k === 2 ? "Trung bình" : "Nâng cao";
  if (state.cap === "thcs") return k === 1 ? "Dễ" : k === 2 ? "Vừa" : "Thử thách";
  return k === 1 ? "🌱 Dễ" : k === 2 ? "🌼 Vừa" : "🔥 Thử thách";
}

