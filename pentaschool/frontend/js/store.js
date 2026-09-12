// ===== store.js — MODULE TRANG THAI DUNG CHUNG =====
export const state = {
  hocSinh: "em",
  lop: 6,
  monMap: {},
  dsBai: [],
  baiDangMo: null,
  dapAn: {},
  tienDo: [],
  tongSao: 0,
};
export function setLop(lop) { state.lop = parseInt(lop, 10); }
export function setHocSinh(ten) { state.hocSinh = ten; }
export function monInfo(mon) {
  return state.monMap[mon] || { ten: mon, icon: "📚", mau: "#FFD97D" };
}
export function khoLabel(k) {
  return k === 1 ? "🌱 Dễ" : k === 2 ? "🌼 Vừa" : "🔥 Thử thách";
}
