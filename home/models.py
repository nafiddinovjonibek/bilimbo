import json
import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .storage import private_voice_storage


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Superadmin'
        TARBIYACHI = 'tarbiyachi', 'Tarbiyachi'
        OQUVCHI = 'oquvchi', "O'quvchi"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OQUVCHI,
        verbose_name='Rol',
    )
    teacher_approved = models.BooleanField(default=False, verbose_name='Tarbiyachi tasdiqlangan')
    guruh = models.ForeignKey(
        'Guruh', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='oquvchilar', verbose_name='Guruhi',
    )

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(guruh__isnull=True) | models.Q(role='oquvchi', is_superuser=False),
                name='only_students_have_group',
            ),
        ]

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_superadmin(self):
        return self.is_superuser or self.role == self.Role.SUPERADMIN

    @property
    def is_tarbiyachi(self):
        return not self.is_superadmin and self.role == self.Role.TARBIYACHI

    @property
    def is_oquvchi(self):
        return not self.is_superadmin and self.role == self.Role.OQUVCHI

    @property
    def is_approved_teacher(self):
        return self.is_tarbiyachi and self.teacher_approved and self.is_active

    def clean(self):
        super().clean()
        if self.guruh_id and not self.is_oquvchi:
            raise ValidationError({'guruh': 'Guruhga faqat o‘quvchi biriktiriladi.'})
        if self.pk and not self.is_tarbiyachi and self.guruhlar.exists():
            raise ValidationError({'role': 'Avval bu tarbiyachining guruhlarini boshqa tarbiyachiga o‘tkazing.'})


