"""1-bo'lim — "TIL VA NUTQ" topshiriqlari, hujjatdagidek to'liq.

Manba: "Bilimbo platformasi uchun topshiriqlari.docx", "Yo'nalish TIL VA NUTQ" bo'limi.
Hujjatdagi variantlar soni, matnlar va topshiriq turlari (drag & drop, moslashtirish,
mikrofon, audio) o'zgartirilmagan holda saqlangan.
"""
from django.db import migrations

RASM = 'images/topshiriq/'
VRASM = 'images/topshiriq/variantlar/'
AUDIO = 'audio/topshiriq/'

# tur: tanlov | tartib | moslash | mikrofon | kvest
#   variantlar : (emoji, matn, to'g'rimi) yoki (emoji, matn, to'g'rimi, rang)
#   v_rasm     : variant tartibi -> rasm yo'li. Rasm berilgan variantda ekranda
#                faqat rasm ko'rinadi (matn ekran o'quvchilar uchun qoladi).
#   tartib     : (emoji, matn) — ro'yxat to'g'ri ketma-ketlikda beriladi
#   juftlar    : (emoji, matn, juft_emoji, juft_matn)
#   bosqichlar : ichma-ich topshiriqlar (faqat kvest uchun)

OSON = [
    {
        'tur': 'tanlov',
        'sarlavha': 'Rasmni tanla',
        'matn': 'Olmani top.',
        # Bu topshiriqda variantlar faqat rasmdan iborat — bola rasmni tanib,
        # matnga suyanmasdan javob berishi kerak.
        'variantlar': [
            ('', 'Olma', True),
            ('', 'Banan', False),
            ('', 'Mashina', False),
            ('', 'It', False),
        ],
        'v_rasm': {
            1: VRASM + 'olma.png',
            2: VRASM + 'banan.png',
            3: VRASM + 'mashina.png',
            4: VRASM + 'it.png',
        },
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Ovozni eshit va top',
        'matn': 'Ovozni eshit va kimniki ekanini top.',
        # Haqiqiy miyov ovozi. Matnni ovozga berib bo'lmaydi — "Mushuk miyovladi"
        # deb o'qilsa, javob bolaga aytib qo'yiladi.
        'audio_fayl': AUDIO + 'mushuk-miyovlashi.wav',
        'audio_matn': 'Mushuk miyovladi.',
        'variantlar': [
            ('', 'Mushuk', True),
            ('', 'Sigir', False),
            ('', 'Tovuq', False),
            ('', 'It', False),
        ],
        'v_rasm': {1: VRASM + 'mushuk.png', 2: VRASM + 'sigir.png',
                   3: VRASM + 'tovuq.png', 4: VRASM + 'it.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Harfni tanla',
        'matn': 'Qaysi harf A?',
        'variantlar': [
            ('', 'B', False),
            ('', 'M', False),
            ('', 'A', True),
            ('', 'T', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Rangni top',
        'matn': 'Qizil rangni tanla.',
        'variantlar': [
            ('', 'Qizil', True, '#e94b4b'),
            ('', "Ko'k", False, '#3d7be0'),
            ('', 'Yashil', False, '#4caf50'),
            ('', 'Sariq', False, '#f2c230'),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kim ortiqcha?',
        'matn': 'Qaysi biri ortiqcha?',
        'variantlar': [
            ('', 'Olma', False),
            ('', 'Nok', False),
            ('', 'Banan', False),
            ('', 'Velosiped', True),
        ],
        'v_rasm': {1: VRASM + 'olma.png', 2: VRASM + 'nok.png',
                   3: VRASM + 'banan.png', 4: VRASM + 'velosiped.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': "So'zni tugat",
        'matn': 'OL _ A',
        'ovoz_matn': "O L, bo'sh joy, A. Bo'sh joyga qaysi harf mos keladi?",
        'variantlar': [
            ('', 'M', True),
            ('', 'B', False),
            ('', 'S', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Sanab top',
        'matn': '⭐️⭐️⭐️⭐️⭐️\nNechta yulduz bor?',
        'ovoz_matn': 'Nechta yulduz bor?',
        'variantlar': [
            ('', '3', False),
            ('', '4', False),
            ('', '5', True),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Mosini top',
        'matn': '🐶 → ?',
        'ovoz_matn': 'It nima qiladi?',
        'variantlar': [
            ('', 'Huradi', True),
            ('', 'Uchadi', False),
            ('', 'Suzadi', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Birinchi tovush',
        'matn': '"Anor"\nQaysi tovush bilan boshlanadi?',
        'ovoz_matn': 'Anor. Qaysi tovush bilan boshlanadi?',
        'variantlar': [
            ('', 'A', True),
            ('', 'O', False),
            ('', 'N', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Gapni tanla',
        'matn': 'Rasmga mos gapni tanla.',
        'rasm': RASM + 'bola-kitob-oqiyapti.png',
        'variantlar': [
            ('', "Bola kitob o'qiyapti.", True),
            ('', 'Bola uxlayapti.', False),
            ('', 'Bola yuguryapti.', False),
        ],
    },
]

ORTA = [
    {
        'tur': 'tartib',
        'sarlavha': 'Ketma-ketlikni joylashtir',
        'matn': 'Rasmlarni voqea ketma-ketligida joylashtir.',
        'tartib': [
            ('', "Urug'"),
            ('', 'Nihol'),
            ('', 'Gul'),
            ('', 'Daraxt'),
        ],
        'v_rasm': {1: VRASM + 'urug.png', 2: VRASM + 'nihol.png',
                   3: VRASM + 'gul.png', 4: VRASM + 'daraxt.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': "So'zni bo'g'inlarga ajrat",
        'matn': '"Olma" so\'zi nechta bo\'g\'indan iborat?',
        'variantlar': [
            ('', '1', False),
            ('', '2', True),
            ('', '3', False),
        ],
    },
    {
        'tur': 'moslash',
        'sarlavha': 'Moslashtir',
        'matn': 'Hayvonlarni yashash joyi bilan bog\'la.',
        'juftlar': [
            ('', 'Baliq', '', 'Suv'),
            ('', 'Qush', '', 'Daraxt'),
            ('', 'Tuya', '', "Cho'l"),
        ],
        'v_rasm': {1: VRASM + 'baliq.png', 2: VRASM + 'qush.png',
                   3: VRASM + 'tuya.png'},
        'j_rasm': {1: VRASM + 'suv.png', 2: VRASM + 'daraxt.png',
                   3: VRASM + 'chol.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Audio tingla va javob ber',
        'matn': 'Bugun ob-havo qanday?',
        'audio_matn': 'Bugun havo quyoshli.',
        'variantlar': [
            ('', "Yomg'irli", False),
            ('', 'Quyoshli', True),
            ('', 'Qorli', False),
        ],
        'v_rasm': {1: VRASM + 'yomgirli.png', 2: VRASM + 'quyoshli.png',
                   3: VRASM + 'qorli.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Yetishmayotgan harfni top',
        'matn': 'B _ L I Q',
        'ovoz_matn': "B, bo'sh joy, L I Q. Bo'sh joyga qaysi harf mos keladi?",
        'variantlar': [
            ('', 'A', True),
            ('', 'O', False),
            ('', 'E', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Nima bilan boshlanadi?',
        'matn': 'Qaysi rasm "S" harfi bilan boshlanadi?',
        'variantlar': [
            ('', 'Sher', True),
            ('', 'Olma', False),
            ('', 'Mashina', False),
            ('', 'Baliq', False),
        ],
        'v_rasm': {1: VRASM + 'sher.png', 2: VRASM + 'olma.png',
                   3: VRASM + 'mashina.png', 4: VRASM + 'baliq.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': "To'g'ri gapni tanla",
        'matn': 'Rasmga mos gapni tanla.',
        'rasm': RASM + 'qiz-gul-sugormoqda.png',
        'variantlar': [
            ('', "Qiz gul sug'ormoqda.", True),
            ('', "Qiz futbol o'ynayapti.", False),
            ('', 'Qiz uxlayapti.', False),
        ],
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Mikrofon orqali javob ber',
        'matn': "O'zing yoqtirgan meva haqida 2–3 ta gap ayt.",
        'izoh': 'Bola ovoz yozadi, platforma yoki tarbiyachi baholaydi.',
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Xatoni top',
        'matn': '"Baliq daraxtda yashaydi."',
        'ovoz_matn': "Baliq daraxtda yashaydi. Bu gap to'g'rimi?",
        'variantlar': [
            ('', "To'g'ri", False),
            ('', "Noto'g'ri", True),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Hikoyani yakunla',
        'matn': '"Quyon o\'rmonda sayr qilayotgan edi. Birdan..."',
        'variantlar': [
            ('', "Do'stini uchratdi.", True),
            ('', 'Mashina haydadi.', False),
            ('', 'Samolyot uchirdi.', False),
        ],
    },
]

QIYIN = [
    {
        'tur': 'tartib',
        'sarlavha': "Hikoyani to'ldir",
        'matn': "Gaplarni to'g'ri ketma-ketlikda joylashtir.",
        'izoh': 'Tavsiya: voqealar ketma-ketligi aniq bo\'lishi uchun '
                'rasmlarni mos ravishda tayyorlang.',
        # Bu topshiriqda gaplarning o'zi mazmun — shuning uchun rasm bilan
        # birga matn ham ko'rsatiladi.
        'variant_matni_korinsin': True,
        'tartib': [
            ('', "O'rmonga bordi."),
            ('', "Sabzi yig'di."),
            ('', 'Savatni oldi.'),
            ('', 'Uyiga xursand qaytdi.'),
        ],
        'v_rasm': {1: VRASM + 'ormon.png', 2: VRASM + 'sabzi.png',
                   3: VRASM + 'savat.png', 4: VRASM + 'uy.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Ortiqcha gapni top',
        'matn': 'Qaysi gap ortiqcha?',
        'variantlar': [
            ('', 'Mushuk sut ichadi.', False),
            ('', 'Mushuk sichqon tutadi.', False),
            ('', 'Mushuk daraxt ekadi.', True),
            ('', 'Mushuk miyovlaydi.', False),
        ],
    },
    {
        'tur': 'tartib',
        'sarlavha': "So'zlardan gap tuz",
        'matn': "Kartochkalarni surib to'g'ri gap tuz.",
        'tartib': [
            ('', 'bola'),
            ('', 'kitob'),
            ('', "o'qiyapti"),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Rasmga mos sarlavhani tanla',
        'matn': 'Rasmga mos sarlavhani tanla.',
        'rasm': RASM + 'bolalar-daraxt-ekmoqda.png',
        'variantlar': [
            ('', 'Tabiatni asraymiz.', True),
            ('', "Qishda qor yog'di.", False),
            ('', 'Bozorda sayr.', False),
        ],
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Mikrofon orqali hikoya qil',
        'matn': "Rasmga qarab 5–6 ta gapdan iborat hikoya ayt.",
        'rasm': RASM + 'bolalar-bogda.png',
        'izoh': 'Baholash mezoni:\n• Gaplar mantiqiyligi.\n• To\'g\'ri talaffuz.\n'
                '• To\'liq gaplardan foydalanish.\n• So\'z boyligi.',
    },
    {
        'tur': 'tanlov',
        'sarlavha': "Ma'nodosh so'zni top",
        'matn': '"Chiroyli" so\'ziga yaqin ma\'noli so\'zni tanla.',
        'variantlar': [
            ('', "Go'zal", True),
            ('', 'Sovuq', False),
            ('', 'Katta', False),
            ('', 'Qora', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': "Qarama-qarshi ma'noni top",
        'matn': '"Baland" so\'zining qarama-qarshi ma\'nosi qaysi?',
        'variantlar': [
            ('', 'Past', True),
            ('', 'Tez', False),
            ('', 'Issiq', False),
            ('', 'Keng', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Topishmoqni yech',
        'matn': "O'zi kichkina,\nDumi uzun,\nPishloqni yaxshi ko'radi.",
        'variantlar': [
            ('', 'Sichqon', True),
            ('', 'Mushuk', False),
            ('', 'Quyon', False),
            ('', 'It', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Mantiqiy savol',
        'matn': 'Qushlar nima uchun uya quradi?',
        'variantlar': [
            ('', 'Dam olish uchun.', False),
            ('', 'Bolalarini parvarish qilish uchun.', True),
            ('', 'Baliq tutish uchun.', False),
            ('', 'Yugurish uchun.', False),
        ],
    },
    {
        'tur': 'kvest',
        'sarlavha': 'Til sarguzashti',
        'matn': "Yakuniy sarguzasht! Ketma-ket 5 ta vazifani bajarasan.",
        'bosqichlar': [
            {
                'tur': 'tanlov',
                'sarlavha': '🔊 Audioni tinglab javob ber',
                'matn': 'Bu qaysi hayvonning ovozi?',
                'audio_fayl': AUDIO + 'sigir-movrashi.wav',
                'audio_matn': "Sigir mo'radi.",
                'variantlar': [
                    ('', 'Sigir', True),
                    ('', 'It', False),
                    ('', 'Mushuk', False),
                ],
                'v_rasm': {1: VRASM + 'sigir.png', 2: VRASM + 'it.png',
                           3: VRASM + 'mushuk.png'},
            },
            {
                'tur': 'tartib',
                'sarlavha': "🧩 So'zlardan gap tuz",
                'matn': "Kartochkalarni surib to'g'ri gap tuz.",
                'tartib': [
                    ('', 'quyon'),
                    ('', 'sabzi'),
                    ('', 'yedi'),
                ],
            },
            {
                'tur': 'tanlov',
                'sarlavha': '🖼️ Rasmga mos sarlavhani tanla',
                'matn': 'Rasmga mos sarlavhani tanla.',
                'rasm': RASM + 'bolalar-daraxt-ekmoqda.png',
                'variantlar': [
                    ('', 'Tabiatni asraymiz.', True),
                    ('', 'Bozorda sayr.', False),
                    ('', "Qishda qor yog'di.", False),
                ],
            },
            {
                'tur': 'mikrofon',
                'sarlavha': '🎤 Mikrofon orqali 5 ta gap ayt',
                'matn': "O'zing yoqtirgan o'yin haqida 5 ta gap ayt.",
                'izoh': 'Bola ovoz yozadi, tarbiyachi baholaydi.',
            },
            {
                'tur': 'tanlov',
                'sarlavha': '🧠 Topishmoqni yech',
                'matn': "Yozda ko'm-ko'k kiyinadi,\nQishda yalang'och qoladi.",
                'variantlar': [
                    ('', 'Daraxt', True),
                    ('', 'Tosh', False),
                    ('', 'Kitob', False),
                ],
                'v_rasm': {1: VRASM + 'daraxt.png', 2: VRASM + 'tosh.png',
                           3: VRASM + 'kitob.png'},
            },
        ],
    },
]

DARAJALAR = [(1, 'oson', OSON), (2, 'orta', ORTA), (3, 'qiyin', QIYIN)]


def yoz(Savol, Variant, bolimcha, order, daraja, t, kvest=None):
    savol = Savol.objects.create(
        bolimcha=bolimcha,
        kvest=kvest,
        order=order,
        daraja=daraja,
        tur=t['tur'],
        sarlavha=t.get('sarlavha', ''),
        matn=t['matn'],
        ovoz_matn=t.get('ovoz_matn', ''),
        audio_matn=t.get('audio_matn', ''),
        audio_fayl=t.get('audio_fayl', ''),
        rasm=t.get('rasm', ''),
        izoh=t.get('izoh', ''),
        variant_matni_korinsin=t.get('variant_matni_korinsin', False),
    )

    rasmlar = t.get('v_rasm', {})
    for i, v in enumerate(t.get('variantlar', []), start=1):
        emoji, matn, togri = v[0], v[1], v[2]
        Variant.objects.create(
            savol=savol, order=i, emoji=emoji, matn=matn,
            togri=togri, rang=v[3] if len(v) > 3 else '',
            rasm=rasmlar.get(i, ''),
        )

    # Ro'yxat to'g'ri ketma-ketlikda berilgan; ekranda aralashtirib ko'rsatiladi
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

    for i, bosqich in enumerate(t.get('bosqichlar', []), start=1):
        yoz(Savol, Variant, bolimcha, i, daraja, bosqich, kvest=savol)

    return savol


def seed(apps, schema_editor):
    Bolim = apps.get_model('home', 'Bolim')
    Bolimcha = apps.get_model('home', 'Bolimcha')
    Savol = apps.get_model('home', 'Savol')
    Variant = apps.get_model('home', 'Variant')

    bolim = Bolim.objects.get(order=1)
    # Eski namunaviy savollar (natijalari bilan birga) o'rniga hujjatdagilari yoziladi
    Savol.objects.filter(bolimcha__bolim=bolim).delete()

    for sub_order, daraja, topshiriqlar in DARAJALAR:
        sub = Bolimcha.objects.get(bolim=bolim, order=sub_order)
        for order, t in enumerate(topshiriqlar, start=1):
            yoz(Savol, Variant, sub, order, daraja, t)


def unseed(apps, schema_editor):
    Bolim = apps.get_model('home', 'Bolim')
    Savol = apps.get_model('home', 'Savol')
    Savol.objects.filter(bolimcha__bolim=Bolim.objects.get(order=1)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_savol_variant_matni'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
