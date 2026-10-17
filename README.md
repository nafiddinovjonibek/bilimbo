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
- 🔊 **Har bir topshiriq ovozli** — asosiy ovoz sifatida Narakeet'ning **Odina**
  ovozi tanlangan. Odina audiosi yaratilguncha mavjud **Madina** MP3 fayllari
  ishlaydi. Brauzer tayyor faylni
  ijro etadi, shuning uchun telefon va kompyuterda ovoz bir xil:
  - `o‘`, `g‘` saqlanadi, emoji o'qilmaydi; `12` — "o'n ikki" bo'ladi;
  - matn, ovoz yoki tezlik o'zgarsa yangi fayl nomi ishlatiladi;
  - admin panelda savol/bosqich saqlanganda yetishmayotgan ovoz yaratiladi;
  - telefon avtomatik ijroni cheklasa, bola 🔊 tugmasini bosib tinglaydi.
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
- 👥 **3 ta rol** — o‘quvchi o‘ynaydi, tasdiqlangan tarbiyachi o‘z guruhlarini kuzatadi, superadmin boshqaradi
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

# 3. Bog'liqliklarni o'rnating
pip install -r requirements.txt

# 4. Bazani tayyorlang (boshlang'ich bo'lim/savollar avtomatik kiritiladi)
python manage.py migrate

# 5. Odina uchun .env ga NARAKEET_API_KEY ni kiriting, so'ng audio yarating
python manage.py generate_question_audio
# Narakeet kaliti bo'lmasa, Madina yozuvlarini tayyorlash mumkin:
# python manage.py generate_question_audio --voice uz-UZ-MadinaNeural --rate=-10%

# 6. Superadmin yarating
python manage.py createsuperuser

# 7. Serverni ishga tushiring
python manage.py runserver
```

Sayt: http://127.0.0.1:8000 · Admin panel: http://127.0.0.1:8000/admin/

### Rollar va guruhlar

Kirgandan so‘ng o‘quvchi topshiriqlar xaritasini, tarbiyachi va superadmin
esa `/kabinet/` sahifasini ko‘radi. Ro‘yxatdan o‘tishda tanlangan tarbiyachi
hisobi administrator tasdiqlaguncha kutish sahifasida qoladi; kutubxonadan
foydalanishi mumkin.

1. Superadmin bilan `/kabinet/tarbiyachilar/` sahifasida tarbiyachini tasdiqlang.
2. **Guruh yaratish** orqali guruh ochib, tasdiqlangan tarbiyachini tanlang.
   Tarbiyachi yaratgan guruh avtomatik o‘ziga biriktiriladi.
3. Guruhdagi **O‘quvchi qo‘shish** orqali yangi bola hisobi yarating yoki
   mavjud hisobni biriktiring. Tarbiyachi mavjud hisob egasining login va
   parolini tasdiqlaydi; boshqa guruhdagi bolani o‘tkaza olmaydi.
   Superadmin login orqali biriktirishi yoki guruhlar orasida o‘tkazishi mumkin.
   Guruhsiz bolalar boshqaruv sahifasida alohida ko‘rsatiladi.

Har bir bolada bitta guruh, guruhda bitta asosiy tarbiyachi bo‘ladi.
Tarbiyachi bir nechta guruhni boshqarishi mumkin. **O‘quvchilar** sahifasida
faqat o‘z guruhidagi bolalar va ularning natijalari chiqadi. **Ovozli javoblar**
orqali yozuvni tinglab, 1–3 yulduzli baho va izoh beriladi; bola uni
**Natijalarim** sahifasida ko‘radi. Bu baho o‘yinda yig‘ilgan yulduzlardan
alohida saqlanadi. Guruhni o‘chirish yoki bolani guruhdan chiqarish uning
hisobi, natijalari va yozuvlarini o‘chirmaydi.

Tarbiyachi va admin o‘quvchi topshiriqlari orqali ball to‘play olmaydi.
**Topshiriqlarni sinash** (`/sinov/`) barcha 150 topshiriqni ochadi;
bu rejim ball, urinishlar yoki ovozli javoblarni saqlamaydi.
Kontentni tahrirlash uchun `/admin/` faqat superadminlarga ochiq.
Tarbiyachi tasdig‘i bekor qilinsa, uning ochiq sessiyasidagi boshqaruv
huquqlari keyingi so‘rovdayoq to‘xtaydi.

Mavjud bazani yangilashda hisoblar va eski natijalar saqlanadi.
Avvalgi tarbiyachilar ham tasdiqlanishi, o‘quvchilar esa kerakli guruhga
biriktirilishi kerak; migratsiya bu bog‘lanishlarni taxmin qilmaydi.

### Bolalarning ovozli yozuvlari

Yangi yozuvlar `private/voices/` ichiga saqlanadi. `PRIVATE_VOICES_ROOT`
muhit o‘zgaruvchisi bilan boshqa yopiq papka tanlanadi. Fayllar faqat
`/ovoz/<id>/tinglash/` orqali bola egasiga, uning tasdiqlangan tarbiyachisiga
va administratorga beriladi; ommaviy media havolasi yaratilmaydi.

Eski serverni yangilashda bazani va `media/ovoz/` papkasini zaxiralang,
keyin quyidagilarni bajaring:

```bash
python manage.py migrate
python manage.py protect_voice_files --dry-run
python manage.py protect_voice_files
```

Buyruq faylni yopiq joyga ko‘chiradi, nusxa yaxlitligini tekshiradi va
shundan keyin ommaviy nusxani olib tashlaydi; bazadagi yozuvlar saqlanadi.
Qayta bajarish xavfsiz. Nginx uchun `deploy/nginx-private-books.conf`
ichidagi `/media/ovoz/` taqiqini ham qo‘llang. Bazani, `private/books/`
va `private/voices/` papkalarini birgalikda zaxiralang.

### O'zbekcha savol ovozlari

Ovoz yaratishda internet kerak; tayyor MP3 ni ijro etishda TTS xizmatiga
so'rov yuborilmaydi. Fayllar `static/audio/tts/` ichida saqlanadi va odatdagi
`collectstatic` bilan joylashtiriladi. `edge-tts` — Microsoft Edge onlayn
ovoz xizmatidan foydalanadigan norasmiy kutubxona, API kaliti talab qilmaydi.
Odina ovozi Narakeet API orqali yaratiladi. API kaliti serverda saqlanadi
va brauzerga berilmaydi.

### Odina ovozini ulash

1. [Narakeet API Keys](https://www.narakeet.com/docs/automating/managing-api-keys/) orqali
   kalit oling. API Top-Up va metered subscription hisoblarida mavjud.
2. `.env.example` nusxasini `.env` deb saqlang va `NARAKEET_API_KEY` ni kiriting.
   `.env` git'ga kirmaydi. Server ishlayotgan bo'lsa, uni qayta ishga tushiring.
3. Avval uchta haqiqiy savol namunasini yarating:

   ```bash
   python manage.py generate_question_audio --samples --voice odina
   ```

4. Barcha savollarni Odina ovozida tayyorlang:

   ```bash
   python manage.py generate_question_audio --voice odina
   ```

Tayyor Odina fayli mavjud bo'lsa, u avtomatik ijro etiladi. Shu matn uchun
Odina fayli yo'q bo'lsa, avvalgi Madina yozuvi olinadi. Madina yozuvining
tezligi alohida `-10%`, Odina esa tanlangan demo kabi `+0%` (1x).
Narakeet so'rovlari odatda ketma-ket bajariladi; tarmoq xatosida pullik
generatsiya avtomatik takrorlanmaydi. Kalit yo'q bo'lsa, generatsiya oldindan
aniq xabar bilan to'xtaydi. [API hujjati](https://www.narakeet.com/docs/automating/text-to-speech-api/)

```bash
# Madina va Sardorda uchta savol namunasi + tinglash sahifasi
python manage.py generate_question_audio --samples

