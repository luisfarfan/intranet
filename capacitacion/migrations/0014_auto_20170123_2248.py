# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 03:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0013_auto_20170123_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='CursoLocal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capacitacion.Curso')),
            ],
            options={
                'db_table': 'CURSO_LOCAL',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='usuariolocal',
            name='id_directoriolocal',
        ),
        migrations.RemoveField(
            model_name='usuariolocal',
            name='id_usuario',
        ),
        migrations.RemoveField(
            model_name='directoriolocal',
            name='usuarios',
        ),
        migrations.RemoveField(
            model_name='local',
            name='marcolocal',
        ),
        migrations.RemoveField(
            model_name='local',
            name='usuario_local',
        ),
        migrations.AlterField(
            model_name='directoriolocal',
            name='id_curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curso_directorio', to='capacitacion.Curso'),
        ),
        migrations.DeleteModel(
            name='UsuarioLocal',
        ),
        migrations.AddField(
            model_name='cursolocal',
            name='id_cursolocal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capacitacion.DirectorioLocal'),
        ),
        migrations.AddField(
            model_name='directoriolocal',
            name='cursos_locales',
            field=models.ManyToManyField(related_name='cursos_local', through='capacitacion.CursoLocal', to='capacitacion.Curso'),
        ),
        migrations.AddField(
            model_name='local',
            name='curso_local',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capacitacion.CursoLocal'),
        ),
    ]
