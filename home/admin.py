from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Bolim, Bolimcha, Savol, SavolNatija, User


class SavolInline(admin.TabularInline):
    model = Savol
    extra = 0
    fields = ('order', 'daraja', 'matn', 'variant_a', 'variant_b', 'variant_c', 'togri_javob')


@admin.register(Savol)
class SavolAdmin(admin.ModelAdmin):
    list_display = ('order', 'daraja', 'matn', 'bolimcha', 'togri_javob')
    list_display_links = ('matn',)
    list_filter = ('bolimcha__bolim', 'bolimcha', 'daraja')


@admin.register(SavolNatija)
class SavolNatijaAdmin(admin.ModelAdmin):
    list_display = ('user', 'savol', 'stars', 'updated_at')
    list_filter = ('savol__bolimcha', 'stars')


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
