"""2-bo'lim — "QURISH-YASASH, KONSTRUKSIYALASH VA MATEMATIKA MARKAZI".

Manba: "Bilimbo platformasi uchun topshiriqlari.docx".
Hujjatdagi 3 daraja x 10 topshiriq. Bu bo'limdagi tasvirlar (shakllar, kublar,
naqshlar, konstruksiya namunalari) chizib tayyorlangan — ular geometrik bo'lgani
uchun chizilgani aniqroq va bir xil uslubda chiqadi.
"""
from django.db import migrations

V = 'images/topshiriq/variantlar/'

# tur: tanlov | tartib | moslash | guruh | qurish | kvest
#   variantlar : (emoji, matn, to'g'rimi)      + v_rasm {tartib raqami: rasm}
#   tartib     : (emoji, matn)                 — to'g'ri ketma-ketlikda
#   juftlar    : (emoji, matn, juft emoji, juft matn) + v_rasm / j_rasm
#   guruh      : (matn, rasm, savat nomi, savat rasmi)
#   qurish     : (matn, rasm, uya "x,y,w,h", oldindan qo'yilganmi)

OSON = [
    {
        'tur': 'tanlov',
        'sarlavha': 'Shaklni top',
        'matn': 'Kvadratni tanla.',
        'variantlar': [('', 'Kvadrat', True), ('', 'Uchburchak', False),
                       ('', 'Doira', False), ('', 'Yulduz', False)],
        'v_rasm': {1: V + 'shakl-kvadrat.png', 2: V + 'shakl-uchburchak.png',
                   3: V + 'shakl-doira.png', 4: V + 'shakl-yulduz.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Sanab javob ber',
        'matn': 'Ekranda nechta olma bor?',
        'rasm': V + 'sanoq-olma-6.png',
        'variantlar': [('', '5', False), ('', '6', True), ('', '7', False)],
    },
    {
        'tur': 'guruh',
        'sarlavha': 'Rangiga qarab ajrat',
        'matn': "Qizil kublarni qizil qutiga, ko'k kublarni ko'k qutiga joylashtir.",
        'guruh': [
            ('Qizil kub', V + 'kub-qizil.png', 'Qizil quti', V + 'quti-qizil.png'),
            ("Ko'k kub", V + 'kub-kok.png', "Ko'k quti", V + 'quti-kok.png'),
            ('Qizil kub', V + 'kub-qizil.png', 'Qizil quti', V + 'quti-qizil.png'),
            ("Ko'k kub", V + 'kub-kok.png', "Ko'k quti", V + 'quti-kok.png'),
            ('Qizil kub', V + 'kub-qizil.png', 'Qizil quti', V + 'quti-qizil.png'),
            ("Ko'k kub", V + 'kub-kok.png', "Ko'k quti", V + 'quti-kok.png'),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kattasini tanla',
        'matn': 'Qaysi biri katta?',
        'variantlar': [('', 'Fil', True), ('', 'Sichqon', False)],
        'v_rasm': {1: V + 'fil.png', 2: V + 'sichqon.png'},
    },
    {
        'tur': 'moslash',
        'sarlavha': 'Shakl soyasini top',
        'matn': 'Har bir shaklni o\'z soyasi bilan bog\'la.',
        'juftlar': [('', 'Doira', '', 'Doira soyasi'),
                    ('', 'Uchburchak', '', 'Uchburchak soyasi'),
                    ('', 'Kvadrat', '', 'Kvadrat soyasi')],
        'v_rasm': {1: V + 'shakl-doira.png', 2: V + 'shakl-uchburchak.png',
                   3: V + 'shakl-kvadrat.png'},
        'j_rasm': {1: V + 'soya-doira.png', 2: V + 'soya-uchburchak.png',
                   3: V + 'soya-kvadrat.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Ketma-ket sanash',
        'matn': '1, 2, 3, __, 5',
        'ovoz_matn': "Bir, ikki, uch, bo'sh joy, besh. Bo'sh joyga qaysi son mos keladi?",
        'variantlar': [('', '4', True), ('', '6', False), ('', '7', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': "O'ng va chapni top",
        'matn': "O'ng tomondagi kubni bos.",
        # Ikkala kub ham bir xil — faqat joyi muhim
        'variantlar': [('', 'Chapdagi kub', False), ('', "O'ngdagi kub", True)],
        'v_rasm': {1: V + 'kub-kok.png', 2: V + 'kub-kok.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Baland minorani tanla',
        'matn': 'Eng baland minorani tanla.',
        'variantlar': [('', 'Past minora', False), ('', 'Baland minora', True),
                       ("", "O'rtacha minora", False)],
        'v_rasm': {1: V + 'minora-past.png', 2: V + 'minora-baland.png',
                   3: V + 'minora-orta.png'},
    },
    {
        'tur': 'moslash',
        'sarlavha': 'Juftini top',
        'matn': 'Mos juftlarni bir-biriga bog\'la.',
        'juftlar': [("", "Qo'lqop", '', "Qo'lqop"), ('', 'Paypoq', '', 'Paypoq'),
                    ('', 'Poyabzal', '', 'Poyabzal')],
        'v_rasm': {1: V + 'qolqop.png', 2: V + 'paypoq.png', 3: V + 'poyabzal.png'},
        'j_rasm': {1: V + 'qolqop.png', 2: V + 'paypoq.png', 3: V + 'poyabzal.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Yetishmayotgan shakl',
        'matn': "Bo'sh joyga qaysi shakl mos keladi?",
        'rasm': V + 'naqsh-kvadrat-uchburchak.png',
        'variantlar': [('', 'Kvadrat', True), ('', 'Doira', False),
                       ('', 'Yulduz', False)],
        'v_rasm': {1: V + 'shakl-kvadrat.png', 2: V + 'shakl-doira.png',
                   3: V + 'shakl-yulduz.png'},
    },
]

ORTA = [
    {
        'tur': 'tanlov',
        'sarlavha': 'Naqshni davom ettir',
        'matn': "Naqshni davom ettir: bo'sh joyga qaysi shakl keladi?",
        'rasm': V + 'naqsh-kok-qizil.png',
        'variantlar': [("", "Ko'k kvadrat", True), ('', 'Qizil kvadrat', False)],
        'v_rasm': {1: V + 'shakl-kvadrat.png', 2: V + 'shakl-kvadrat-qizil.png'},
    },
    {
        'tur': 'qurish',
        'sarlavha': "Konstruktor yig'",
        'matn': "Namunadagi uyni bloklardan yig'.",
        'rasm': V + 'namuna-uy.png',
        'qurish': [
            ('Tom', V + 'bolak-uchburchak-qizil-56x30.png', '22,4,56,30', False),
            ('Chap devor', V + 'bolak-kvadrat-kok-26x30.png', '24,36,26,30', False),
            ("O'ng devor", V + 'bolak-kvadrat-kok-26x30.png', '50,36,26,30', False),
            ('Eshik', V + 'bolak-tortburchak-jigar-16x16.png', '42,50,16,16', False),
        ],
    },
    {
        'tur': 'tartib',
        'sarlavha': 'Sonlarni tartibla',
        'matn': 'Sonlarni kichikdan kattaga joylashtir.',
        'tartib': [('', '1'), ('', '3'), ('', '5'), ('', '7')],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Teng miqdorni top',
        'matn': 'Bir tomonda 8 ta kub bor. Ikkinchi tomondan ham 8 ta kubni tanla.',
        'rasm': V + 'sanoq-kub-8.png',
        'variantlar': [('', '6 ta kub', False), ('', '8 ta kub', True),
                       ('', '10 ta kub', False)],
        'v_rasm': {1: V + 'sanoq-kub-6.png', 2: V + 'sanoq-kub-8.png',
                   3: V + 'sanoq-kub-10.png'},
    },
    {
        'tur': 'labirint',
        'sarlavha': 'Labirint',
        'matn': "Robotni uyigacha olib bor.",
        # # devor, nuqta yo'l, R robot, H uy.
        # Mukammal labirint: har ikki katak orasida aynan bitta yo'l bor,
        # ya'ni noto'g'ri burilish albatta boshi berk yo'lga olib boradi.
        # 18 yurish, 5 ta boshi berk yo'l.
        'labirint': '\n'.join([
            '###########',
            '#R#.......#',
            '#.###.#.###',
            '#...#.#...#',
            '###.#####.#',
            '#.#.#.....#',
            '#.#.#.###.#',
            '#.....#..H#',
            '###########',
        ]),
    },
    {
        'tur': 'tanlov',
        'sarlavha': "Qaysi biri og'ir?",
        'matn': "Qaysi biri og'ir?",
        'variantlar': [("", "To'p", False), ('', 'Tosh', True)],
        'v_rasm': {1: V + 'top.png', 2: V + 'tosh.png'},
    },
    {
        'tur': 'qurish',
        'sarlavha': 'Geometrik figuradan rasm yasash',
        'matn': "Doira, kvadrat va uchburchaklardan robot yasa.",
        'rasm': V + 'namuna-robot.png',
        'qurish': [
            ('Bosh', V + 'bolak-doira-sariq-28x26.png', '36,2,28,26', False),
            ('Tana', V + 'bolak-tortburchak-kok-40x30.png', '30,28,40,30', False),
            ("Chap qo'l", V + 'bolak-kvadrat-yashil-15x15.png', '14,30,15,15', False),
            ("O'ng qo'l", V + 'bolak-kvadrat-yashil-15x15.png', '71,30,15,15', False),
            ('Chap oyoq', V + 'bolak-uchburchak-tosariq-17x20.png', '31,58,17,20', False),
            ("O'ng oyoq", V + 'bolak-uchburchak-tosariq-17x20.png', '52,58,17,20', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Misolni yech',
        'matn': '4 + 3 = ?',
        'ovoz_matn': "To'rt qo'shuv uch necha bo'ladi?",
        'variantlar': [('', '6', False), ('', '7', True), ('', '8', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Taqqosla',
        'matn': '9 __ 6',
        'ovoz_matn': "To'qqiz va olti. Bo'sh joyga qaysi belgi mos keladi?",
        'variantlar': [('', 'Katta', True), ('', 'Kichik', False)],
        'v_rasm': {1: V + 'belgi-katta.png', 2: V + 'belgi-kichik.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Yetishmayotgan son',
        'matn': '2, 4, 6, __, 10',
        'ovoz_matn': "Ikki, to'rt, olti, bo'sh joy, o'n. Bo'sh joyga qaysi son mos keladi?",
        'variantlar': [('', '7', False), ('', '8', True), ('', '9', False)],
    },
]

QIYIN = [
    {
        'tur': 'qurish',
        'sarlavha': '3D konstruktor',
        'matn': "Namunadagi qasrni bloklardan yig'. Bloklar soni va joylashuvi "
                "bir xil bo'lishi kerak.",
        'rasm': V + 'namuna-qasr.png',
        'qurish': [
            ('Chap minora tomi', V + 'bolak-uchburchak-qizil-22x20.png', '6,6,22,20', False),
            ("O'ng minora tomi", V + 'bolak-uchburchak-qizil-22x20.png', '72,6,22,20', False),
            ('Chap minora', V + 'bolak-kvadrat-kulrang-18x40.png', '8,26,18,40', False),
            ("O'ng minora", V + 'bolak-kvadrat-kulrang-18x40.png', '74,26,18,40', False),
            ("O'rta devor", V + 'bolak-tortburchak-kulrang-48x26.png', '26,40,48,26', False),
            ('Darvoza', V + 'bolak-tortburchak-jigar-14x16.png', '43,50,14,16', False),
        ],
    },
    {
        'tur': 'qurish',
        'sarlavha': "Simmetriyani to'ldir",
        'matn': "Rasmning chap yarmi berilgan. O'ng yarmini xuddi shunday to'ldir.",
        'rasm': V + 'namuna-simmetriya.png',
        'qurish': [
            ('Chap uchburchak', V + 'bolak-uchburchak-qizil-20x24.png', '28,10,20,24', True),
            ('Chap doira', V + 'bolak-doira-sariq-16x16.png', '30,36,16,16', True),
            ('Chap kvadrat', V + 'bolak-kvadrat-binafsha-24x22.png', '26,54,24,22', True),
            ("O'ng uchburchak", V + 'bolak-uchburchak-qizil-20x24.png', '52,10,20,24', False),
            ("O'ng doira", V + 'bolak-doira-sariq-16x16.png', '54,36,16,16', False),
            ("O'ng kvadrat", V + 'bolak-kvadrat-binafsha-24x22.png', '50,54,24,22', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Murakkab naqsh',
        'matn': "Naqshni davom ettir: bo'sh joydan keyin qaysi ketma-ketlik keladi?",
        'rasm': V + 'naqsh-murakkab.png',
        'variantlar': [("", 'Uchburchak, kvadrat, kvadrat', True),
                       ('', 'Kvadrat, kvadrat, uchburchak', False),
                       ('', 'Kvadrat, uchburchak, kvadrat', False)],
        'v_rasm': {1: V + 'javob-uch-kvadrat-kvadrat.png',
                   2: V + 'javob-kvadrat-kvadrat-uch.png',
                   3: V + 'javob-kvadrat-uch-kvadrat.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Mantiqiy masala',
        'matn': "Azizda 5 ta kub bor edi. U yana 4 ta kub oldi.\n"
                "Keyin 2 tasini ukasiga berdi.\nAzizda nechta kub qoldi?",
        'variantlar': [('', '7', True), ('', '8', False), ('', '9', False)],
    },
    {
        'tur': 'tartib',
        'sarlavha': 'Robotni dasturla',
        'matn': "Robot xaritadagi yo'l bilan bayroqchagacha borishi kerak.\n"
                "Buyruqlarni shu yo'l bo'yicha ketma-ket joylashtir.",
        # Xaritasiz bu topshiriqni yechib bo'lmaydi — qaysi tartib to'g'ri
        # ekanini bola aynan shu yo'lga qarab aniqlaydi
        'rasm': V + 'yol-robot-4.png',
        'tartib': [('', 'Yuqoriga'), ("", "O'ngga"), ("", "O'ngga"), ('', 'Pastga')],
        'v_rasm': {1: V + 'strelka-yuqori.png', 2: V + 'strelka-ong.png',
                   3: V + 'strelka-ong.png', 4: V + 'strelka-past.png'},
    },
    {
        'tur': 'tartib',
        'sarlavha': "O'lchov",
        'matn': 'Qalamlarni eng uzunidan eng qisqasigacha tartibla.',
        'tartib': [('', 'Uzun qalam'), ("", "O'rtacha qalam"), ('', 'Qisqa qalam')],
        'v_rasm': {1: V + 'qalam-uzun.png', 2: V + 'qalam-orta.png',
                   3: V + 'qalam-qisqa.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Geometrik tahlil',
        'matn': 'Uy rasmini yasash uchun nechta kvadrat va nechta uchburchak '
                'ishlatilgan?',
        'rasm': V + 'namuna-uy.png',
        'variantlar': [('', '2 ta kvadrat, 1 ta uchburchak', True),
                       ('', '3 ta kvadrat, 1 ta uchburchak', False),
                       ('', '2 ta kvadrat, 2 ta uchburchak', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Son qonuniyatini top',
        'matn': '3, 6, 9, 12, __',
        'ovoz_matn': "Uch, olti, to'qqiz, o'n ikki, bo'sh joy. Keyingi son qaysi?",
        'variantlar': [('', '13', False), ('', '14', False), ('', '15', True)],
    },
    {
        'tur': 'qurish',
        'sarlavha': 'Qurilish loyihasi',
        'matn': "2 ta kvadrat, 3 ta to'rtburchak va 1 ta uchburchakdan ko'prik yasa.",
        'rasm': V + 'namuna-koprik.png',
        'qurish': [
            ("Cho'qqi", V + 'bolak-uchburchak-qizil-20x18.png', '40,4,20,18', False),
            ("Yo'lak (chap)", V + 'bolak-tortburchak-kok-26x12.png', '10,24,26,12', False),
            ("Yo'lak (o'rta)", V + 'bolak-tortburchak-kok-26x12.png', '37,24,26,12', False),
            ("Yo'lak (o'ng)", V + 'bolak-tortburchak-kok-26x12.png', '64,24,26,12', False),
            ('Chap ustun', V + 'bolak-kvadrat-kulrang-20x28.png', '16,38,20,28', False),
            ("O'ng ustun", V + 'bolak-kvadrat-kulrang-20x28.png', '64,38,20,28', False),
        ],
    },
    {
        'tur': 'kvest',
        'sarlavha': 'STEM sarguzashti',
        'matn': 'Yakuniy sarguzasht! Ketma-ket 5 ta vazifani bajarasan.',
        'bosqichlar': [
            {
                'tur': 'qurish',
                'sarlavha': "🧩 Konstruktor yig'",
                'matn': "Namunadagi minorani bloklardan yig'.",
                'rasm': V + 'namuna-minorabop.png',
                'qurish': [
                    ('Tom', V + 'bolak-uchburchak-qizil-34x24.png', '33,6,34,24', False),
                    ('Yuqori blok', V + 'bolak-kvadrat-kok-30x18.png', '35,30,30,18', False),
                    ('Pastki blok', V + 'bolak-kvadrat-kok-30x18.png', '35,48,30,18', False),
                ],
            },
            {
                'tur': 'tanlov',
                'sarlavha': '🔢 Matematik misolni yech',
                'matn': '5 + 2 = ?',
                'ovoz_matn': "Besh qo'shuv ikki necha bo'ladi?",
                'variantlar': [('', '6', False), ('', '7', True), ('', '8', False)],
            },
            {
                'tur': 'tanlov',
                'sarlavha': '📐 Naqshni davom ettir',
                'matn': "Bo'sh joyga qaysi shakl mos keladi?",
                'rasm': V + 'naqsh-kvadrat-uchburchak.png',
                'variantlar': [('', 'Kvadrat', True), ('', 'Doira', False),
                               ('', 'Yulduz', False)],
                'v_rasm': {1: V + 'shakl-kvadrat.png', 2: V + 'shakl-doira.png',
                           3: V + 'shakl-yulduz.png'},
            },
            {
                'tur': 'tartib',
                'sarlavha': "🤖 Robot yo'lini tuz",
                'matn': "Xaritadagi yo'l bo'yicha buyruqlarni joylashtir.",
                'rasm': V + 'yol-robot-3.png',
                'tartib': [('', 'Yuqoriga'), ("", "O'ngga"), ('', 'Pastga')],
                'v_rasm': {1: V + 'strelka-yuqori.png', 2: V + 'strelka-ong.png',
                           3: V + 'strelka-past.png'},
            },
            {
                'tur': 'qurish',
                'sarlavha': '🏗️ Yangi inshoot yarat',
                'matn': "Berilgan shakllardan namunadagi inshootni yasa.",
                'rasm': V + 'namuna-inshoot.png',
                'qurish': [
                    ('Gumbaz', V + 'bolak-doira-sariq-16x16.png', '42,2,16,16', False),
                    ('Tepa qavat', V + 'bolak-tortburchak-yashil-60x14.png', '20,20,60,14', False),
                    ('Chap ustun', V + 'bolak-kvadrat-binafsha-22x30.png', '24,36,22,30', False),
                    ("O'ng ustun", V + 'bolak-kvadrat-binafsha-22x30.png', '54,36,22,30', False),
                ],
            },
        ],
    },
]

BOLIM = {'order': 2, 'name': 'Qurish-yasash va matematika', 'emoji': '🧱'}
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
        audio_matn=t.get('audio_matn', ''),
        audio_fayl=t.get('audio_fayl', ''),
        rasm=t.get('rasm', ''),
        izoh=t.get('izoh', ''),
        labirint=t.get('labirint', ''),
        variant_matni_korinsin=t.get('variant_matni_korinsin', False),
    )

    rasmlar = t.get('v_rasm', {})
    for i, v in enumerate(t.get('variantlar', []), start=1):
        Variant.objects.create(
            savol=savol, order=i, emoji=v[0], matn=v[1], togri=v[2],
            rang=v[3] if len(v) > 3 else '', rasm=rasmlar.get(i, ''),
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

    # Bo'limchalar har bo'lim ichida 1 dan boshlab raqamlanadi
    for bolim in Bolim.objects.all():
        for i, sub in enumerate(bolim.bolimchalar.order_by('order'), start=1):
            if sub.order != i:
                sub.order = i
                sub.save()

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
    Savol.objects.filter(bolimcha__bolim=Bolim.objects.get(order=2)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_savol_labirint'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
