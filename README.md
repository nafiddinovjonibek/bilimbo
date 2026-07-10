# 🎈 Bilimbo

**Bilimbo** — 5–7 yoshli bolalar uchun o'yin orqali o'rgatuvchi ta'lim platformasi. Bola sarguzasht xaritasi bo'ylab yurib, bo'limdan bo'limga o'tadi va savollarni yechib yulduzlar yig'adi.

## ✨ Imkoniyatlar

- 🗺️ **Sarguzasht xaritasi** — 5 ta bo'lim egri-bugri yo'lakcha bo'ylab joylashgan, bolalarga mos yorqin dizayn (osmon, quyosh, bulutlar, tepaliklar)
- 📚 **Bo'limchalar** — har bo'limda 2–3 tadan, jami 12 ta bo'limcha
- ❓ **Bosqichli savollar** — har bo'limchada 10 ta savol:
  - 3 ta oson 🟢, 3 ta o'rta 🟡, 3 ta qiyin 🟠, 1 ta tanqidiy 🟣
  - Savollar ketma-ket ochiladi — oldingisini yechmasdan keyingisiga o'tib bo'lmaydi
- ⭐ **Yulduzli baholash** — har savol 3 yulduzgacha:
  - 1-urinishda to'g'ri javob → ⭐⭐⭐
  - 2-urinishda → ⭐⭐
  - 3-urinishda → ⭐
- 👥 **3 ta rol** — Superadmin, Tarbiyachi, O'quvchi (ro'yxatdan o'tishda tarbiyachi/o'quvchi tanlanadi)
- 📱 **Mobilga mos** — aksariyat foydalanuvchilar telefondan kirishi hisobga olingan (mobile-first)
- 🛠️ **Admin panel** — bo'lim, bo'limcha va savollarni kod yozmasdan tahrirlash

## 🧰 Texnologiyalar

- Python / Django 6.0
- SQLite (dev)
- Sof HTML/CSS (framework'siz), Baloo 2 shrifti

## 🚀 O'rnatish

```bash
# 1. Loyihani yuklab oling
git clone <repo-url>
cd bilimbo

# 2. Virtual muhit yarating va faollashtiring
python -m venv env
env\Scripts\activate        # Windows
# source env/bin/activate   # Linux/Mac

# 3. Django o'rnating
pip install django

# 4. Bazani tayyorlang (boshlang'ich bo'lim/savollar avtomatik kiritiladi)
python manage.py migrate

# 5. Superadmin yarating
python manage.py createsuperuser

# 6. Serverni ishga tushiring
python manage.py runserver
```

Sayt: http://127.0.0.1:8000 · Admin panel: http://127.0.0.1:8000/admin/

## 📁 Tuzilma

```
bilimbo/
├── core/            # Django sozlamalari (settings, urls)
├── home/            # Asosiy ilova
│   ├── models.py    # User (rollar), Bolim, Bolimcha, Savol, SavolNatija
│   ├── views.py     # Xarita, savol yechish, auth view'lari
│   ├── forms.py     # Login/register formalari
│   ├── decorators.py# role_required, superadmin_required, ...
│   └── migrations/  # Sxema + boshlang'ich ma'lumotlar (seed)
├── templates/
│   ├── base.html    # Umumiy dizayn (osmon, navbar, pufakchalar)
│   ├── index.html   # Bosh sahifa — bo'limlar xaritasi
│   ├── bolim.html   # Bo'lim — bo'limchalar ro'yxati
│   ├── bolimcha.html# Savollar yo'li
│   ├── savol.html   # Savol yechish sahifasi
│   └── auth/        # Login / register
└── manage.py
```

## 📝 Kontentni tahrirlash

Bo'lim, bo'limcha nomlari va savollar hozircha namuna (placeholder) holida. Haqiqiy kontentni **admin panel** orqali kiritiladi:

1. `/admin/` ga superadmin bilan kiring
2. **Bo'limlar** / **Bo'limchalar** — nom va emojilarni o'zgartiring
3. **Savollar** — savol matni, A/B/C variantlar va to'g'ri javobni kiriting (bo'lim va daraja bo'yicha filtrlash bor)

O'quvchilar natijalari **Savol natijalari** bo'limida ko'rinadi.
