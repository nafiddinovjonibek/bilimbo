import asyncio

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Bolim, Bolimcha, Guruh, Kitob, OvozJavob, Savol, SavolNatija, User, Variant
from .narakeet import NarakeetConfigurationError
from .tts import audio_ready, generate_speech, question_texts, speech_path


class SuperadminAdminMixin:
    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_superadmin

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)


class SavolInline(admin.TabularInline):
    model = Savol
    extra = 0
    fk_name = 'bolimcha'
    fields = ('order', 'daraja', 'tur', 'sarlavha', 'matn')


@admin.register(Kitob)
class KitobAdmin(SuperadminAdminMixin, admin.ModelAdmin):
    list_display = ('nom', 'manba', 'sahifalar', 'order', 'faol')
    list_filter = ('faol',)
    search_fields = ('nom', 'mualliflar')
    list_editable = ('order', 'faol')
    fields = ('nom', 'mualliflar', 'order', 'faol', 'manba', 'sahifalar')
    readonly_fields = ('manba', 'sahifalar')

    def has_add_permission(self, request):
        # Fayllar tekshirilgan import_kitoblar buyrug'i orqali qo'shiladi.
        return False


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
class SavolAdmin(SuperadminAdminMixin, admin.ModelAdmin):
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
        configuration_error = next((result for result in results
                                    if isinstance(result, NarakeetConfigurationError)), None)
        if configuration_error:
            self.message_user(request, f'Ma’lumot saqlandi. {configuration_error}', level=messages.WARNING)
            return
        failed = sum(isinstance(result, Exception) for result in results)
        if failed:
            self.message_user(
                request, f'Ma’lumot saqlandi, lekin {failed} ta ovoz yaratilmagan. '
                'Internetni tekshirib, “Savollar ovozini tayyorlash / yangilash” amalini qayta bajaring.',
                level=messages.WARNING)
        else:
            self.message_user(request, 'Savolning o‘zbekcha ovozi tayyor.', level=messages.SUCCESS)


@admin.register(SavolNatija)
class SavolNatijaAdmin(SuperadminAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'savol', 'stars', 'updated_at')
    list_filter = ('savol__bolimcha', 'stars')


@admin.register(OvozJavob)
class OvozJavobAdmin(SuperadminAdminMixin, admin.ModelAdmin):
    """Administrator ovozli javoblarni boshqaradi; tarbiyachi uchun /kabinet/ mavjud."""

    list_display = ('user', 'savol', 'created_at', 'tarbiyachi_bahosi')
    list_filter = ('savol__bolimcha', 'tarbiyachi_bahosi')
    readonly_fields = ('user', 'savol', 'tinglash', 'created_at', 'baholagan', 'baholangan_at')
    fields = ('user', 'savol', 'tinglash', 'created_at', 'tarbiyachi_bahosi', 'tarbiyachi_izohi', 'baholagan', 'baholangan_at')

    @admin.display(description='Ovozli javob')
    def tinglash(self, obj):
        if not obj.pk or not obj.fayl:
            return 'Ovoz fayli yo‘q'
        return format_html('<audio controls preload="none" src="{}"></audio>', reverse('ovoz_fayl', args=[obj.pk]))

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        obj.baholagan = request.user if obj.tarbiyachi_bahosi else None
        obj.baholangan_at = timezone.now() if obj.tarbiyachi_bahosi else None
        super().save_model(request, obj, form, change)


class BolimchaInline(admin.TabularInline):
    model = Bolimcha
    extra = 0


@admin.register(Bolim)
class BolimAdmin(SuperadminAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'emoji', 'name')
    list_display_links = ('name',)
    inlines = [BolimchaInline]


@admin.register(Bolimcha)
class BolimchaAdmin(SuperadminAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'emoji', 'name', 'bolim')
    list_display_links = ('name',)
    list_filter = ('bolim',)
    inlines = [SavolInline]


@admin.register(User)
class CustomUserAdmin(SuperadminAdminMixin, UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'teacher_approved', 'guruh', 'is_active')
    list_filter = ('role', 'teacher_approved', 'guruh', 'is_active')
    actions = ('approve_teachers', 'revoke_teachers')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol va guruh', {'fields': ('role', 'teacher_approved', 'guruh')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol va guruh', {'fields': ('role', 'teacher_approved', 'guruh')}),
    )

    @admin.action(description='Tanlangan tarbiyachilarni tasdiqlash')
    def approve_teachers(self, request, queryset):
        count = queryset.filter(role=User.Role.TARBIYACHI, is_superuser=False).update(teacher_approved=True)
        self.message_user(request, f'{count} ta tarbiyachi tasdiqlandi.')

    @admin.action(description='Tanlangan tarbiyachilar tasdig‘ini bekor qilish')
    def revoke_teachers(self, request, queryset):
        count = queryset.filter(role=User.Role.TARBIYACHI, is_superuser=False).update(teacher_approved=False)
        self.message_user(request, f'{count} ta tarbiyachi tasdig‘i bekor qilindi.')


@admin.register(Guruh)
class GuruhAdmin(SuperadminAdminMixin, admin.ModelAdmin):
    list_display = ('nom', 'tarbiyachi', 'created_at')
    list_filter = ('tarbiyachi',)
    search_fields = ('nom', 'tarbiyachi__username', 'tarbiyachi__first_name')
