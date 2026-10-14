"""Mavjud simmetriya topshirig‘ini kapalakning mos bo‘laklari bilan yangilash."""
import json
from pathlib import Path

from django.db import migrations


def rewrite(apps, direction):
    Savol = apps.get_model('home', 'Savol')
    Variant = apps.get_model('home', 'Variant')
    data = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf8'))
    section, level, order = map(int, data['key'].split('.'))
    question = Savol.objects.filter(
        bolimcha__bolim__order=section, bolimcha__order=level,
        order=order, kvest__isnull=True, tur=data['tur'],
    ).first()
    if question is None:
        return
    variants = list(Variant.objects.filter(savol_id=question.pk).order_by('order'))
    updates = data['variants_' + direction]
    if [variant.order for variant in variants] != [entry['order'] for entry in updates]:
        return
    Savol.objects.filter(pk=question.pk).update(**data[direction])
    for variant, entry in zip(variants, updates):
        Variant.objects.filter(pk=variant.pk).update(
            matn=entry['matn'], rasm=entry['rasm'], slot=entry['slot'],
        )


def forwards(apps, schema_editor):
    rewrite(apps, 'after')


def backwards(apps, schema_editor):
    rewrite(apps, 'before')


class Migration(migrations.Migration):
    dependencies = [('home', '0026_qasr_topshirigini_yangilash')]
    operations = [migrations.RunPython(forwards, backwards)]
