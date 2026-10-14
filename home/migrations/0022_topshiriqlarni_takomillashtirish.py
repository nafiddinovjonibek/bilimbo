"""Mavjud topshiriqlarni ID, tur, daraja va sonini saqlab tahrirlash."""
import json
from pathlib import Path

from django.db import migrations


def rewrite(apps, direction):
    Savol = apps.get_model('home', 'Savol')
    Variant = apps.get_model('home', 'Variant')
    content = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf8'))
    for entry in content:
        primary, _, step = entry['key'].partition('/')
        section, level, order = map(int, primary.split('.'))
        question = Savol.objects.filter(
            bolimcha__bolim__order=section, bolimcha__order=level,
            order=order, kvest__isnull=True,
        ).first()
        if question is None:
            continue  # Admin o‘chirgan savolni qayta yaratmaydi.
        if step:
            question = Savol.objects.filter(kvest_id=question.pk, order=int(step)).first()
        if question is None or question.tur != entry['tur']:
            continue
        # Variantlarni PK bo‘yicha bog‘lash qayta tartiblanganda ham identifikatorlarni
        # saqlaydi. Eski seed ularni ketma-ket yaratgan; hech biri o‘chirilmaydi.
        variants = list(Variant.objects.filter(savol_id=question.pk).order_by('pk'))
        variant_data = entry['variants_' + direction]
        if len(variants) != len(variant_data):
            continue  # Admin qo‘shgan yoki o‘chirgan variantlar saqlanadi.
        Savol.objects.filter(pk=question.pk).update(**entry[direction])
        for variant, values in zip(variants, variant_data):
            Variant.objects.filter(pk=variant.pk).update(**values)


def forwards(apps, schema_editor):
    rewrite(apps, 'after')


def backwards(apps, schema_editor):
    rewrite(apps, 'before')


class Migration(migrations.Migration):
    dependencies = [('home', '0021_seed_sanat')]
    operations = [migrations.RunPython(forwards, backwards)]
