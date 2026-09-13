# Quy uoc dat ten module (de mo rong, them chuc nang khong dung cham code cu)

## 1. Nguyen tac chung

- Tien to `ps_` = ha tang dung chung PentaSchool (core, khong chua nghiep vu).
- Tien to `mod_` = 1 chuc nang nghiep vu doc lap (home, courses, classroom, tutor, growth, lab...).
- Moi module gom: 1 section `data-module="<id>"` + 1 file `mod_<id>.js` + 1 file `mod_<id>.css`.
- Module chi giao tiep qua `ps_store.js` (state) + `ps_api.js` (fetch) + `ps_ui.js` (registerModule/showModule).

## 2. Cay thu muc hien tai

```text
frontend/
  index.html                    # khung + nap css theo nhom
  css/
    core/                       # khung dung chung, khong sua khi them tinh nang
      ps_base.css               # bien mau goc + reset + font
      ps_layout.css             # sidebar / main / bottomnav / toast / panel
      ps_video.css              # khung player video (iframe, video)
    themes/                     # giao dien theo cap, tu doi khi doi lop
      theme_tieu_hoc.css        # cap1: hong/vang pastel, bo goc to, icon to
      theme_thcs.css            # cap2: xanh la/duong thien nhien, it icon
      theme_thpt.css            # cap3: xanh navy + anh kim, o .hoc-thuat/.cong-thuc
    modules/                    # moi module 1 file, them module = them 1 file
      mod_home.css / mod_courses.css / mod_classroom.css / mod_tutor.css / mod_growth.css
  js/
    ps_app.js                   # bootstrap: import + bind, khong logic
    core/
      ps_api.js                 # SchoolAPI + TutorAPI (fetch JSON)
      ps_store.js               # state + setLop/setHocSinh + capCuaLop + khoLabel theo cap
      ps_theme.js               # THEMES + applyTheme() (doi <link>, nav, mascot, loi chao)
      ps_ui.js                  # toast + registerModule + showModule (title theo cap)
      ps_video.js               # taiVideo + videoEmbedHTML (youtube -> iframe, mp4 -> video)
    modules/
      mod_home.js               # card cap + tien do + goi y
      mod_courses.js            # thu vien bai hoc (loc mon, tim kiem)
      mod_classroom.js          # mo bai + quiz + nop (cap3 boc o hoc-thuat)
      mod_tutor.js              # hoi dap (ten doi theo cap: Co Cao / Ban / Tro giang)
      mod_growth.js             # sao + huy hieu + lich su
      mod_cap.js                # FEATURES theo cap + renderCapFeatures ([data-feature])
      mod_lab.js                # mau mo rong: Lab hoc thuat cap3 (cong thuc + pomodoro + de)
```

## 3. Them chuc nang moi (vi du: mod_kiem_tra.js) — 4 buoc, khong sua core

1. Tao `js/modules/mod_kiem_tra.js` export `init/render...`, tu `registerModule({id:"kiem_tra",...})`.
2. Tao `css/modules/mod_kiem_tra.css` (chi style cua module do).
3. Them `<section class="module" data-module="kiem_tra">` + nut `data-nav="kiem_tra"` vao `index.html`.
4. Them 2 dong `<link>` + `import` trong `index.html` / `ps_app.js`. Xong — khong dung vao module cu.

## 4. Chuc nang thay doi theo cap

- `state.cap` tu dong theo lop (`ps_store.capCuaLop`): 1-5 tieu_hoc, 6-9 thcs, 10-12 thpt.
- Doi lop → `ps_app` goi `applyTheme()` (doi `body[data-cap]` + file theme) + `renderCapFeatures()`.
- Nut theo cap: gan `data-feature="doc_to|to_mau|so_tay|thi_dua|pomodoro..."`, khai bao trong `mod_cap.FEATURES`.
- Mau chu dao: cap1 hong/vang (`--chinh:#F4738C`), cap2 xanh la (`--chinh:#2E9E6B`), cap3 xanh navy (`--chinh:#1D4ED8`).
- O hoc thuat cap3: `.hoc-thuat` + `.cong-thuc` (nen navy, chu mono) — dung trong classroom/tutor/lab.

## 5. Backend giu nguyen

`catalog.py / learning.py / videos.py / tutor.py` + `domain/` + `infrastructure/db.py` (video chi chua link).
