# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-22 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cacaosms', '0018_auto_20170822_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backend',
            name='id',
        ),
        migrations.AlterField(
            model_name='backend',
            name='nombre',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Nombre'),
        ),
    ]
