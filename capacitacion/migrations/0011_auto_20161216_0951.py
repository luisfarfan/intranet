# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-16 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0010_auto_20161216_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='dni',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='nombre_completo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]