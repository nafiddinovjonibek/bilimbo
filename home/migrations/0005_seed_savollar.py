from django.db import migrations


def daraja_by_order(order):
    if order <= 3:
        return 'oson'
    if order <= 6:
        return 'orta'
    if order <= 9:
        return 'qiyin'
    return 'tanqidiy'


def seed(apps, schema_editor):
    Bolimcha = apps.get_model('home', 'Bolimcha')
    Savol = apps.get_model('home', 'Savol')

    for sub in Bolimcha.objects.all():
        for order in range(1, 11):
            Savol.objects.create(
                bolimcha=sub,
                order=order,
                daraja=daraja_by_order(order),
                matn=f'{sub.name}: {order}-savol matni shu yerda bo\'ladi. To\'g\'ri javobni tanlang!',
                variant_a='Birinchi javob',
                variant_b='Ikkinchi javob',
                variant_c='Uchinchi javob',
                togri_javob='abc'[order % 3],
            )


def unseed(apps, schema_editor):
    apps.get_model('home', 'Savol').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_savol_savolnatija_savol_unique_savol_order_and_more'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