class Guruh(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Guruh nomi')
    tarbiyachi = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='guruhlar', verbose_name='Tarbiyachi',
        limit_choices_to={'role': User.Role.TARBIYACHI, 'teacher_approved': True, 'is_active': True},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom', 'pk']
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'

    def __str__(self):
        return self.nom

    def clean(self):
        super().clean()
        if self.tarbiyachi_id and not self.tarbiyachi.is_approved_teacher:
            raise ValidationError({'tarbiyachi': 'Faol va administrator tasdiqlagan tarbiyachini tanlang.'})


class Kitob(models.Model):
    manba = models.CharField(max_length=100, unique=True, verbose_name='Manba papkasi')
    nom = models.CharField(max_length=255, verbose_name='Nomi')
    mualliflar = models.TextField(blank=True, verbose_name='Mualliflar')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib raqami')
    sahifalar = models.PositiveIntegerField(verbose_name='Sahifalar (muqova bilan)')
    faol = models.BooleanField(default=True, verbose_name='Faol')
    fayl = models.CharField(max_length=255, editable=False)
    muqova = models.CharField(max_length=255, editable=False)
    fingerprint = models.CharField(max_length=64, editable=False)

    class Meta:
        ordering = ['order', 'pk']
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'

    def __str__(self):
        return self.nom


class Bolim(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nomi')
    order = models.PositiveIntegerField(unique=True, verbose_name='Tartib raqami')
    emoji = models.CharField(max_length=10, default='🎮', verbose_name='Emoji')

    class Meta:
        ordering = ['order']
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return self.name


class Bolimcha(models.Model):
    bolim = models.ForeignKey(
        Bolim,
        on_delete=models.CASCADE,
        related_name='bolimchalar',
        verbose_name="Bo'lim",
    )
    name = models.CharField(max_length=100, verbose_name='Nomi')
    order = models.PositiveIntegerField(verbose_name='Tartib raqami')
    emoji = models.CharField(max_length=10, default='⭐', verbose_name='Emoji')

    class Meta:
        ordering = ['order']
        verbose_name = "Bo'limcha"
        verbose_name_plural = "Bo'limchalar"

    def __str__(self):
        return f'{self.bolim.name} — {self.name}'


class Savol(models.Model):
    """Bitta topshiriq. `tur` maydoni uni qanday o'ynash kerakligini belgilaydi."""

    class Daraja(models.TextChoices):
        OSON = 'oson', 'Oson'
        ORTA = 'orta', "O'rta"
        QIYIN = 'qiyin', 'Qiyin'
        TANQIDIY = 'tanqidiy', 'Tanqidiy'

    class Tur(models.TextChoices):
        TANLOV = 'tanlov', 'Variantdan tanlash'
        KOPTANLOV = 'koptanlov', 'Bir nechta variantni tanlash'
        XARID = 'xarid', 'Byudjetga qarab xarid qilish'
        TARTIB = 'tartib', 'Ketma-ketlikka joylash'
        MOSLASH = 'moslash', 'Juftlarni moslashtirish'
        GURUH = 'guruh', 'Savatlarga ajratish'
        QURISH = 'qurish', 'Namunaga qarab yig\'ish'
        LABIRINT = 'labirint', 'Labirintdan olib o\'tish'
        BOYASH = 'boyash', 'Rasmni bo\'yash'
        MIKROFON = 'mikrofon', 'Mikrofon orqali javob'
        KVEST = 'kvest', 'Ko\'p bosqichli sarguzasht'

    bolimcha = models.ForeignKey(
        Bolimcha,
        on_delete=models.CASCADE,
        related_name='savollar',
        verbose_name="Bo'limcha",
    )
    # Kvest bosqichlari — o'zi savollar ro'yxatida ko'rinmaydigan bolalar
    kvest = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='bosqichlar',
        null=True,
        blank=True,
        verbose_name='Qaysi kvestga tegishli',
    )
    order = models.PositiveIntegerField(verbose_name='Tartib raqami')
    daraja = models.CharField(max_length=10, choices=Daraja.choices, verbose_name='Daraja')
    tur = models.CharField(
        max_length=10,
        choices=Tur.choices,
        default=Tur.TANLOV,
        verbose_name='Topshiriq turi',
    )
    sarlavha = models.CharField(max_length=120, blank=True, verbose_name='Topshiriq nomi')
    matn = models.TextField(verbose_name='Savol matni')
    # "Har bir topshiriq ovozli" — shu matndan o'zbekcha MP3 tayyorlanadi
    ovoz_matn = models.TextField(
        blank=True,
        verbose_name='Ovozlashtiriladigan matn',
        help_text="Bo'sh bo'lsa savol matni o'qiladi.",
    )
    # "Audioni tingla" turidagi topshiriqlar. Agar audio_fayl berilsa — o'sha
    # fayl ijro etiladi; aks holda audio_matn ovoz sinteziga o'qitiladi.
    # DIQQAT: javobni oshkor qiladigan matnni (masalan "Mushuk miyovladi")
    # ovozga bermang — bunday topshiriqlarga haqiqiy ovoz fayli kerak.
    audio_matn = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Audio matni',
        help_text='Ovoz fayli bo\'lmasa shu matn o\'qib eshittiriladi.',
    )
    audio_fayl = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Audio fayli',
        help_text='static papkasiga nisbatan yo\'l, masalan: '
                  'audio/topshiriq/mushuk-miyovlashi.wav',
    )
    rasm = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Rasm',
        help_text='static papkasiga nisbatan yo\'l, masalan: images/topshiriq/bola.png',
    )
    izoh = models.TextField(blank=True, verbose_name='Izoh / baholash mezoni')
    byudjet = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Byudjet (tanga)',
        help_text='"Xarid qilish" turida bolaga berilgan pul miqdori.',
    )
    boyash = models.TextField(
        blank=True,
        verbose_name='Bo\'yash chizmasi (SVG)',
        help_text='Bo\'yaladigan har bir soha data-soha="nom" bilan belgilanadi. '
                  'Agar soha data-togri="#rang" ham olsa, u aynan shu rangga '
                  'bo\'yalishi kerak; aks holda bola istagan rangni tanlaydi.',
    )
    labirint = models.TextField(
        blank=True,
        verbose_name='Labirint xaritasi',
        help_text='Har bir qator bitta satr. # — devor, nuqta — yo\'l, '
                  'R — robot boshlanishi, H — uy. Masalan:\n'
                  '#######\n#R#...#\n#.#.#.#\n#...#H#\n#######',
    )
    variant_matni_korinsin = models.BooleanField(
        default=False,
        verbose_name='Rasm yonida variant matni ham ko\'rinsin',
        help_text='Odatda rasmli variantda faqat rasm ko\'rsatiladi. Matnning '
                  'o\'zi topshiriq mazmuni bo\'lganda (masalan hikoya gaplarini '
                  'tartiblashda) shu bayroqni yoqing.',
    )

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['bolimcha', 'order'],
                condition=models.Q(kvest__isnull=True),
                name='unique_savol_order',
            ),
        ]
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'

    def __str__(self):
        return f'{self.bolimcha.name} — {self.order}-savol ({self.get_daraja_display()})'

    TUR_EMOJI = {
        Tur.TANLOV: '❓',
        Tur.KOPTANLOV: '☑️',
        Tur.XARID: '🛒',
        Tur.TARTIB: '🧩',
        Tur.MOSLASH: '🔗',
        Tur.GURUH: '🧺',
        Tur.QURISH: '🏗️',
        Tur.LABIRINT: '🤖',
        Tur.BOYASH: '🎨',
        Tur.MIKROFON: '🎤',
        Tur.KVEST: '🏆',
    }

    @property
    def aytiladigan_matn(self):
        return self.ovoz_matn or self.matn

    @property
    def tur_emoji(self):
        return self.TUR_EMOJI.get(self.tur, '❓')

    @property
    def boyash_sohalari(self):
        """Chizmadagi sohalar: {soha nomi: kutilgan rang yoki None}."""
        sohalar = {}
        for parcha in re.findall(r'<[^>]*data-soha=[^>]*>', self.boyash):
            nom = re.search(r'data-soha="([^"]+)"', parcha)
            togri = re.search(r'data-togri="([^"]+)"', parcha)
            if nom:
                sohalar[nom.group(1)] = togri.group(1).lower() if togri else None
        return sohalar

    def boyash_toldirilganmi(self, javob):
        """Bo'yalgan sohalarni tekshiradi.

        Har bir soha bo'yalgan bo'lishi kerak. Namuna berilgan sohalar
        (data-togri) aynan o'sha rangga bo'yalishi shart; qolganlarida bola
        istagan rangni tanlashi mumkin — erkin ijod topshiriqlari shunday.
        """
        try:
            berilgan = json.loads(javob or '{}')
        except (ValueError, TypeError):
            return False
        if not isinstance(berilgan, dict):
            return False

        sohalar = self.boyash_sohalari
        if not sohalar:
            return False
        for nom, kutilgan in sohalar.items():
            rang = str(berilgan.get(nom, '')).strip().lower()
            if not rang:
                return False
            if kutilgan and rang != kutilgan:
                return False
        return True

    @property
    def labirint_qatorlari(self):
        """Labirint xaritasini qatorlar ro'yxatiga aylantiradi."""
        return [q for q in (s.strip() for s in self.labirint.splitlines()) if q]

    def _labirint_joyi(self, belgi):
        for y, qator in enumerate(self.labirint_qatorlari):
            x = qator.find(belgi)
            if x >= 0:
                return x, y
        return None

    def labirint_yechildimi(self, yurishlar):
        """Yurishlar ketma-ketligini xaritada bosib chiqadi va uyga yetganini tekshiradi.

        `yurishlar` — U/D/L/R harflaridan iborat satr. Devorga qaragan yurish
        e'tiborga olinmaydi (brauzer ham unday yurishga ruxsat bermaydi).
        """
        xarita = self.labirint_qatorlari
        bosh = self._labirint_joyi('R')
        uy = self._labirint_joyi('H')
        if not xarita or not bosh or not uy:
            return False

        yonalish = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
        x, y = bosh
        for harf in (yurishlar or '').upper()[:400]:
            dx, dy = yonalish.get(harf, (0, 0))
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(xarita) and 0 <= nx < len(xarita[ny]) \
                    and xarita[ny][nx] != '#':
                x, y = nx, ny
        return (x, y) == uy

    def tekshir(self, post):
        """POST ma'lumotidan javobning to'g'riligini aniqlaydi."""
        if self.tur == self.Tur.TANLOV:
            javob = post.get(f'javob_{self.pk}') or post.get('javob')
            try:
                javob = int(javob)
            except (ValueError, TypeError):
                return False
            return self.variantlar.filter(pk=javob, togri=True).exists()

        if self.tur in (self.Tur.KOPTANLOV, self.Tur.XARID):
            # Belgilangan to'plam to'g'ri to'plam bilan aynan mos kelishi kerak
            belgilangan = set(post.getlist(f'tanlangan_{self.pk}'))
            kerak = {str(pk) for pk in
                     self.variantlar.filter(togri=True).values_list('pk', flat=True)}
            return belgilangan == kerak

        if self.tur == self.Tur.TARTIB:
            berilgan = post.getlist(f'tartib_{self.pk}') or post.getlist('tartib')
            elementlar = {str(v.pk): v for v in self.variantlar.all()}
            if len(berilgan) != len(elementlar):
                return False
            # Bir xil ko'rinishdagi kartochkalar (masalan ikkita bir xil strelka)
            # o'zaro almashishi mumkin, shuning uchun aynan qaysi kartochka emas,
            # uning ko'rinishi solishtiriladi.
            def belgi(v):
                return v.rasm or v.matn

            kutilgan = [belgi(v) for v in self.variantlar.order_by('togri_order')]
            qoyilgan = [belgi(elementlar[pk]) for pk in berilgan if pk in elementlar]
            return len(qoyilgan) == len(kutilgan) and qoyilgan == kutilgan

        if self.tur == self.Tur.MOSLASH:
            for v in self.variantlar.all():
                if (post.get(f'moslash_{self.pk}_{v.pk}') or
                        post.get(f'moslash_{v.pk}')) != str(v.pk):
                    return False
            return True

        if self.tur == self.Tur.GURUH:
            # Har bir element o'z savatiga tushishi kerak; savat kaliti — juft_matn
            for v in self.variantlar.all():
                if post.get(f'guruh_{self.pk}_{v.pk}') != v.juft_matn:
                    return False
            return True

        if self.tur == self.Tur.QURISH:
            # Har bir uyaga to'g'ri bo'lak qo'yilishi kerak. Bir xil ko'rinishdagi
            # bo'laklar o'zaro almashishi mumkin, shuning uchun aynan qaysi bo'lak
            # emas, uning ko'rinishi solishtiriladi.
            bolaklar = {str(v.pk): v for v in self.variantlar.all()}
            for v in bolaklar.values():
                if v.oldindan:
                    continue          # namunada tayyor turgan bo'lak
                qoyilgan = bolaklar.get(post.get(f'qurish_{self.pk}_{v.togri_order}', ''))
                if qoyilgan is None or qoyilgan.rasm != v.rasm:
                    return False
            return True

        if self.tur == self.Tur.LABIRINT:
            return self.labirint_yechildimi(post.get(f'labirint_{self.pk}', ''))

        if self.tur == self.Tur.BOYASH:
            return self.boyash_toldirilganmi(post.get(f'boyash_{self.pk}', ''))

        if self.tur == self.Tur.MIKROFON:
            # Ovoz yozilgan bo'lsa qabul qilinadi, sifatini tarbiyachi baholaydi
            return bool(post.get(f'ovoz_{self.pk}') or post.get('ovoz'))

        if self.tur == self.Tur.KVEST:
            return all(b.tekshir(post) for b in self.bosqichlar.all())

        return False


