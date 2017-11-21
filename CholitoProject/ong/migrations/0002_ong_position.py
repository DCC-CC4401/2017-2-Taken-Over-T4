# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 00:03
from __future__ import unicode_literals

from django.db import migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ong', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ong',
            name='position',
            field=geoposition.fields.GeopositionField(default=0, max_length=42),
            preserve_default=False,
        ),
    ]
