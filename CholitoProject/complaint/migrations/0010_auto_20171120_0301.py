# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-20 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0009_auto_20171120_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]