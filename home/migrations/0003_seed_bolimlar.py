from django.db import migrations

# (emoji, bo'limchalar soni)
BOLIMLAR = [
    ('🚀', 3),
    ('🧩', 2),
    ('🎨', 3),
    ('🎵', 2),
    ('🌟', 2),
]

BOLIMCHA_EMOJILAR = ['🎯', '🎲', '🃏', '🔤', '🔢', '🖍️', '🧸', '🎪', '🥁', '🎤', '🏆', '🎁']


def seed(apps, schema_editor):
    Bolim = apps.get_model('home', 'Bolim')
    Bolimcha = apps.get_model('home', 'Bolimcha')

    counter = 1
    for i, (emoji, sub_count) in enumerate(BOLIMLAR, start=1):
        bolim = Bolim.objects.create(name=f"Bo'lim {i}", order=i, emoji=emoji)
        for _ in range(sub_count):
            Bolimcha.objects.create(
                bolim=bolim,
                name=f"Bo'limcha {counter}",
                order=counter,
                emoji=BOLIMCHA_EMOJILAR[counter - 1],
            )
            counter += 1


def unseed(apps, schema_editor):
    apps.get_model('home', 'Bolim').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_bolim_bolimcha'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
