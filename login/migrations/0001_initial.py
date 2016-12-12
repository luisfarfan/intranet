# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-01 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=20)),
                ('clave', models.CharField(max_length=200)),
                ('nombre_completo', models.CharField(max_length=200)),
                ('ccdd', models.CharField(max_length=2)),
                ('ccpp', models.CharField(max_length=2)),
                ('ccdi', models.CharField(max_length=2)),
                ('zona', models.CharField(max_length=5)),
            ],
        ),
    ]
