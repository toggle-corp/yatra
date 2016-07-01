# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 05:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0006_auto_20160701_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='trippoint',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trippoint',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]