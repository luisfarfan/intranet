# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-05 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0022_pea_asistencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pea_asistencia',
            name='marcacion',
        ),
        migrations.AddField(
            model_name='pea_asistencia',
            name='fecha',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pea_asistencia',
            name='turno_manana',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pea_asistencia',
            name='turno_tarde',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
