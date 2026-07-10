from django.contrib.auth.models import AbstractUser
from django.db import models


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

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_superadmin(self):
        return self.role == self.Role.SUPERADMIN

    @property
    def is_tarbiyachi(self):
        return self.role == self.Role.TARBIYACHI

    @property
    def is_oquvchi(self):
        return self.role == self.Role.OQUVCHI


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
    class Daraja(models.TextChoices):
        OSON = 'oson', 'Oson'
        ORTA = 'orta', "O'rta"
        QIYIN = 'qiyin', 'Qiyin'
        TANQIDIY = 'tanqidiy', 'Tanqidiy'

    VARIANTLAR = [('a', 'A'), ('b', 'B'), ('c', 'C')]

    bolimcha = models.ForeignKey(
        Bolimcha,
        on_delete=models.CASCADE,
        related_name='savollar',
        verbose_name="Bo'limcha",
    )
    order = models.PositiveIntegerField(verbose_name='Tartib raqami')
    daraja = models.CharField(max_length=10, choices=Daraja.choices, verbose_name='Daraja')
    matn = models.TextField(verbose_name='Savol matni')
    variant_a = models.CharField(max_length=255, verbose_name='A varianti')
    variant_b = models.CharField(max_length=255, verbose_name='B varianti')
    variant_c = models.CharField(max_length=255, verbose_name='C varianti')
    togri_javob = models.CharField(max_length=1, choices=VARIANTLAR, verbose_name="To'g'ri javob")

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['bolimcha', 'order'], name='unique_savol_order'),
        ]
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'

    def __str__(self):
        return f'{self.bolimcha.name} — {self.order}-savol ({self.get_daraja_display()})'


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
