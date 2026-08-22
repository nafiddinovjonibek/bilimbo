from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Bolim, Bolimcha, OvozJavob, Savol, SavolNatija, User, Variant


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
