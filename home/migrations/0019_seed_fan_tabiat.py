"""4-bo'lim — "FAN VA TABIAT MARKAZI".

Manba: "Bilimbo platformasi uchun topshiriqlari.docx".
Hujjatdagi ikkita topshiriqda video ko'zda tutilgan ("Muz erimoqda",
"Bir o'simlik sug'orilgan, ikkinchisi sug'orilmagan") — ular oldin/keyin
rasmiga aylantirildi, savol va javoblar o'zgarmadi.
"""
from django.db import migrations

V = 'images/topshiriq/variantlar/'

OSON = [
    {
        'tur': 'guruh',
        'sarlavha': 'Jonli yoki jonsiz?',
        'matn': "Rasmni to'g'ri qutiga joylashtir.",
        'guruh': [
            ('Daraxt', V + 'daraxt.png', 'Jonli', V + 'quti-kok.png'),
            ('Tosh', V + 'tosh.png', 'Jonsiz', V + 'quti-qizil.png'),
            ('Qush', V + 'qush.png', 'Jonli', V + 'quti-kok.png'),
            ('Mashina', V + 'mashina.png', 'Jonsiz', V + 'quti-qizil.png'),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Faslni tanla',
        'matn': "Qor yog'ayotgan rasm qaysi faslni bildiradi?",
        'rasm': V + 'qish.png',
        'variantlar': [('', 'Bahor', False), ('', 'Yoz', False),
                       ('', 'Kuz', False), ('', 'Qish', True)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Hayvonning bolasini top',
        'matn': 'Sigirning bolasi qaysi?',
        'rasm': V + 'sigir.png',
        'variantlar': [('', 'Buzoq', True), ('', 'Toychoq', False),
                       ("", "Qo'zichoq", False)],
        'v_rasm': {1: V + 'buzoq.png', 2: V + 'toychoq.png', 3: V + 'qozichoq.png'},
    },
    {
        'tur': 'guruh',
        'sarlavha': 'Meva yoki sabzavot?',
        'matn': 'Rasmlarni "Meva" va "Sabzavot" savatlariga ajrat.',
        'guruh': [
            ('Sabzi', V + 'sabzi.png', 'Sabzavot', V + 'quti-qizil.png'),
            ('Olma', V + 'olma.png', 'Meva', V + 'quti-kok.png'),
            ('Bodring', V + 'bodring.png', 'Sabzavot', V + 'quti-qizil.png'),
            ('Banan', V + 'banan.png', 'Meva', V + 'quti-kok.png'),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Qayerda yashaydi?',
        'matn': 'Baliq qayerda yashaydi?',
        'rasm': V + 'baliq.png',
        'variantlar': [('', 'Suv', True), ("", "O'rmon", False),
                       ("", "Cho'l", False)],
        'v_rasm': {1: V + 'suv.png', 2: V + 'ormon.png', 3: V + 'chol.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Rangni top',
        'matn': 'Quyosh qanday rangda?',
        'variantlar': [('', 'Sariq', True, '#f2c230'), ('', 'Yashil', False, '#4caf50'),
                       ("", "Ko'k", False, '#3d7be0'), ('', 'Qizil', False, '#e94b4b')],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Daraxtni tanla',
        'matn': 'Daraxtni tanla.',
        'variantlar': [('', 'Daraxt', True), ('', 'Gul', False),
                       ("", "Qo'ziqorin", False), ('', 'Kaktus', False)],
        'v_rasm': {1: V + 'daraxt.png', 2: V + 'gul.png',
                   3: V + 'qoziqorin.png', 4: V + 'kaktus.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Ob-havoni top',
        'matn': 'Bugun ob-havo qanday?',
        'rasm': V + 'quyoshli.png',
        'variantlar': [('', 'Quyoshli', True), ("", "Yomg'irli", False),
                       ('', 'Shamolli', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kim uchadi?',
        'matn': 'Qaysi biri ucha oladi?',
        'variantlar': [('', 'Kapalak', True), ('', 'Sigir', False),
                       ('', 'Baliq', False), ('', 'Toshbaqa', False)],
        'v_rasm': {1: V + 'kapalak.png', 2: V + 'sigir.png',
                   3: V + 'baliq.png', 4: V + 'toshbaqa.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': "To'g'ri javobni tanla",
        'matn': "O'simlik o'sishi uchun nima kerak?",
        'variantlar': [('', 'Suv', True), ('', 'Qum', False), ('', 'Tosh', False)],
        'v_rasm': {1: V + 'suv.png', 2: V + 'qum.png', 3: V + 'tosh.png'},
    },
]

ORTA = [
    {
        'tur': 'qurish',
        'sarlavha': "O'simlikning qismlarini joylashtir",
        'matn': "O'simlik qismlarini o'z joyiga qo'y.",
        'rasm': V + 'namuna-osimlik.png',
        'qurish': [
            ('Gul', V + 'osimlik-gul.png', '38,2,24,22', False),
            ('Barg', V + 'osimlik-barg.png', '52,28,26,10', False),
            ('Poya', V + 'osimlik-poya.png', '47,22,7,34', False),
            ('Ildiz', V + 'osimlik-ildiz.png', '39,54,23,14', False),
        ],
    },
    {
        'tur': 'tartib',
        'sarlavha': 'Oziq zanjiri',
        'matn': "Oziq zanjirini to'g'ri ketma-ketlikda joylashtir.",
        'tartib': [("", "O't"), ('', 'Quyon'), ('', 'Tulki')],
        'v_rasm': {1: V + 'ot-giyoh.png', 2: V + 'quyon.png', 3: V + 'tulki.png'},
    },
    {
        'tur': 'tartib',
        'sarlavha': 'Fasllarni tartibla',
        'matn': "Fasllarni to'g'ri ketma-ketlikka joylashtir.",
        'tartib': [('', 'Bahor'), ('', 'Yoz'), ('', 'Kuz'), ('', 'Qish')],
        'v_rasm': {1: V + 'bahor.png', 2: V + 'yoz.png',
                   3: V + 'kuz.png', 4: V + 'qish.png'},
    },
    {
        'tur': 'moslash',
        'sarlavha': 'Hayvonlarni yashash joyiga joylashtir',
        'matn': "Har bir hayvonni yashash joyi bilan bog'la.",
        'juftlar': [('', 'Sher', '', 'Savanna'), ('', 'Pingvin', '', 'Muzlik'),
                    ('', 'Tuya', '', "Cho'l")],
        'v_rasm': {1: V + 'sher.png', 2: V + 'pingvin.png', 3: V + 'tuya.png'},
        'j_rasm': {1: V + 'savanna.png', 2: V + 'muzlik.png', 3: V + 'chol.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Tabiat hodisasini tanla',
        'matn': 'Chaqmoqni tanla.',
        'variantlar': [('', 'Chaqmoq', True), ('', 'Qor', False),
                       ('', 'Tuman', False)],
        'v_rasm': {1: V + 'chaqmoq.png', 2: V + 'qorli.png', 3: V + 'tuman.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Tajribani kuzat',
        'matn': 'Muz nima bo\'ldi?',
        'rasm': V + 'tajriba-muz.png',
        'variantlar': [('', 'Eridi', True), ('', 'Yonib ketdi', False),
                       ("", "O'sdi", False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Qaysi biri tabiatni ifloslantiradi?',
        'matn': 'Qaysi biri tabiatni ifloslantiradi?',
        'variantlar': [('', 'Barg', False), ('', 'Plastik shisha', True),
                       ('', 'Qush', False), ('', 'Daraxt', False)],
        'v_rasm': {1: V + 'barg.png', 2: V + 'plastik-shisha.png',
                   3: V + 'qush.png', 4: V + 'daraxt.png'},
    },
    {
        'tur': 'guruh',
        'sarlavha': 'Guruhlarga ajrat',
        'matn': 'Uy hayvonlari va yovvoyi hayvonlarni ajrat.',
        'guruh': [
            ('It', V + 'it.png', 'Uy hayvonlari', V + 'quti-kok.png'),
            ('Sher', V + 'sher.png', 'Yovvoyi hayvonlar', V + 'quti-qizil.png'),
            ('Mushuk', V + 'mushuk.png', 'Uy hayvonlari', V + 'quti-kok.png'),
            ('Tulki', V + 'tulki.png', 'Yovvoyi hayvonlar', V + 'quti-qizil.png'),
            ('Sigir', V + 'sigir.png', 'Uy hayvonlari', V + 'quti-kok.png'),
            ('Ayiq', V + 'ayiq.png', 'Yovvoyi hayvonlar', V + 'quti-qizil.png'),
        ],
    },
    {
        'tur': 'moslash',
        'sarlavha': 'Soya kimniki?',
        'matn': "Har bir hayvonni o'z soyasi bilan bog'la.",
        'juftlar': [('', 'Fil', '', 'Fil soyasi'), ('', 'Baliq', '', 'Baliq soyasi'),
                    ('', 'Qush', '', 'Qush soyasi')],
        'v_rasm': {1: V + 'fil.png', 2: V + 'baliq.png', 3: V + 'qush.png'},
        'j_rasm': {1: V + 'soya-fil.png', 2: V + 'soya-baliq.png',
                   3: V + 'soya-qush.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Sababini top',
        'matn': 'Nima uchun gullarga suv kerak?',
        'variantlar': [("", "O'sishi va so'lmasligi uchun.", True),
                       ('', 'Rangi chiroyli bo\'lishi uchun.', False),
                       ('', 'Hidi yoqimli bo\'lishi uchun.', False)],
    },
]

QIYIN = [
    {
        'tur': 'tanlov',
        'sarlavha': 'Tajribani tahlil qil',
        'matn': "Bir o'simlik sug'orilgan, ikkinchisi sug'orilmagan.\n"
                "Qaysi o'simlik yaxshi o'sadi?",
        'rasm': V + 'tajriba-osimlik.png',
        'variantlar': [("", "Sug'orilgani — o'simlikka suv kerak.", True),
                       ("", "Sug'orilmagani.", False),
                       ('', 'Ikkalasi ham bir xil.', False)],
    },
    {
        'tur': 'guruh',
        'sarlavha': 'Tabiatni asra',
        'matn': "Axlatni chiqindi qutisiga tashla, tabiatnikini joyida qoldir.",
        'guruh': [
            ('Plastik shisha', V + 'plastik-shisha.png',
             'Chiqindi qutisi', V + 'chiqindi-qutisi.png'),
            ('Gul', V + 'gul.png', 'Tabiatda qolsin', V + 'ormon.png'),
            ("Qog'oz", V + 'qogoz.png', 'Chiqindi qutisi', V + 'chiqindi-qutisi.png'),
            ('Daraxt', V + 'daraxt.png', 'Tabiatda qolsin', V + 'ormon.png'),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Hayvonni tavsifidan top',
        'matn': '"Men suvda yashayman, jabram bilan nafas olaman."\nBu kim?',
        'variantlar': [('', 'Baliq', True), ('', 'Mushuk', False), ('', 'It', False)],
        'v_rasm': {1: V + 'baliq.png', 2: V + 'mushuk.png', 3: V + 'it.png'},
    },
    {
        'tur': 'tartib',
        'sarlavha': 'Qaysi biri avval sodir bo\'ladi?',
        'matn': "To'g'ri ketma-ketlikni tuz.",
        'tartib': [("", "Urug'"), ('', 'Nihol'), ('', 'Gul')],
        'v_rasm': {1: V + 'urug.png', 2: V + 'nihol.png', 3: V + 'gul.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Tabiat muammosi',
        'matn': 'Tabiatga yordam berish uchun nima qilish kerak?',
        'rasm': V + 'kesilgan-daraxt.png',
        'variantlar': [('', 'Daraxt ekish', True), ('', 'Axlat tashlash', False),
                       ('', 'Gullarni uzish', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Mantiqiy savol',
        'matn': "Qushlar qishda issiq o'lkalarga nima uchun uchib ketadi?",
        'variantlar': [('', 'Oziq topish va sovuqdan saqlanish uchun.', True),
                       ('', 'Uxlash uchun.', False),
                       ("", "O'ynash uchun.", False)],
    },
    {
        'tur': 'koptanlov',
        'sarlavha': 'Tajribani rejalashtir',
        'matn': "O'simlik o'sishi uchun kerakli narsalarni tanla.",
        'variantlar': [('', 'Quyosh', True), ('', 'Suv', True), ('', 'Tuproq', True),
                       ('', 'Tosh', False), ('', 'Kitob', False)],
        'v_rasm': {1: V + 'quyoshli.png', 2: V + 'suv.png', 3: V + 'tuproq.png',
                   4: V + 'tosh.png', 5: V + 'kitob.png'},
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Mikrofon orqali tushuntir',
        'matn': 'Nima uchun tabiatni asrash kerak? 4–5 ta gap bilan javob ber.',
        'rasm': V + 'ormon.png',
        'izoh': 'Baholash mezoni:\n• 4–5 ta gap.\n• Fikrning mantiqiyligi.\n'
                '• Aniq misollar.',
    },
    {
        'tur': 'koptanlov',
        'sarlavha': 'Tabiat detektivi',
        'matn': 'Rasmlar orasida xatolari bor. Xato rasmlarning hammasini belgila.',
        # Hujjatda bitta rasmdagi 5 ta xato ko'zda tutilgan; bu yerda har bir xato
        # alohida rasmga ajratilgan — bola ularni belgilaydi.
        'variantlar': [('', 'Baliq daraxtda', True), ('', 'Baliq suvda', False),
                       ('', 'Qush suv ostida', True), ('', 'Qush daraxtda', False),
                       ("", "Yozda qor yog'moqda", True), ('', 'Yozda quyosh', False)],
        'v_rasm': {1: V + 'xato-baliq-daraxtda.png', 2: V + 'togri-baliq-suvda.png',
                   3: V + 'xato-qush-suvda.png', 4: V + 'togri-qush-daraxtda.png',
                   5: V + 'xato-qor-yozda.png', 6: V + 'togri-quyosh-yozda.png'},
    },
    {
        'tur': 'kvest',
        'sarlavha': 'Yosh Olim',
        'matn': 'Yakuniy sarguzasht! Ketma-ket 5 ta vazifani bajarasan.',
        'bosqichlar': [
            {
                'tur': 'guruh',
                'sarlavha': "🌿 Jonli va jonsizni ajrat",
                'matn': "Rasmni to'g'ri qutiga joylashtir.",
                'guruh': [
                    ('Gul', V + 'gul.png', 'Jonli', V + 'quti-kok.png'),
                    ('Tosh', V + 'tosh.png', 'Jonsiz', V + 'quti-qizil.png'),
                    ('Baliq', V + 'baliq.png', 'Jonli', V + 'quti-kok.png'),
                    ('Kitob', V + 'kitob.png', 'Jonsiz', V + 'quti-qizil.png'),
                ],
            },
            {
                'tur': 'tanlov',
                'sarlavha': '🧪 Tajribani kuzatib xulosa chiqar',
                'matn': "Muz nima bo'ldi?",
                'rasm': V + 'tajriba-muz.png',
                'variantlar': [('', 'Eridi', True), ('', 'Qotdi', False),
                               ("", "O'sdi", False)],
            },
            {
                'tur': 'moslash',
                'sarlavha': '🦁 Hayvonlarni yashash joyiga joylashtir',
                'matn': "Har bir hayvonni yashash joyi bilan bog'la.",
                'juftlar': [('', 'Pingvin', '', 'Muzlik'), ('', 'Tuya', '', "Cho'l")],
                'v_rasm': {1: V + 'pingvin.png', 2: V + 'tuya.png'},
                'j_rasm': {1: V + 'muzlik.png', 2: V + 'chol.png'},
            },
            {
                'tur': 'tanlov',
                'sarlavha': "🌍 Tabiatni asrash bo'yicha qaror",
                'matn': "Parkda plastik shisha ko'rding. Nima qilasan?",
                'rasm': V + 'plastik-shisha.png',
                'variantlar': [('', 'Chiqindi qutisiga tashlayman.', True),
                               ('', 'Joyida qoldiraman.', False),
                               ('', 'Uzoqroqqa uloqtiraman.', False)],
            },
            {
                'tur': 'mikrofon',
                'sarlavha': '🎤 Tabiat haqida fikr bildir',
                'matn': "Tabiat haqida 3–4 ta gap ayt.",
                'rasm': V + 'ormon.png',
                'izoh': 'Bola ovoz yozadi, tarbiyachi baholaydi.',
            },
        ],
    },
]

BOLIM = {'order': 4, 'name': 'Fan va tabiat', 'emoji': '🌿'}
DARAJALAR = [
    (1, 'oson', '1-daraja — Oson', '🟢', OSON),
    (2, 'orta', "2-daraja — O'rta", '🟡', ORTA),
    (3, 'qiyin', '3-daraja — Qiyin', '🔴', QIYIN),
]


def yoz(Savol, Variant, bolimcha, order, daraja, t, kvest=None):
    savol = Savol.objects.create(
        bolimcha=bolimcha, kvest=kvest, order=order, daraja=daraja,
        tur=t['tur'],
        sarlavha=t.get('sarlavha', ''),
        matn=t['matn'],
        ovoz_matn=t.get('ovoz_matn', ''),
        rasm=t.get('rasm', ''),
        izoh=t.get('izoh', ''),
        byudjet=t.get('byudjet'),
    )

    rasmlar = t.get('v_rasm', {})
    narxlar = t.get('narxlar', {})
    for i, v in enumerate(t.get('variantlar', []), start=1):
        Variant.objects.create(
            savol=savol, order=i, emoji=v[0], matn=v[1], togri=v[2],
            rang=v[3] if len(v) > 3 else '',
            rasm=rasmlar.get(i, ''), narx=narxlar.get(i),
        )

    for i, (emoji, matn) in enumerate(t.get('tartib', []), start=1):
        Variant.objects.create(
            savol=savol, order=i, emoji=emoji, matn=matn, togri_order=i,
            rasm=rasmlar.get(i, ''),
        )

    juft_rasmlar = t.get('j_rasm', {})
    for i, (emoji, matn, jemoji, jmatn) in enumerate(t.get('juftlar', []), start=1):
        Variant.objects.create(
            savol=savol, order=i, emoji=emoji, matn=matn,
            juft_emoji=jemoji, juft_matn=jmatn,
            rasm=rasmlar.get(i, ''), juft_rasm=juft_rasmlar.get(i, ''),
        )

    for i, (matn, rasm, savat, savat_rasm) in enumerate(t.get('guruh', []), start=1):
        Variant.objects.create(
            savol=savol, order=i, matn=matn, rasm=rasm,
            juft_matn=savat, juft_rasm=savat_rasm,
        )

    for i, (matn, rasm, slot, oldindan) in enumerate(t.get('qurish', []), start=1):
        Variant.objects.create(
            savol=savol, order=i, matn=matn, rasm=rasm,
            slot=slot, togri_order=i, oldindan=oldindan,
        )

    for i, bosqich in enumerate(t.get('bosqichlar', []), start=1):
        yoz(Savol, Variant, bolimcha, i, daraja, bosqich, kvest=savol)

    return savol


def seed(apps, schema_editor):
    Bolim = apps.get_model('home', 'Bolim')
    Bolimcha = apps.get_model('home', 'Bolimcha')
    Savol = apps.get_model('home', 'Savol')
    Variant = apps.get_model('home', 'Variant')

    bolim = Bolim.objects.get(order=BOLIM['order'])
    bolim.name = BOLIM['name']
    bolim.emoji = BOLIM['emoji']
    bolim.save()

    Savol.objects.filter(bolimcha__bolim=bolim).delete()

    for sub_order, daraja, nom, emoji, topshiriqlar in DARAJALAR:
        sub, _ = Bolimcha.objects.get_or_create(
            bolim=bolim, order=sub_order, defaults={'name': nom, 'emoji': emoji})
        sub.name = nom
        sub.emoji = emoji
        sub.save()
        for order, t in enumerate(topshiriqlar, start=1):
            yoz(Savol, Variant, sub, order, daraja, t)


def unseed(apps, schema_editor):
    Bolim = apps.get_model('home', 'Bolim')
    Savol = apps.get_model('home', 'Savol')
    Savol.objects.filter(bolimcha__bolim=Bolim.objects.get(order=4)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_seed_rolli_oyinlar'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
