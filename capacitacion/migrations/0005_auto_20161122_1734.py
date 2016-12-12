# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-22 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0004_auto_20161122_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='local',
            name='cantidad_disponible_auditorios',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_disponible_aulas',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_disponible_oficina',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_disponible_otros',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_disponible_sala',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_usar_auditorios',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_usar_oficina',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_usar_otros',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_usar_sala',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
