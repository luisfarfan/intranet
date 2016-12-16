# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-15 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0007_auto_20161214_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuncionariosINEI',
            fields=[
                ('id_per', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('dni', models.CharField(blank=True, max_length=8, null=True)),
                ('ape_paterno', models.CharField(blank=True, db_column='ape_paterno', max_length=100, null=True)),
                ('ape_materno', models.CharField(blank=True, db_column='ape_materno', max_length=100, null=True)),
                ('nombre', models.CharField(blank=True, db_column='nombre', max_length=100, null=True)),
                ('cargo', models.CharField(blank=True, max_length=100, null=True)),
                ('correo', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono', models.CharField(blank=True, max_length=100, null=True)),
                ('celular', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'v_personal_contratado_cpv',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='local',
            name='funcionario_cargo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]