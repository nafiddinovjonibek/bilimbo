"""5-bo'lim — "SAN'AT MARKAZI".

Manba: "Bilimbo platformasi uchun topshiriqlari.docx".

Hujjatdagi "musiqa tinglash" topshiriqlarida audio fayl yo'q, shuning uchun
musiqa kayfiyati matn bilan tasvirlangan (ovoz sintezi o'qib beradi) —
javob esa hujjatdagidek qolgan.
"""
from django.db import migrations

V = 'images/topshiriq/variantlar/'

# Bo'yash chizmalari. Har bir soha data-soha bilan belgilanadi; data-togri
# berilgan soha aynan shu rangga bo'yalishi kerak (namunaga qarab bo'yash),
# aks holda bola istagan rangni tanlaydi (erkin ijod).
KAPALAK = (
    '<svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg" role="img">'
    '<ellipse data-soha="qanot-yuqori-chap" cx="105" cy="80" rx="52" ry="42"'
    ' transform="rotate(-18 105 80)"/>'
    '<ellipse data-soha="qanot-yuqori-ong" cx="195" cy="80" rx="52" ry="42"'
    ' transform="rotate(18 195 80)"/>'
    '<ellipse data-soha="qanot-past-chap" cx="118" cy="152" rx="40" ry="34"'
    ' transform="rotate(14 118 152)"/>'
    '<ellipse data-soha="qanot-past-ong" cx="182" cy="152" rx="40" ry="34"'
    ' transform="rotate(-14 182 152)"/>'
    '<ellipse data-soha="tana" cx="150" cy="118" rx="13" ry="62"/>'
    '<path class="chizgi" d="M144 62 C136 40 122 32 112 28"/>'
    '<path class="chizgi" d="M156 62 C164 40 178 32 188 28"/>'
    '</svg>'
)

GUL_NAMUNA = (
    '<svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg" role="img">'
    '<rect data-soha="poya" data-togri="#4caf50" x="142" y="110" width="16"'
    ' height="88" rx="8"/>'
    '<ellipse data-soha="barg-chap" data-togri="#4caf50" cx="108" cy="150" rx="32"'
    ' ry="15" transform="rotate(-18 108 150)"/>'
    '<ellipse data-soha="barg-ong" data-togri="#4caf50" cx="192" cy="168" rx="32"'
    ' ry="15" transform="rotate(18 192 168)"/>'
    '<circle data-soha="gulbarg1" data-togri="#e94b4b" cx="150" cy="42" r="30"/>'
    '<circle data-soha="gulbarg2" data-togri="#e94b4b" cx="196" cy="76" r="30"/>'
    '<circle data-soha="gulbarg3" data-togri="#e94b4b" cx="178" cy="128" r="30"/>'
    '<circle data-soha="gulbarg4" data-togri="#e94b4b" cx="122" cy="128" r="30"/>'
    '<circle data-soha="gulbarg5" data-togri="#e94b4b" cx="104" cy="76" r="30"/>'
    '<circle data-soha="markaz" data-togri="#f2c230" cx="150" cy="90" r="24"/>'
    '</svg>'
)

MANZARA = (
    '<svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg" role="img">'
    '<rect data-soha="osmon" x="6" y="6" width="288" height="140" rx="12"/>'
    '<circle data-soha="quyosh" cx="246" cy="48" r="26"/>'
    '<rect data-soha="yer" x="6" y="146" width="288" height="68" rx="12"/>'
    '<rect data-soha="uy-devor" x="48" y="100" width="94" height="62" rx="6"/>'
    '<polygon data-soha="uy-tom" points="40,102 95,58 150,102"/>'
    '<rect data-soha="eshik" x="82" y="124" width="28" height="38" rx="4"/>'
    '<rect data-soha="daraxt-tana" x="214" y="118" width="18" height="46" rx="6"/>'
    '<circle data-soha="daraxt-barg" cx="223" cy="106" r="36"/>'
    '</svg>'
)

MAKTAB = (
    '<svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg" role="img">'
    '<rect data-soha="osmon" x="6" y="6" width="288" height="150" rx="12"/>'
    '<circle data-soha="quyosh" cx="250" cy="44" r="24"/>'
    '<rect data-soha="yer" x="6" y="156" width="288" height="58" rx="12"/>'
    '<rect data-soha="bino" x="64" y="86" width="170" height="76" rx="6"/>'
    '<polygon data-soha="tom" points="54,88 149,44 244,88"/>'
    '<rect data-soha="eshik" x="134" y="120" width="32" height="42" rx="4"/>'
    '<rect data-soha="deraza-chap" x="84" y="104" width="30" height="26" rx="4"/>'
    '<rect data-soha="deraza-ong" x="186" y="104" width="30" height="26" rx="4"/>'
    '<rect data-soha="bayroq" x="146" y="16" width="26" height="18" rx="3"/>'
    '<line class="chizgi" x1="145" y1="14" x2="145" y2="46"/>'
    '</svg>'
)

