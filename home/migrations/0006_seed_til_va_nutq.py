from django.db import migrations

# "Bilimbo platformasi uchun topshiriqlari.docx" hujjatidagi
# 1-bo'lim — "TIL VA NUTQ" yo'nalishi topshiriqlari.
#
# Hujjatda har daraja uchun 10 tadan topshiriq bor. Platformada bitta savol
# 3 ta variantdan iborat bo'lgani uchun 4 variantli savollar 3 taga qisqartirildi,
# drag & drop / mikrofon topshiriqlari esa shu mazmunni saqlagan holda
# tanlovli ko'rinishga moslashtirildi.

BOLIM = {
    'order': 1,
    'name': 'Til va nutq',
    'emoji': '🗣️',
}

# (bolimcha order, nomi, emoji, daraja, savollar)
# savol: (matn, variant_a, variant_b, variant_c, to'g'ri javob)
BOLIMCHALAR = [
    (1, '1-daraja — Oson', '🟢', 'oson', [
        (
            'Olmani top.',
            '🍎 Olma', '🍌 Banan', '🚗 Mashina', 'a',
        ),
        (
            '🔊 "Mushuk miyovladi." Bu qaysi hayvonning ovozi?',
            '🐄 Sigir', '🐱 Mushuk', '🐔 Tovuq', 'b',
        ),
        (
            'Qaysi harf "A"?',
            'B', 'T', 'A', 'c',
        ),
        (
            'Qizil rangni tanla.',
            '🟦 Ko\'k', '🟥 Qizil', '🟩 Yashil', 'b',
        ),
        (
            'Qaysi biri ortiqcha? 🍎 🍐 🍌 🚲',
            '🍐 Nok', '🚲 Velosiped', '🍌 Banan', 'b',
        ),
        (
            'So\'zni tugat: OL _ A',
            'M', 'B', 'S', 'a',
        ),
        (
            'Nechta yulduz bor? ⭐️⭐️⭐️⭐️⭐️',
            '3 ta', '4 ta', '5 ta', 'c',
        ),
        (
            '🐶 It nima qiladi?',
            'Suzadi', 'Uchadi', 'Huradi', 'c',
        ),
        (
            '"Anor" so\'zi qaysi tovush bilan boshlanadi?',
            'A', 'O', 'N', 'a',
        ),
        (
            '🖼 Rasmda bola kitob o\'qiyapti. Qaysi gap rasmga mos?',
            'Bola uxlayapti.', 'Bola kitob o\'qiyapti.', 'Bola yuguryapti.', 'b',
        ),
    ]),
    (2, '2-daraja — O\'rta', '🟡', 'orta', [
        (
            'Voqea ketma-ketligi: 🌱 Urug\' → ❓ → 🌼 Gul → 🌳 Daraxt. '
            'Bo\'sh joyga nima to\'g\'ri keladi?',
            '🌿 Nihol', '🍎 Olma', '🪨 Tosh', 'a',
        ),
        (
            '"Olma" so\'zi nechta bo\'g\'indan iborat?',
            '1 ta', '2 ta', '3 ta', 'b',
        ),
        (
            '🐟 Baliq qayerda yashaydi?',
            '🌳 Daraxtda', '🏜 Cho\'lda', '🌊 Suvda', 'c',
        ),
        (
            '🔊 "Bugun havo quyoshli." Bugun ob-havo qanday?',
            '🌧 Yomg\'irli', '☀️ Quyoshli', '❄️ Qorli', 'b',
        ),
        (
            'Yetishmayotgan harfni top: B _ L I Q',
            'A', 'O', 'E', 'a',
        ),
        (
            'Qaysi so\'z "S" harfi bilan boshlanadi?',
            '🍎 Olma', '🦁 Sher', '🚗 Mashina', 'b',
        ),
        (
            '🖼 Rasmda qiz gul sug\'ormoqda. Qaysi gap to\'g\'ri?',
            'Qiz futbol o\'ynayapti.', 'Qiz uxlayapti.', 'Qiz gul sug\'ormoqda.', 'c',
        ),
        (
            '🎤 Yoqtirgan mevang haqida gapirmoqchisan. Qaysi gap to\'g\'ri tuzilgan?',
            'Men olmani yaxshi ko\'raman.', 'Men olma ko\'raman yaxshi.',
            'Olma men yaxshi ko\'raman.', 'a',
        ),
        (
            'Xatoni top: "Baliq daraxtda yashaydi."',
            'To\'g\'ri', 'Noto\'g\'ri', 'Ba\'zan to\'g\'ri', 'b',
        ),
        (
            'Hikoyani yakunla: "Quyon o\'rmonda sayr qilayotgan edi. Birdan..."',
            'Samolyot uchirdi.', 'Mashina haydadi.', 'Do\'stini uchratdi.', 'c',
        ),
    ]),
    (3, '3-daraja — Qiyin', '🔴', 'qiyin', [
        (
            '🐰 Quyon savatni oldi va o\'rmonga bordi. Keyin nima qildi?',
            '🥕 Sabzi yig\'di.', '😴 Uxlab qoldi.', '🏫 Maktabga bordi.', 'a',
        ),
        (
            'Ortiqcha gapni top.',
            'Mushuk sut ichadi.', 'Mushuk daraxt ekadi.', 'Mushuk miyovlaydi.', 'b',
        ),
        (
            'So\'zlardan gap tuz: "kitob", "o\'qiyapti", "bola".',
            'Kitob bola o\'qiyapti.', 'O\'qiyapti bola kitob.', 'Bola kitob o\'qiyapti.', 'c',
        ),
        (
            '🖼 Rasmda bolalar daraxt ekmoqda. Rasmga mos sarlavhani tanla.',
            '"Tabiatni asraymiz."', '"Qishda qor yog\'di."', '"Bozorda sayr."', 'a',
        ),
        (
            '🎤 Rasm asosida hikoya tuzyapsan. Qaysi gap hikoyani boshlash uchun mos?',
            'Keyin ular uyga qaytishdi.', 'Bir kuni bolalar bog\'ga chiqishdi.',
            'Shunday qilib kun tugadi.', 'b',
        ),
        (
            '"Chiroyli" so\'ziga yaqin ma\'noli so\'zni tanla.',
            'Sovuq', 'Katta', 'Go\'zal', 'c',
        ),
        (
            '"Baland" so\'zining qarama-qarshi ma\'nosi qaysi?',
            'Past', 'Tez', 'Keng', 'a',
        ),
        (
            'Topishmoqni yech: "O\'zi kichkina, dumi uzun, pishloqni yaxshi ko\'radi."',
            '🐭 Sichqon', '🐱 Mushuk', '🐰 Quyon', 'a',
        ),
        (
            'Qushlar nima uchun uya quradi?',
            'Dam olish uchun.', 'Bolalarini parvarish qilish uchun.',
            'Baliq tutish uchun.', 'b',
        ),
        (
            '🏆 "Til sarguzashti"ning oxirgi vazifasi — topishmoq: '
            '"Yozda ko\'m-ko\'k kiyinadi, qishda yalang\'och qoladi."',
            '🪨 Tosh', '📚 Kitob', '🌳 Daraxt', 'c',
        ),
    ]),
]


