# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-14 19:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0002_auto_20170114_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='local',
            name='marcolocal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='capacitacion.MarcoLocal'),
        ),
    ]
