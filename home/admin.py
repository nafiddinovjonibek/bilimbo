import asyncio

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q

from .models import Bolim, Bolimcha, OvozJavob, Savol, SavolNatija, User, Variant
from .tts import audio_ready, generate_speech, question_texts, speech_path


class SavolInline(admin.TabularInline):
    model = Savol
    extra = 0
    fk_name = 'bolimcha'
    fields = ('order', 'daraja', 'tur', 'sarlavha', 'matn')


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


class BosqichInline(admin.TabularInline):
    model = Savol
    fk_name = 'kvest'
    extra = 0
    fields = ('order', 'tur', 'sarlavha', 'matn')
    verbose_name_plural = 'Kvest bosqichlari'


@admin.register(Savol)
class SavolAdmin(admin.ModelAdmin):
    list_display = ('order', 'daraja', 'tur', 'sarlavha', 'matn', 'bolimcha')
    list_display_links = ('matn',)
    list_filter = ('bolimcha__bolim', 'bolimcha', 'daraja', 'tur')
    inlines = [VariantInline, BosqichInline]
    actions = ['prepare_question_audio']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        self._prepare_audio(request, [form.instance, *form.instance.bosqichlar.all()])

    @admin.action(description='Tanlangan savollar ovozini tayyorlash / yangilash')
    def prepare_question_audio(self, request, queryset):
        ids = list(queryset.values_list('pk', flat=True))
        questions = Savol.objects.filter(Q(pk__in=ids) | Q(kvest_id__in=ids))
        self._prepare_audio(request, questions)

    def _prepare_audio(self, request, questions):
        pending = set()
        for _, _, text in question_texts(questions):
            relative = speech_path(text)
            if relative and not audio_ready(settings.BASE_DIR / 'static' / relative):
                pending.add(text)
        if not pending:
            return

        async def create():
            semaphore = asyncio.Semaphore(3)

            async def make(text):
                async with semaphore:
                    return await generate_speech(text, timeout=15, attempts=1)

            return await asyncio.gather(*(make(text) for text in pending), return_exceptions=True)

        results = asyncio.run(create())
        failed = sum(isinstance(result, Exception) for result in results)
        if failed:
            self.message_user(
                request, f'Ma’lumot saqlandi, lekin {failed} ta ovoz yaratilmagan. '
                'Internetni tekshirib, “Savollar ovozini tayyorlash / yangilash” amalini qayta bajaring.',
                level=messages.WARNING)
        else:
            self.message_user(request, 'Savolning o‘zbekcha ovozi tayyor.', level=messages.SUCCESS)


@admin.register(SavolNatija)
class SavolNatijaAdmin(admin.ModelAdmin):
    list_display = ('user', 'savol', 'stars', 'updated_at')
    list_filter = ('savol__bolimcha', 'stars')


@admin.register(OvozJavob)
class OvozJavobAdmin(admin.ModelAdmin):
    """Tarbiyachi bolalarning ovozli javoblarini shu yerda tinglab baholaydi."""

    list_display = ('user', 'savol', 'created_at', 'tarbiyachi_bahosi')
    list_filter = ('savol__bolimcha', 'tarbiyachi_bahosi')
    readonly_fields = ('user', 'savol', 'fayl', 'created_at')


class BolimchaInline(admin.TabularInline):
    model = Bolimcha
    extra = 0


@admin.register(Bolim)
class BolimAdmin(admin.ModelAdmin):
    list_display = ('order', 'emoji', 'name')
    list_display_links = ('name',)
    inlines = [BolimchaInline]


@admin.register(Bolimcha)
class BolimchaAdmin(admin.ModelAdmin):
    list_display = ('order', 'emoji', 'name', 'bolim')
    list_display_links = ('name',)
    list_filter = ('bolim',)
    inlines = [SavolInline]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol', {'fields': ('role',)}),
    )
