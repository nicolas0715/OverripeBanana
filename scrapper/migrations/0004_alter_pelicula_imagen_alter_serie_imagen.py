# Generated by Django 4.1 on 2023-10-07 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0003_alter_pelicula_fecha_streaming_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='imagen',
            field=models.URLField(max_length=500, verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='imagen',
            field=models.URLField(max_length=500, verbose_name='Imagen_Serie'),
        ),
    ]