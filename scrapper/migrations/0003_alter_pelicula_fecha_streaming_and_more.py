# Generated by Django 4.1 on 2023-10-01 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0002_avatar_pelicula_streaming_serie_streaming_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='fecha_streaming',
            field=models.DateField(blank=True, verbose_name='Fecha_Streaming'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='ultimo_capitulo',
            field=models.DateField(blank=True, verbose_name='Ultimo_Capitulo'),
        ),
    ]