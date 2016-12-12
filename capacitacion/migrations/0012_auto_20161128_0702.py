# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0011_auto_20161125_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='local',
            name='cantidad_total_auditorios',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_total_aulas',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_total_oficina',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_total_otros',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='local',
            name='cantidad_total_sala',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