# Barcha yangi/o'zgargan savollar (tayyorlari qayta yaratilmaydi)
python manage.py generate_question_audio

# Ayrim savollar; kvest bo'lsa uning bosqichlari ham olinadi
python manage.py generate_question_audio --ids 121 150

# Sardor ovozini sinash
python manage.py generate_question_audio --voice uz-UZ-SardorNeural --limit 3
```

Namunalar: `static/audio/tts/namunalar.html` faylini brauzerda oching yoki
server ishlayotganda `/static/audio/tts/namunalar.html` ga kiring.
Sahifada boshqa xizmatlardan qo'shilgan ovoz namunalari ham ko'rinadi:
ular `static/audio/tts/QOSHIMCHA_NAMUNALAR.json` da qayd etilgan. Bilimbo
savolini o'qigan yozuvlar va xizmatlarning tayyor demo matnlari alohida
ko'rsatiladi. Narakeet demo audiolari xizmatning ochiq URL laridan ijro
etiladi, shu sababli ularni tinglash uchun internet kerak. `--samples`
qayta bajarilganda qo'shimcha namunalarning ro'yxati saqlanadi.
Asosiy ovoz va tezlik `core/settings.py` dagi `BILIMBO_TTS_VOICE` hamda
`BILIMBO_TTS_RATE` bilan tanlanadi. Ularni o'zgartirgach, generatsiya buyrug'ini
qayta bajaring. `--voice` faqat yaratiladigan fayllarni tanlaydi, sayt sozlamasini
o'zgartirmaydi. `--rate=-10%`, `--force`, `--jobs 3` ham mavjud.

Admin panelda **Savollar → Tanlangan savollar ovozini tayyorlash / yangilash**
amali orqali ovozlarni qayta tayyorlash mumkin. Xizmatga ulanish ishlamasa,
savol saqlanadi va admin ogohlantirish oladi. Yangi matnning audiosi tayyor
bo'lmaguncha eski savol ovozi ijro etilmaydi.

## 📚 Kitoblar kutubxonasi

`/kutubxona/` orqali akkauntga kirgan foydalanuvchi kitoblarni o‘qiydi.
Bosh sahifada **Kitoblar olami** havolasi, menyuda esa 📚 tugmasi bor.
Kitob bitta uzun sahifada pastga aylantirib o‘qiladi. Ekranga yaqin betlar
avtomatik yuklanadi; uzoqlashgan betlar telefon xotirasini band qilib turmaydi.
O‘lchamni kattalashtirish va havoladagi `#sahifa=10` orqali o‘qish joyiga
qaytish mumkin.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py import_kitoblar --dry-run
python manage.py import_kitoblar
```

Import `kitoblar/` ichidagi to‘plamlarni, jumladan `yangi/` kabi ichki
papkalarni ham tekshiradi. Har bir kitob papkasida bitta asosiy PDF va
ixtiyoriy ikki sahifali muqova bo‘lishi mumkin. `ОБЛОЖКА.pdf`, `Обложка (2).pdf`,
`muqova.pdf`, `cover.pdf` nomlari taniladi; boshqa nomdagi muqova ikkita PDF
orasidagi yagona ikki sahifali fayl bo‘lsa ham aniqlanadi. Bitta tayyor PDF
berilsa, uning sahifalar tartibi saqlanadi.

Import old muqova → barcha asosiy sahifalar → orqa muqova tartibida
birlashtiradi. Alohida JPEG/PNG shtrix-kod berilsa, orqa muqovaga qo‘yiladi;
berilmasa, muqovadagi mavjud shtrix-kod saqlanadi.
Manbalar o‘zgarmaydi. Kitoblarning nomi va mualliflari
`home/data/kitoblar.json` da; keyingi yangi kitob uchun ham shu faylga
ma’lumot qo‘shish mumkin. `2`, `4`, `5` manbalaridagi shtrix-kodlar bir xil;
import bu holatni xabar qiladi va berilgan rasmlarni saqlaydi.

Faqat yangi to‘plamni qo‘shish: `python manage.py import_kitoblar --source kitoblar/yangi`.
Manba kalitlari `2` va `yangi/2` ko‘rinishida saqlanadi, shuning uchun yangi
papkadagi raqamlar oldingi kitoblarni almashtirmaydi. `yangi/` to‘plamida
8 ta yangi asar bor; `yangi/5/Untitled.pdf` — `yangi/4` dagi “Qiziqarli
matematika”ning muqova bilan birlashtirilgan takroriy nusxasi. Manifestdagi
`duplicate_of` va `duplicate_sha256` aynan tekshirilgan nusxani takror
qo‘shishdan saqlaydi; fayl o‘zgarsa import tekshirishni talab qiladi.

Tayyor PDF va muqova rasmlari `private/books/` ichida, ommaviy `media/` va
`static/` dan tashqarida saqlanadi. `PRIVATE_BOOKS_ROOT` muhit o‘zgaruvchisi
bilan boshqa yopiq papka berish mumkin. Bazani ham, shu papkani ham
birgalikda serverga ko‘chirish/zaxiralash kerak; yoki asl `kitoblar/`
papkasidan serverda importni qayta bajarish mumkin. O‘zgarmagan manbani
qayta import qilish dublikat yaratmaydi. `--force` fayllarni qayta yig‘adi.
Admin panelda **Kitoblar** orqali nom, muallif, tartib va faollik o‘zgartiriladi.

Asl va birlashtirilgan PDF uchun yuklash endpointi yo‘q. O‘quvchi faqat
serverda rasmga aylantirilgan sahifalarni oladi; har sahifaga foydalanuvchi
ID va sana yoziladi. Sahifa so‘rovlari login, kitob/faollik, akkaunt va joriy
sessiyaga bog‘langan muddati cheklangan imzo bilan tekshiriladi.
Javoblar `private, no-store` bilan qaytadi. Soat tugaganda sahifani yangilash
kerak. Bir akkaunt uchun daqiqasiga 90 ta sahifa so‘rovi chegarasi bor.
Bu PDF faylini to‘g‘ridan-to‘g‘ri olishni yopadi; ekranda ko‘ringan kontentni
skrinshot yoki brauzer vositalari orqali ko‘chirishni to‘liq to‘xtata olmaydi.

Serverga joylashda:

- Nginx/Apache’da loyiha ildizi, `kitoblar/` yoki `private/` uchun ommaviy
  `alias`/`root` bermang. Nginx namunasi: `deploy/nginx-private-books.conf`.
- `/kutubxona/` uchun CDN/proksi keshini o‘chiring; brauzerga yopiq papkadan
  hech qanday faylni to‘g‘ridan-to‘g‘ri bermang.
- Bir nechta worker ishlatilsa, limit barcha workerlar uchun umumiy bo‘lishi
  uchun Django `CACHES` ni Redis/Memcached kabi umumiy keshga sozlang.
- Ishlab chiqarishda HTTPS ishlating va `.env` da `DJANGO_DEBUG=false`,
  tasodifiy maxfiy `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS=sizning-domen.uz`
  ni kiriting. Debug o‘chiq holatda maxfiy kalit bo‘lmasa server ishga tushmaydi;
  session/CSRF cookie faqat HTTPS orqali uzatiladi.

Tekshirish: `python manage.py test home.test_books`.

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
├── private/voices/  # Bolalar yozgan yopiq ovozlar (git'ga kirmaydi)
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
