"""3-bo'lim — "SYUJETLI-ROLLI O'YINLAR MARKAZI".

Manba: "Bilimbo platformasi uchun topshiriqlari.docx".
Hujjatdagi 3 daraja x 10 topshiriq.
"""
from django.db import migrations

V = 'images/topshiriq/variantlar/'

# tur: tanlov | koptanlov | xarid | tartib | moslash | mikrofon | kvest
#   variantlar : (emoji, matn, to'g'rimi)   + v_rasm {tartib: rasm}
#   xarid/koptanlov: variantlar + narxlar {tartib: narx}, byudjet

OSON = [
    {
        'tur': 'tanlov',
        'sarlavha': 'Kasbni tanla',
        'matn': 'Bemorni kim davolaydi?',
        'variantlar': [('', 'Shifokor', True), ('', 'Oshpaz', False),
                       ("", "Yo'l patruli", False), ('', 'Dehqon', False)],
        'v_rasm': {1: V + 'shifokor.png', 2: V + 'oshpaz.png',
                   3: V + 'politsiyachi.png', 4: V + 'dehqon.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kerakli buyumni tanla',
        'matn': 'Shifokorga kerakli buyumni tanla.',
        'variantlar': [('', 'Shprits', False), ('', 'Stetoskop', True),
                       ('', 'Kitob', False), ("", "To'p", False)],
        'v_rasm': {1: V + 'shprits.png', 2: V + 'stetoskop.png',
                   3: V + 'kitob.png', 4: V + 'top.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kim nima qiladi?',
        'matn': 'Oshpaz nima qiladi?',
        'variantlar': [('', 'Ovqat pishiradi.', True),
                       ('', 'Mashina boshqaradi.', False),
                       ('', 'Uy quradi.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Dialogni tugat',
        'matn': '— Assalomu alaykum.\nSen nima deysan?',
        'variantlar': [('', 'Vaalaykum assalom.', True), ('', 'Xayr.', False),
                       ('', 'Rahmat.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': "To'g'ri muomala",
        'matn': "Do'konda nima deysan?",
        'variantlar': [('', 'Iltimos.', True), ('', 'Baqiraman.', False),
                       ('', 'Yuguraman.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kasbni top',
        'matn': 'Bu mashinada kim ishlaydi?',
        'rasm': V + 'yongin-mashinasi.png',
        'variantlar': [("", "O't o'chiruvchi", True), ('', 'Haydovchi', False),
                       ('', 'Tikuvchi', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kimga yordam berasan?',
        'matn': 'Bola yiqilib tushdi. Sen nima qilasan?',
        'rasm': V + 'yiqilgan-bola.png',
        'variantlar': [('', 'Yordam beraman.', True), ('', 'Kulaman.', False),
                       ('', 'Ketaman.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Telefon suhbati',
        'matn': '"Salom!" deganidan keyin nima deysan?',
        'rasm': V + 'telefon.png',
        'variantlar': [('', 'Salom.', True), ('', 'Xayr.', False),
                       ('', 'Jim turaman.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Navbat',
        'matn': "Do'konda navbat bor. Nima qilasan?",
        'variantlar': [('', 'Navbat kutaman.', True),
                       ('', 'Oldinga yuguraman.', False),
                       ('', 'Itaraman.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': "His-tuyg'uni top",
        'matn': 'Xursand bolani tanla.',
        'variantlar': [('', 'Xursand', True), ('', 'Xafa', False),
                       ('', 'Jahli chiqqan', False), ('', 'Hayron', False)],
        'v_rasm': {1: V + 'his-xursand.png', 2: V + 'his-xafa.png',
                   3: V + 'his-jahli.png', 4: V + 'his-hayron.png'},
    },
]

ORTA = [
    {
        'tur': 'moslash',
        'sarlavha': 'Rollarni moslashtir',
        'matn': "Kasbni ish joyi bilan bog'la.",
        'juftlar': [('', 'Shifokor', '', 'Kasalxona'),
                    ("", "O'qituvchi", '', 'Maktab'),
                    ("", "Yo'l patruli", '', "Ko'cha")],
        'v_rasm': {1: V + 'shifokor.png', 2: V + 'oqituvchi.png',
                   3: V + 'politsiyachi.png'},
        'j_rasm': {1: V + 'kasalxona.png', 2: V + 'maktab.png', 3: V + 'kocha.png'},
    },
    {
        'tur': 'tartib',
        'sarlavha': 'Dialogni tartibla',
        'matn': "Gaplarni to'g'ri ketma-ketlikda joylashtir.",
        'tartib': [('', 'Assalomu alaykum.'), ('', 'Marhamat.'),
                   ('', 'Rahmat.'), ('', 'Xayr.')],
    },
    {
        'tur': 'xarid',
        'sarlavha': 'Xarid qil',
        'matn': 'Senda 10 tanga bor. Aynan 10 tangalik xarid qil.',
        'byudjet': 10,
        # 4 + 3 + 3 = 10. Kitob qo'shilsa yoki biror mahsulot tushib qolsa,
        # summa 10 dan chiqib ketadi — javob yagona.
        'variantlar': [('', 'Olma', True), ('', 'Sut', True),
                       ('', 'Non', True), ('', 'Kitob', False)],
        'v_rasm': {1: V + 'olma.png', 2: V + 'sut.png',
                   3: V + 'non.png', 4: V + 'kitob.png'},
        'narxlar': {1: 4, 2: 3, 3: 3, 4: 5},
    },
    {
        'tur': 'koptanlov',
        'sarlavha': 'Kerakli buyumni tanla',
        'matn': 'Sayohatga ketayotgan bola uchun kerakli buyumlarni tanla.',
        'variantlar': [('', 'Ryukzak', True), ('', 'Kiyim', True),
                       ('', 'Suv', True), ('', 'Televizor', False)],
        'v_rasm': {1: V + 'ryukzak.png', 2: V + 'kiyim.png',
                   3: V + 'suv-shisha.png', 4: V + 'televizor.png'},
    },
    {
        'tur': 'mikrofon',
        'sarlavha': "Mikrofon orqali xaridor bo'l",
        'matn': "Do'kondan non sotib ol. Sotuvchi bilan qisqa suhbat qur.",
        'izoh': 'Bola ovoz yozadi, tarbiyachi baholaydi.',
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Xatoni top',
        'matn': "Oshpaz bemorni operatsiya qilyapti.\nBu to'g'rimi?",
        'variantlar': [("", "To'g'ri", False), ("", "Noto'g'ri", True)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Muammoni hal qil',
        'matn': "Do'sting o'yinchog'ini tushirib yubordi. Nima qilasan?",
        'variantlar': [('', 'Yordam beraman.', True), ('', 'Ketaman.', False),
                       ('', 'Urishaman.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Rasmga mos kasbni tanla',
        'matn': 'Bu yerda kim ishlaydi?',
        'rasm': V + 'qurilish.png',
        'variantlar': [('', 'Quruvchi', True), ('', 'Shifokor', False),
                       ('', 'Sotuvchi', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Mehmon kutish',
        'matn': 'Mehmon kelganda birinchi nima qilasan?',
        'variantlar': [('', 'Salomlashaman.', True),
                       ('', 'Yugurib ketaman.', False),
                       ('', 'Jim turaman.', False)],
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Kasb haqida gapir',
        'matn': '"Men shifokorman..." deb 3–4 ta gap ayt.',
        'rasm': V + 'shifokor.png',
        'izoh': 'Baholash mezoni:\n• Gaplar mantiqiyligi.\n• Kasb haqida aniq ma\'lumot.\n'
                '• To\'liq gaplardan foydalanish.',
    },
]

QIYIN = [
    {
        'tur': 'kvest',
        'sarlavha': "Virtual do'kon",
        'matn': "Sen xaridorsan. Mahsulot tanla, narxini hisobla, "
                "to'lov qil va qaytimni tekshir.",
        'bosqichlar': [
            {
                'tur': 'xarid',
                'sarlavha': '🛒 Mahsulot tanla',
                'matn': 'Senda 12 tanga bor. Aynan 12 tangalik xarid qil.',
                'byudjet': 12,
                # 5 + 4 + 3 = 12; boshqa hech qanday to'plam 12 ni bermaydi
                'variantlar': [('', 'Kitob', True), ('', 'Olma', True),
                               ('', 'Sut', True), ('', 'Televizor', False)],
                'v_rasm': {1: V + 'kitob.png', 2: V + 'olma.png',
                           3: V + 'sut.png', 4: V + 'televizor.png'},
                'narxlar': {1: 5, 2: 4, 3: 3, 4: 6},
            },
            {
                'tur': 'tanlov',
                'sarlavha': '🔢 Narxini hisobla',
                'matn': 'Kitob 5, olma 4, sut 3 tanga.\nJami qancha bo'
                        "'ldi?",
                'ovoz_matn': "Kitob besh, olma to'rt, sut uch tanga. Jami qancha bo'ldi?",
                'variantlar': [('', '10', False), ('', '12', True), ('', '14', False)],
            },
            {
                'tur': 'tanlov',
                'sarlavha': "💵 To'lov qil",
                'matn': "Xarid 12 tanga bo'ldi. Sotuvchiga qaysi pulni berasan?",
                'variantlar': [('', '5 tanga', False), ('', '10 tanga', False),
                               ('', '15 tanga', True)],
            },
            {
                'tur': 'tanlov',
                'sarlavha': '💰 Qaytimni tekshir',
                'matn': "15 tanga berding, xarid 12 tanga edi.\nQancha qaytim olasan?",
                'ovoz_matn': "O'n besh tanga berding, xarid o'n ikki tanga edi. "
                             "Qancha qaytim olasan?",
                'variantlar': [('', '2 tanga', False), ('', '3 tanga', True),
                               ('', '5 tanga', False)],
            },
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Kasalxonada',
        'matn': "Bemorning isitmasi bor. To'g'ri yordamni tanla.",
        'rasm': V + 'bemor.png',
        'variantlar': [('', 'Shifokorga olib borish.', True),
                       ('', 'Muzqaymoq berish.', False),
                       ('', 'Yugurtirish.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Maktabdagi vaziyat',
        'matn': "O'qituvchi savol berdi. Qanday javob berasan?",
        'rasm': V + 'oqituvchi.png',
        'variantlar': [("", "Qo'l ko'tarib javob beraman.", True),
                       ('', 'Baqirib javob beraman.', False),
                       ('', 'Javob bermayman.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Mojaroni hal qil',
        'matn': "Ikki bola bitta o'yinchoqni talashmoqda.\nEng to'g'ri yechim qaysi?",
        'variantlar': [("", "Navbat bilan o'ynashni taklif qilaman.", True),
                       ("", "O'yinchoqni o'zim olaman.", False),
                       ('', 'Yig\'layman.', False)],
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Mikrofon orqali dialog',
        'matn': '"Sotuvchi va xaridor" rolini ijro et. Kamida 6 ta gap ishlat.',
        'izoh': 'Baholash mezoni:\n• Kamida 6 ta gap.\n• Salomlashish va xayrlashish.\n'
                '• Muomala odobi.',
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Hikoyani davom ettir',
        'matn': '"Maktabga birinchi kunim..." — 3–5 ta gap bilan davom ettir.',
        'rasm': V + 'maktab.png',
        'izoh': 'Baholash mezoni:\n• 3–5 ta gap.\n• Voqealar ketma-ketligi.',
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Kasbni tavsifla',
        'matn': "Bir kasbni nomini aytmasdan tarifla.\n"
                'Masalan: "Men odamlarni davolayman..."',
        'izoh': 'Platforma yoki tarbiyachi javobni baholaydi.',
    },
    {
        'tur': 'tanlov',
        'sarlavha': "His-tuyg'uni aniqla",
        'matn': "Bola yig'layapti. Nima uchun yig'layotgan bo'lishi mumkin?",
        'rasm': V + 'yiglayotgan-bola.png',
        'variantlar': [("", "O'yinchog'i sinib qoldi.", True),
                       ('', 'Muzqaymoq yedi.', False),
                       ('', 'Uxlab qoldi.', False)],
    },
    {
        'tur': 'tanlov',
        'sarlavha': "To'g'ri qaror qabul qil",
        'matn': "Ko'chada svetofor qizil. Nima qilasan?",
        'rasm': V + 'svetofor-qizil.png',
        'variantlar': [('', 'Kutaman.', True), ("", "Yugurib o'taman.", False),
                       ('', 'Velosiped haydayman.', False)],
    },
    {
        'tur': 'kvest',
        'sarlavha': 'Hayot maktabi',
        'matn': 'Yakuniy sarguzasht! Ketma-ket 5 ta rolni bajarasan.',
        'bosqichlar': [
            {
                'tur': 'tanlov',
                'sarlavha': '👨‍⚕️ Shifokor',
                'matn': "Bemorning isitmasi bor. Shifokor nima qiladi?",
                'rasm': V + 'bemor.png',
                'variantlar': [("", "Ko'rikdan o'tkazib, dori beradi.", True),
                               ('', 'Muzqaymoq beradi.', False),
                               ('', 'Yugurtiradi.', False)],
            },
            {
                'tur': 'xarid',
                'sarlavha': '🛒 Xaridor',
                'matn': 'Senda 6 tanga bor. Aynan 6 tangalik xarid qil.',
                'byudjet': 6,
                # 2 + 4 = 6; kitob (5) bilan hech qanday juftlik 6 ni bermaydi
                'variantlar': [('', 'Non', True), ('', 'Sut', True),
                               ('', 'Kitob', False)],
                'v_rasm': {1: V + 'non.png', 2: V + 'sut.png', 3: V + 'kitob.png'},
                'narxlar': {1: 2, 2: 4, 3: 5},
            },
            {
                'tur': 'tanlov',
                'sarlavha': "👨‍🏫 O'quvchi",
                'matn': "Darsda javob bermoqchisan. Nima qilasan?",
                'rasm': V + 'maktab.png',
                'variantlar': [("", "Qo'l ko'taraman.", True),
                               ('', 'Joyimdan baqiraman.', False),
                               ('', 'Sinfdan chiqib ketaman.', False)],
            },
            {
                'tur': 'tanlov',
                'sarlavha': '🚒 Qutqaruvchi',
                'matn': "Yong'in chiqdi. Birinchi nima qilasan?",
                'rasm': V + 'yongin-mashinasi.png',
                'variantlar': [('', 'Kattalarni chaqiraman.', True),
                               ("", "O'zim o'chirishga urinaman.", False),
                               ('', 'Yashirinaman.', False)],
            },
            {
                'tur': 'tanlov',
                'sarlavha': "👮 Yo'l harakati ishtirokchisi",
                'matn': "Yo'lni qayerdan kesib o'tasan?",
                'rasm': V + 'kocha.png',
                'variantlar': [("", "Piyodalar yo'lagidan.", True),
                               ('', 'Istagan joyimdan.', False),
                               ('', 'Mashinalar orasidan.', False)],
            },
        ],
    },
]

BOLIM = {'order': 3, 'name': "Syujetli-rolli o'yinlar", 'emoji': '🎭'}
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
        byudjet=t.get('byudjet'),
    )

    rasmlar = t.get('v_rasm', {})
    narxlar = t.get('narxlar', {})
    for i, v in enumerate(t.get('variantlar', []), start=1):
        Variant.objects.create(
            savol=savol, order=i, emoji=v[0], matn=v[1], togri=v[2],
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
    Savol.objects.filter(bolimcha__bolim=Bolim.objects.get(order=3)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_koptanlov_xarid'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
