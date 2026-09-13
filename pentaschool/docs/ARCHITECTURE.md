# PentaSchool — Kien truc LMS K12 (lop 1-12)

> Triet ly: de thuong + nhe nhang + nghiem tuc.
> 1 trang duy nhat, chia 5 module ro rang o ca frontend lan backend.

## 1. So do 1 trang LMS

```text
SIDEBAR (trai, desktop) / BOTTOMNAV (mobile)
  Trang chu | Khoa hoc | Lop hoc | Hoi co Cao | Tien bo
MODULE 1 HOME: chao + cap hoc + stats + goi y
MODULE 2 COURSES: loc mon/tim kiem + luoi the
MODULE 3 CLASSROOM: doc bai + quiz + nop + sao
MODULE 4 TUTOR: hoi co Cao + chip hoi nhanh
MODULE 5 GROWTH: tong sao + huy hieu + lich su
```

## 2. Chia module frontend (moi module = 1 css + 1 js)

```text
frontend/
  index.html          # khung 5 section data-module
  css/: base, layout, home, courses, classroom, tutor, growth
  js/: app (bootstrap), api, store, ui, home, courses, classroom, tutor, growth
```

Quy tac: app.js chi noi module; module khong import cheo nhau.

## 3. Backend

```text
backend/api/catalog.py   -> mon-hoc, bai-hoc, chi-tiet (an dap an)
backend/api/learning.py  -> nop-bai, tien-do, goi-y-hom-nay
backend/api/tutor.py     -> hoi co Cao
backend/domain/          -> models + seed (14 bai/12 lop) + services
backend/infrastructure/  -> STORE in-memory -> sau thay Postgres
```

## 4. Mau sac pastel

nen kem #FFF9F2, hong #FFB3C1/#F4738C, vang #FFD97D,
xanh la #A8E6B0, xanh duong #A8D8FF, tim #D5B8FF, cam #FFC89F

## 5. Chay

```bash
cd /home/gooleseswsq1/Projects/PentaAI
python3 -m pentaschool.backend.main
# mo http://127.0.0.1:8001/
python3 pentaschool/tests/test_basic.py
```
