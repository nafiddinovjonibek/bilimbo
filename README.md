# 🎈 Bilimbo

**Bilimbo** — 5–7 yoshli bolalar uchun o'yin orqali o'rgatuvchi ta'lim platformasi. Bola sarguzasht xaritasi bo'ylab yurib, bo'limdan bo'limga o'tadi va savollarni yechib yulduzlar yig'adi.

## ✨ Imkoniyatlar

- 🗺️ **Sarguzasht xaritasi** — 5 ta bo'lim egri-bugri yo'lakcha bo'ylab joylashgan, bolalarga mos yorqin dizayn (osmon, quyosh, bulutlar, tepaliklar)
- 📚 **Bo'limchalar** — har bo'limda 2–3 tadan, jami 12 ta bo'limcha
- ❓ **Bosqichli topshiriqlar** — har bo'limchada 10 ta topshiriq, ketma-ket ochiladi
  (oldingisini yechmasdan keyingisiga o'tib bo'lmaydi)
- 🎲 **5 xil topshiriq turi**:
  | Tur | Nima qiladi |
  |---|---|
  | ❓ `tanlov` | 2–4 variantdan bittasini tanlash (rasm, matn yoki rang) |
  | ☑️ `koptanlov` | Bir nechta to'g'ri variantni belgilash |
  | 🛒 `xarid` | Byudjetga aynan to'g'ri keladigan mahsulotlarni tanlash |
  | 🧩 `tartib` | Kartochkalarni sudrab yoki bosib to'g'ri ketma-ketlikka joylash |
  | 🔗 `moslash` | Juftlarni ip bilan bog'lash |
  | 🧺 `guruh` | Elementlarni savatlarga ajratish |
  | 🏗️ `qurish` | Namunaga qarab bloklardan yig'ish (uyalar bo'yicha) |
  | 🤖 `labirint` | Robotni devorlar orasidan uyigacha olib borish |
  | 🎨 `boyash` | Chizmani palitradagi ranglar bilan bo'yash |
  | 🎤 `mikrofon` | Bola ovozini yozadi, tarbiyachi admin panelda tinglab baholaydi |
  | 🏆 `kvest` | Ketma-ket 5 bosqichli yakuniy sarguzasht |