class Variant(models.Model):
    """Topshiriq elementi: tanlov varianti, ketma-ketlik bo'lagi yoki juftlik."""

    savol = models.ForeignKey(
        Savol,
        on_delete=models.CASCADE,
        related_name='variantlar',
        verbose_name='Savol',
    )
    order = models.PositiveIntegerField(verbose_name='Ko\'rsatish tartibi')
    matn = models.CharField(max_length=255, blank=True, verbose_name='Matn')
    emoji = models.CharField(max_length=16, blank=True, verbose_name='Emoji')
    rasm = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Rasm',
        help_text='static papkasiga nisbatan yo\'l, masalan: '
                  'images/topshiriq/variantlar/olma.png. Rasm berilsa, ekranda '
                  'faqat rasm ko\'rinadi; matn ekranni o\'qib beruvchi '
                  'dasturlar uchun saqlanadi.',
    )
    rang = models.CharField(
        max_length=20, blank=True,
        verbose_name='Rang',
        help_text='Rang topshiriqlari uchun CSS rangi, masalan #e94b4b',
    )
    # tanlov turi uchun
    togri = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    # xarid turi uchun
    narx = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Narxi (tanga)',
    )
    # tartib turi uchun
    togri_order = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="To'g'ri ketma-ketlikdagi o'rni",
    )
    # moslash turi uchun — shu variantga mos keladigan juftlik
    juft_matn = models.CharField(max_length=255, blank=True, verbose_name='Juftlik matni')
    juft_emoji = models.CharField(max_length=16, blank=True, verbose_name='Juftlik emojisi')
    juft_rasm = models.CharField(
        max_length=200, blank=True, verbose_name='Juftlik rasmi',
        help_text='static papkasiga nisbatan yo\'l. Berilsa, juftlikda '
                  'faqat rasm ko\'rinadi. "Savatlarga ajratish" turida bu '
                  'savatning rasmi, juftlik matni esa savat nomi bo\'ladi.',
    )
    # qurish turi uchun — namunadagi uyaning o'rni
    slot = models.CharField(
        max_length=40, blank=True, verbose_name='Uya joyi',
        help_text='"Namunaga qarab yig\'ish" turida uyaning joyi foizda: '
                  'x,y,kenglik,balandlik — masalan 10,60,25,30',
    )
    oldindan = models.BooleanField(
        default=False, verbose_name='Oldindan qo\'yilgan',
        help_text='Bo\'lak boshidanoq o\'z joyida turadi (masalan simmetriya '
                  'topshirig\'ida rasmning berilgan yarmi).',
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Variant'
        verbose_name_plural = 'Variantlar'

    def __str__(self):
        return f'{self.savol_id} — {self.emoji} {self.matn}'.strip()

    @property
    def belgi(self):
        return f'{self.emoji} {self.matn}'.strip()

    @property
    def slot_uslubi(self):
        """Uya joyini ("x,y,w,h" foizda) CSS uslubiga aylantiradi."""
        qismlar = [q.strip() for q in self.slot.split(',')] if self.slot else []
        if len(qismlar) != 4:
            return ''
        x, y, w, h = qismlar
        return f'left:{x}%;top:{y}%;width:{w}%;height:{h}%'


class SavolNatija(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='natijalar',
        verbose_name='Foydalanuvchi',
    )
    savol = models.ForeignKey(
        Savol,
        on_delete=models.CASCADE,
        related_name='natijalar',
        verbose_name='Savol',
    )
    stars = models.PositiveSmallIntegerField(verbose_name='Yulduzlar')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'savol'], name='unique_user_savol'),
        ]
        verbose_name = 'Savol natijasi'
        verbose_name_plural = 'Savol natijalari'

    def __str__(self):
        return f'{self.user.username} — {self.savol} — {self.stars}⭐'


class OvozJavob(models.Model):
    """Mikrofonli topshiriqda bola yozgan ovoz — tarbiyachi keyin tinglab baholaydi."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ovoz_javoblar',
        verbose_name='Foydalanuvchi',
    )
    savol = models.ForeignKey(
        Savol,
        on_delete=models.CASCADE,
        related_name='ovoz_javoblar',
        verbose_name='Savol',
    )
    fayl = models.FileField(
        storage=private_voice_storage, upload_to='ovoz/%Y/%m/', verbose_name='Ovoz fayli',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    tarbiyachi_bahosi = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='Tarbiyachi bahosi (1–3 yulduz)',
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    )
    tarbiyachi_izohi = models.TextField(blank=True, max_length=1000, verbose_name='Tarbiyachi izohi')
    baholagan = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='baholangan_ovozlar', verbose_name='Baholagan',
    )
    baholangan_at = models.DateTimeField(null=True, blank=True, verbose_name='Baholangan vaqt')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ovozli javob'
        verbose_name_plural = 'Ovozli javoblar'

    def __str__(self):
        return f'{self.user.username} — {self.savol_id} — {self.created_at:%d.%m.%Y %H:%M}'
