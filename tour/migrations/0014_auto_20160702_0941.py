# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 09:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0013_auto_20160702_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='starting_point',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.TripPoint'),
        ),
    ]