def seed(apps, schema_editor):
    Bolim = apps.get_model('home', 'Bolim')
    Bolimcha = apps.get_model('home', 'Bolimcha')
    Savol = apps.get_model('home', 'Savol')

    bolim = Bolim.objects.get(order=BOLIM['order'])
    bolim.name = BOLIM['name']
    bolim.emoji = BOLIM['emoji']
    bolim.save()

    for sub_order, sub_name, sub_emoji, daraja, savollar in BOLIMCHALAR:
        sub = Bolimcha.objects.get(bolim=bolim, order=sub_order)
        sub.name = sub_name
        sub.emoji = sub_emoji
        sub.save()

        for order, (matn, a, b, c, togri) in enumerate(savollar, start=1):
            Savol.objects.update_or_create(
                bolimcha=sub,
                order=order,
                defaults={
                    'daraja': daraja,
                    'matn': matn,
                    'variant_a': a,
                    'variant_b': b,
                    'variant_c': c,
                    'togri_javob': togri,
                },
            )


def unseed(apps, schema_editor):
    """0005 dagi namunaviy holatga qaytaradi."""
    Bolim = apps.get_model('home', 'Bolim')
    Bolimcha = apps.get_model('home', 'Bolimcha')
    Savol = apps.get_model('home', 'Savol')

    def daraja_by_order(order):
        if order <= 3:
            return 'oson'
        if order <= 6:
            return 'orta'
        if order <= 9:
            return 'qiyin'
        return 'tanqidiy'

    bolim = Bolim.objects.get(order=BOLIM['order'])
    bolim.name = f"Bo'lim {bolim.order}"
    bolim.emoji = '🚀'
    bolim.save()

    for sub in Bolimcha.objects.filter(bolim=bolim):
        sub.name = f"Bo'limcha {sub.order}"
        sub.emoji = ['🎯', '🎲', '🃏'][sub.order - 1]
        sub.save()

        for order in range(1, 11):
            Savol.objects.filter(bolimcha=sub, order=order).update(
                daraja=daraja_by_order(order),
                matn=f'{sub.name}: {order}-savol matni shu yerda bo\'ladi. '
                     f'To\'g\'ri javobni tanlang!',
                variant_a='Birinchi javob',
                variant_b='Ikkinchi javob',
                variant_c='Uchinchi javob',
                togri_javob='abc'[order % 3],
            )


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_seed_savollar'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
