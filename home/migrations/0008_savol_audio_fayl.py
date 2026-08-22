from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_ovozjavob_variant_remove_savol_unique_savol_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='savol',
            name='audio_fayl',
            field=models.CharField(
                blank=True,
                max_length=200,
                verbose_name='Audio fayli',
                help_text="static papkasiga nisbatan yo'l, masalan: "
                          'audio/topshiriq/mushuk-miyovlashi.wav',
            ),
        ),
        migrations.AlterField(
            model_name='savol',
            name='audio_matn',
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name='Audio matni',
                help_text="Ovoz fayli bo'lmasa shu matn o'qib eshittiriladi.",
            ),
        ),
    ]