- 🔊 **Har bir topshiriq ovozli** — savol va audio matnlar brauzerning nutq sintezi
  (Web Speech API) orqali **o'zbekcha** o'qib eshittiriladi:
  - tizimda o'zbek ovozi bo'lsa — matn o'zgarishsiz o'qiladi;
  - bo'lmasa, lotin yozuvini eng yaqin o'qiydigan turkiy ovoz (turk, ozarbayjon,
    qozoq...) tanlanadi va matn unga moslab tayyorlanadi (tutuq belgisi olib
    tashlanadi, `sh→ş`, `ch→ç`);
  - raqamlar so'z bilan aytiladi (`2–3` → "ikki–uch"), emoji va strelkalar o'qilmaydi.

  > Eng yaxshi natija uchun operatsion tizimga o'zbekcha TTS ovozini o'rnatish
  > tavsiya etiladi (Windows: *Sozlamalar → Vaqt va til → Til va mintaqa → O'zbek*).
- 🎧 **Haqiqiy ovozli topshiriqlar** — "Ovozni eshit va top" da hayvon ovozi ijro
  etiladi (`static/audio/topshiriq/`). Bunday topshiriqda matnni ovoz sinteziga
  berish mumkin emas — "Mushuk miyovladi" deb o'qilsa javob oshkor bo'ladi.
- 🖼️ **Rasmli topshiriqlar** — `static/images/topshiriq/`
- 🃏 **Rasmli variantlar** — 9 ta topshiriqda javob variantlari faqat rasmdan
  iborat (matn ham, emoji ham yo'q): bola rasmni tanib javob beradi. Matn
  bazada qolib, rasmning `alt` matni bo'ladi — ekranni o'qib beruvchi
  dasturlar uchun.

  > Rasm va ovozlarning manbasi hamda litsenziyasi o'sha papkalardagi
  > `MANBALAR.md` fayllarida.
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
│   ├── models.py    # User (rollar), Bolim, Bolimcha, Savol, Variant,
│   │                #   SavolNatija, OvozJavob
│   ├── views.py     # Xarita, savol yechish, auth view'lari
│   ├── forms.py     # Login/register formalari
│   ├── decorators.py# role_required, superadmin_required, ...
│   └── migrations/  # Sxema + boshlang'ich ma'lumotlar (seed)
├── templates/
│   ├── base.html    # Umumiy dizayn (osmon, navbar, pufakchalar)
│   ├── index.html   # Bosh sahifa — bo'limlar xaritasi
│   ├── bolim.html   # Bo'lim — bo'limchalar ro'yxati
│   ├── bolimcha.html# Topshiriqlar yo'li
│   ├── savol.html   # Topshiriq yechish sahifasi (barcha turlar uchun JS)
│   ├── topshiriq/   # Topshiriq turlarining umumiy partial'i
│   └── auth/        # Login / register
├── static/images/topshiriq/   # Topshiriq rasmlari + MANBALAR.md
├── static/audio/topshiriq/    # Topshiriq ovozlari + MANBALAR.md
├── media/           # Bolalar yozgan ovozlar (git'ga kirmaydi)
└── manage.py
```

## 📚 Kontent holati

Manba: **"Bilimbo platformasi uchun topshiriqlari.docx"** — har bir markaz
3 daraja × 10 topshiriqdan iborat.

| Bo'lim | Holat |
|---|---|
| 1. Til va nutq | ✅ To'liq |
| 2. Qurish-yasash va matematika | ✅ To'liq |
| 3. Syujetli-rolli o'yinlar | ✅ To'liq |
| 4. Fan va tabiat | ✅ To'liq |
| 5. San'at | ✅ To'liq |

**Jami 150 ta topshiriq** — hujjatdagi beshala markaz to'liq kiritilgan.

## 📝 Kontentni tahrirlash

Kontent **admin panel** orqali kiritiladi:

1. `/admin/` ga superadmin bilan kiring
2. **Bo'limlar** / **Bo'limchalar** — nom va emojilarni o'zgartiring
3. **Savollar** — topshiriq turini tanlang, matn/rasm/audio matnini kiriting,
   so'ng **Variantlar** ichida:
   - `tanlov` uchun — variantlar va "To'g'ri javob" belgisi
   - **Rasm** maydoni to'ldirilsa, variantda faqat rasm ko'rinadi
     (`moslash` da juftlik uchun — "Juftlik rasmi")
   - `tartib` uchun — "To'g'ri ketma-ketlikdagi o'rni"
   - `moslash` uchun — "Juftlik matni" / "Juftlik rasmi"
   - `guruh` uchun — "Juftlik matni" savat nomi, "Juftlik rasmi" savat rasmi
   - `qurish` uchun — "Uya joyi" (`x,y,kenglik,balandlik` foizda) va tartib
     raqami; savolning **Rasm** maydoni namuna bo'ladi
   - `koptanlov` uchun — to'g'ri variantlarning hammasiga belgi qo'ying
   - `xarid` uchun — variantlarga **Narxi**, savolga **Byudjet**; to'g'ri
     belgilangan variantlar summasi byudjetga teng bo'lishi kerak
   - `labirint` uchun — variant kerak emas, savolning **Labirint xaritasi**
     maydoniga chizma yoziladi: `#` devor, `.` yo'l, `R` robot, `H` uy.
     Har qanday o'lchamdagi to'g'ri to'rtburchak bo'lishi mumkin.
   - `boyash` uchun — savolning **Bo'yash chizmasi** maydoniga SVG yoziladi;
     bo'yaladigan har bir soha `data-soha="nom"` oladi. Variantlar palitra
     bo'ladi (faqat **Rang** maydoni to'ldiriladi). Agar sohaga
     `data-togri="#rang"` qo'shilsa, u aynan shu rangga bo'yalishi kerak —
     namunaga qarab bo'yash shunday ishlaydi; qolgan sohalarda bola istagan
     rangni tanlaydi (erkin ijod).
   - `kvest` uchun — **Kvest bosqichlari** inline'ida 5 ta bosqich

O'quvchilar natijalari **Savol natijalari**, mikrofonli javoblar esa
**Ovozli javoblar** bo'limida (tinglash va baholash bilan) ko'rinadi.
