"""Bitta mavjud sanoq savolining sharti va rasmini yangilash."""
import json
from pathlib import Path

from django.db import migrations


def rewrite(apps, direction):
    Savol = apps.get_model('home', 'Savol')
    Variant = apps.get_model('home', 'Variant')
    content = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf8'))
    section, level, order = map(int, content['key'].split('.'))
    question = Savol.objects.filter(
        bolimcha__bolim__order=section, bolimcha__order=level,
        order=order, kvest__isnull=True, tur=content['tur'],
    ).first()
    if question is None:
        return
    variants = list(Variant.objects.filter(savol_id=question.pk).values('matn', 'togri'))
    if sorted(variants, key=lambda value: value['matn']) != content['variants']:
        return  # Admin o‘zgartirgan javoblarni qayta yozmaydi.
    Savol.objects.filter(pk=question.pk).update(**content[direction])


def forwards(apps, schema_editor):
    rewrite(apps, 'after')


def backwards(apps, schema_editor):
    rewrite(apps, 'before')


class Migration(migrations.Migration):
    dependencies = [('home', '0022_topshiriqlarni_takomillashtirish')]
    operations = [migrations.RunPython(forwards, backwards)]
