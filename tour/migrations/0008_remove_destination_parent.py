# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 05:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0007_auto_20160701_0526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='parent',
        ),
    ]