# Bo'yoq palitrasi — bo'yash topshiriqlarida variantlar shu ranglar bo'ladi
PALITRA = [
    ('', 'Qizil', False, '#e94b4b'), ('', "To'q sariq", False, '#ff9f43'),
    ('', 'Sariq', False, '#f2c230'), ('', 'Yashil', False, '#4caf50'),
    ("", "Ko'k", False, '#3d7be0'), ('', 'Binafsha', False, '#a06cf0'),
    ('', 'Jigarrang', False, '#92683e'),
]

OSON = [
    {
        'tur': 'tanlov',
        'sarlavha': 'Rangni tanla',
        'matn': "Olmani qanday rangga bo'yaysan?",
        'rasm': V + 'olma.png',
        'variantlar': [('', 'Qizil', True, '#e94b4b'), ("", "Ko'k", False, '#3d7be0'),
                       ('', 'Binafsha', False, '#a06cf0')],
    },
    {
        'tur': 'boyash',
        'sarlavha': 'Rang ber',
        'matn': "Kapalakni istagan ranglaringga bo'ya.",
        'boyash': KAPALAK,
        'variantlar': PALITRA,
    },
    {
        'tur': 'qurish',
        'sarlavha': 'Shakldan rasm yasash',
        'matn': 'Uchburchak, kvadrat va doiradan uycha yasa.',
        'rasm': V + 'namuna-uycha.png',
        'qurish': [
            ('Tom', V + 'bolak-uchburchak-qizil-52x28.png', '24,6,52,28', False),
            ('Devor', V + 'bolak-kvadrat-kok-40x32.png', '30,34,40,32', False),
            ('Deraza', V + 'bolak-doira-sariq-14x14.png', '43,44,14,14', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': "Cho'tkani tanla",
        'matn': 'Rasm chizish uchun qaysi buyum kerak?',
        'variantlar': [("", "Cho'tka", True), ('', 'Qoshiq', False),
                       ("", "To'p", False)],
        'v_rasm': {1: V + 'chotka.png', 2: V + 'qoshiq.png', 3: V + 'top.png'},
    },
    {
        'tur': 'moslash',
        'sarlavha': 'Ranglarni moslashtir',
        'matn': "Har bir narsani o'z rangi bilan bog'la.",
        'juftlar': [('', 'Quyosh', '', 'Sariq'), ('', 'Barg', '', 'Yashil'),
                    ('', 'Suv', '', "Ko'k")],
        'v_rasm': {1: V + 'quyoshli.png', 2: V + 'barg.png', 3: V + 'suv.png'},
        'j_rasm': {1: V + 'rang-sariq.png', 2: V + 'rang-yashil.png',
                   3: V + 'rang-kok.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Ortiqchasini top',
        'matn': 'Qaysi biri ortiqcha?',
        'variantlar': [('', 'Palitra', False), ("", "Cho'tka", False),
                       ('', 'Qalam', False), ('', 'Banan', True)],
        'v_rasm': {1: V + 'palitra.png', 2: V + 'chotka.png',
                   3: V + 'qalam-uzun.png', 4: V + 'banan.png'},
    },
    {
        'tur': 'qurish',
        'sarlavha': 'Rasmni yakunla',
        'matn': "Gulning yarmi chizilgan. Qolgan qismini o'z joyiga qo'yib tugat.",
        'rasm': V + 'namuna-gul-yarim.png',
        'qurish': [
            ('Markaz', V + 'bolak-doira-sariq-14x14.png', '44,30,14,14', True),
            ('Chap yuqori gulbarg', V + 'bolak-doira-qizil-16x16.png',
             '30,14,16,16', True),
            ('Chap past gulbarg', V + 'bolak-doira-qizil-16x16.png',
             '28,40,16,16', True),
            ("O'ng yuqori gulbarg", V + 'bolak-doira-qizil-16x16.png',
             '56,14,16,16', False),
            ("O'ng past gulbarg", V + 'bolak-doira-qizil-16x16.png',
             '58,40,16,16', False),
            ('Poya', V + 'bolak-tortburchak-yashil-8x12.png', '47,56,8,12', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Musiqaga mos rasm',
        'matn': "Quvnoq, tez musiqa yangramoqda.\nQaysi rasm shu musiqaga mos?",
        'variantlar': [('', 'Bayram', True), ('', 'Yomg\'ir', False),
                       ('', 'Tuman', False)],
        'v_rasm': {1: V + 'his-xursand.png', 2: V + 'yomgirli.png',
                   3: V + 'tuman.png'},
    },
    {
        'tur': 'moslash',
        'sarlavha': 'Soyani top',
        'matn': "Har bir buyumni o'z soyasi bilan bog'la.",
        'juftlar': [("", "Cho'tka", '', "Cho'tka soyasi"),
                    ('', 'Palitra', '', 'Palitra soyasi'),
                    ('', 'Qalam', '', 'Qalam soyasi')],
        'v_rasm': {1: V + 'chotka.png', 2: V + 'palitra.png', 3: V + 'qalam-uzun.png'},
        'j_rasm': {1: V + 'soya-chotka.png', 2: V + 'soya-palitra.png',
                   3: V + 'soya-qalam.png'},
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Qaysi rang yetishmayapti?',
        'matn': 'Kamalakda bitta rang yo\'q. Qaysi rang yetishmayapti?',
        'rasm': V + 'kamalak-yashilsiz.png',
        'variantlar': [('', 'Yashil', True, '#4caf50'), ('', 'Qizil', False, '#e94b4b'),
                       ('', 'Binafsha', False, '#a06cf0')],
    },
]

ORTA = [
    {
        'tur': 'boyash',
        'sarlavha': 'Namunaga qarab bo\'ya',
        'matn': "Namunadagi gulni ko'r va xuddi shunday ranglarda bo'ya.",
        'rasm': V + 'namuna-gul.png',
        'boyash': GUL_NAMUNA,
        'variantlar': PALITRA,
    },
    {
        'tur': 'qurish',
        'sarlavha': 'Kollaj yarat',
        'matn': "Daraxt, qush va quyosh rasmlarini sudrab tabiat manzarasini hosil qil.",
        'rasm': V + 'namuna-kollaj.png',
        'qurish': [
            ('Qush', V + 'qush.png', '10,8,20,28', False),
            ('Daraxt', V + 'daraxt.png', '54,26,30,43', False),
            ('Quyosh', V + 'quyoshli.png', '72,6,20,28', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Naqshni davom ettir',
        'matn': "Bo'sh joyga qaysi rang keladi?",
        'rasm': V + 'naqsh-qizil-yashil.png',
        'variantlar': [('', 'Qizil', True, '#e94b4b'), ('', 'Yashil', False, '#4caf50'),
                       ("", "Ko'k", False, '#3d7be0')],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Musiqani tingla',
        'matn': "Sekin, mayin musiqa yangramoqda.\nQaysi rasm shu musiqaga mos?",
        'variantlar': [('', 'Gullar', True), ("", "Yomg'ir", False),
                       ("", "Yong'in", False)],
        'v_rasm': {1: V + 'gul.png', 2: V + 'yomgirli.png',
                   3: V + 'yongin-mashinasi.png'},
    },
    {
        'tur': 'qurish',
        'sarlavha': "Simmetriyani to'ldir",
        'matn': "Kapalakning chap yarmi berilgan. O'ng yarmini xuddi shunday to'ldir.",
        'rasm': V + 'namuna-kapalak-yarim.png',
        'qurish': [
            ('Tana', V + 'bolak-tortburchak-jigar-8x40.png', '46,20,8,40', True),
            ('Chap yuqori qanot', V + 'bolak-doira-binafsha-22x22.png',
             '24,14,22,22', True),
            ('Chap past qanot', V + 'bolak-doira-tosariq-18x18.png',
             '26,40,18,18', True),
            ("O'ng yuqori qanot", V + 'bolak-doira-binafsha-22x22.png',
             '54,14,22,22', False),
            ("O'ng past qanot", V + 'bolak-doira-tosariq-18x18.png',
             '56,40,18,18', False),
        ],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Ranglarni aralashtir',
        'matn': 'Qizil + Sariq = ?',
        'ovoz_matn': 'Qizil va sariq rang aralashtirilsa qanday rang hosil bo\'ladi?',
        'variantlar': [("", "To'q sariq", True, '#ff9f43'),
                       ('', 'Yashil', False, '#4caf50'),
                       ("", "Ko'k", False, '#3d7be0')],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Rasmga nom ber',
        'matn': 'Rasmga mos sarlavhani tanla.',
        'rasm': V + 'namuna-kollaj.png',
        'variantlar': [('', 'Tabiat manzarasi', True), ('', 'Shahar ko\'chasi', False),
                       ('', 'Dengiz bo\'yi', False)],
    },
    {
        'tur': 'moslash',
        'sarlavha': "His-tuyg'uni rang bilan ifodala",
        'matn': "Har bir his-tuyg'uga mos rangni tanla.",
        'juftlar': [('', 'Xursand', '', 'Sariq'), ('', 'Xafa', '', "Ko'k"),
                    ('', 'Jahli chiqqan', '', 'Qizil')],
        'v_rasm': {1: V + 'his-xursand.png', 2: V + 'his-xafa.png',
                   3: V + 'his-jahli.png'},
        'j_rasm': {1: V + 'rang-sariq.png', 2: V + 'rang-kok.png',
                   3: V + 'rang-qizil.png'},
    },
    {
        'tur': 'qurish',
        'sarlavha': "Mozaika yig'",
        'matn': "Mayda geometrik shakllardan baliq rasmini yig'.",
        'rasm': V + 'namuna-mozaika-baliq.png',
        'qurish': [
            ('Bosh', V + 'bolak-doira-sariq-30x30.png', '28,22,30,30', False),
            ('Tana', V + 'bolak-tortburchak-tosariq-30x18.png', '44,28,30,18', False),
            ('Dum', V + 'bolak-uchburchak-qizil-22x26.png', '70,24,22,26', False),
            ("Ko'z", V + 'bolak-doira-kok-8x8.png', '34,30,8,8', False),
        ],
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Mikrofon orqali izoh ber',
        'matn': "Chizgan rasming haqida 3–4 ta gap ayt.",
        'izoh': 'Baholash mezoni:\n• 3–4 ta gap.\n• Ranglar haqida gapirish.\n'
                '• Fikrning tushunarliligi.',
    },
]

QIYIN = [
    {
        'tur': 'boyash',
        'sarlavha': 'Erkin ijod',
        'matn': '"Mening orzuimdagi maktab" — rasmni istagan ranglaringda bo\'ya.',
        'boyash': MAKTAB,
        'variantlar': PALITRA,
    },
    {
        'tur': 'qurish',
        'sarlavha': 'Berilgan shakllardan rasm yarat',
        'matn': "Faqat 3 ta doira, 2 ta kvadrat va 2 ta uchburchakdan rasm yarat.",
        'rasm': V + 'namuna-erkin-shakllar.png',
        'qurish': [
            ('Doira', V + 'bolak-doira-sariq-16x16.png', '42,4,16,16', False),
            ('Doira', V + 'bolak-doira-sariq-16x16.png', '22,26,16,16', False),
            ('Doira', V + 'bolak-doira-sariq-16x16.png', '62,26,16,16', False),
            ('Kvadrat', V + 'bolak-kvadrat-binafsha-18x20.png', '30,46,18,20', False),
            ('Kvadrat', V + 'bolak-kvadrat-binafsha-18x20.png', '52,46,18,20', False),
            ('Uchburchak', V + 'bolak-uchburchak-yashil-14x20.png', '14,46,14,20', False),
            ('Uchburchak', V + 'bolak-uchburchak-yashil-14x20.png', '72,46,14,20', False),
        ],
    },
    {
        'tur': 'koptanlov',
        'sarlavha': 'Xatoni top',
        'matn': "Ikki rasmni solishtir. Nimalar farq qiladi? Hammasini belgila.",
        'rasm': V + 'farq-namuna.png',
        'variantlar': [('', 'Quyoshning rangi', True), ('', 'Tomning rangi', True),
                       ('', 'Qushlar qo\'shilgan', True), ('', 'Uyning shakli', False),
                       ('', 'Derazalar soni', False)],
    },
    {
        'tur': 'boyash',
        'sarlavha': 'Musiqa va rasm',
        'matn': "Sekin, mayin musiqa yangramoqda.\n"
                "Manzarani shu musiqaga mos ranglar bilan bo'ya.",
        'boyash': MANZARA,
        'variantlar': PALITRA,
    },
    {
        'tur': 'tartib',
        'sarlavha': 'Ketma-ketlikni tikla',
        'matn': "Rasm chizish bosqichlarini to'g'ri tartibga joylashtir.",
        'tartib': [("", "G'oyani tanlash"), ('', 'Chizish'),
                   ('', 'Rang berish'), ('', 'Yakunlash')],
    },
    {
        'tur': 'tanlov',
        'sarlavha': 'Rang uyg\'unligini tanla',
        'matn': "Qaysi ranglar bir-biriga mos keladi?",
        'variantlar': [("", "Bir-biriga yaqin ranglar", True),
                       ('', 'Keskin farqli ranglar', False),
                       ('', 'Xira ranglar', False)],
        'v_rasm': {1: V + 'uygunlik-1.png', 2: V + 'uygunlik-2.png',
                   3: V + 'uygunlik-3.png'},
    },
    {
        'tur': 'mikrofon',
        'sarlavha': "Virtual ko'rgazma",
        'matn': "Ko'rgazmadagi rasmlardan eng yoqqanini tanla va nima uchun "
                "yoqqanini ayt.",
        'rasm': V + 'namuna-kollaj.png',
        'izoh': 'Baholash mezoni:\n• Tanlovni asoslash.\n• Ranglar va shakllar '
                'haqida fikr.',
    },
    {
        'tur': 'mikrofon',
        'sarlavha': 'Rasm asosida hikoya',
        'matn': "Rasmga qarab 5–6 ta gapdan iborat hikoya tuz.",
        'rasm': 'images/topshiriq/bolalar-bogda.png',
        'izoh': 'Baholash mezoni:\n• 5–6 ta gap.\n• Voqealar ketma-ketligi.\n'
                '• Rasmga mos mazmun.',
    },
    {
        'tur': 'koptanlov',
        'sarlavha': 'Ijodiy muammo',
        'matn': "Kuz manzarasi uchun faqat kuz ranglarini tanla.",
        'variantlar': [('', 'Sariq', True, '#f2c230'),
                       ("", "To'q sariq", True, '#ff9f43'),
                       ('', 'Jigarrang', True, '#92683e'),
                       ("", "Ko'k", False, '#3d7be0'),
                       ('', 'Binafsha', False, '#a06cf0')],
    },
    {
        'tur': 'kvest',
        'sarlavha': 'Yosh Rassom',
        'matn': 'Yakuniy sarguzasht! Ketma-ket 5 ta vazifani bajarasan.',
        'bosqichlar': [
            {
                'tur': 'boyash',
                'sarlavha': '🎨 Rasmni bo\'ya',
                'matn': "Kapalakni istagan ranglaringga bo'ya.",
                'boyash': KAPALAK,
                'variantlar': PALITRA,
            },
            {
                'tur': 'qurish',
                'sarlavha': "🧩 Mozaika yig'",
                'matn': "Shakllardan baliq rasmini yig'.",
                'rasm': V + 'namuna-mozaika-baliq.png',
                'qurish': [
                    ('Bosh', V + 'bolak-doira-sariq-30x30.png', '28,22,30,30', False),
                    ('Tana', V + 'bolak-tortburchak-tosariq-30x18.png',
                     '44,28,30,18', False),
                    ('Dum', V + 'bolak-uchburchak-qizil-22x26.png', '70,24,22,26', False),
                    ("Ko'z", V + 'bolak-doira-kok-8x8.png', '34,30,8,8', False),
                ],
            },
            {
                'tur': 'tanlov',
                'sarlavha': '🌈 Ranglarni aralashtir',
                'matn': "Ko'k + Sariq = ?",
                'ovoz_matn': "Ko'k va sariq rang aralashtirilsa qanday rang "
                             "hosil bo'ladi?",
                'variantlar': [('', 'Yashil', True, '#4caf50'),
                               ('', 'Qizil', False, '#e94b4b'),
                               ('', 'Jigarrang', False, '#92683e')],
            },
            {
                'tur': 'boyash',
                'sarlavha': '🖼️ Erkin rasm yarat',
                'matn': "Manzarani istagan ranglaringda bo'ya.",
                'boyash': MANZARA,
                'variantlar': PALITRA,
            },
            {
                'tur': 'mikrofon',
                'sarlavha': "🎤 O'z ijodingni tushuntir",
                'matn': "Chizgan rasming haqida 3–4 ta gap ayt.",
                'izoh': 'Bola ovoz yozadi, tarbiyachi baholaydi.',
            },
        ],
    },
]

BOLIM = {'order': 5, 'name': "San'at", 'emoji': '🎨'}
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
        boyash=t.get('boyash', ''),
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
    Savol.objects.filter(bolimcha__bolim=Bolim.objects.get(order=5)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_savol_boyash'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
