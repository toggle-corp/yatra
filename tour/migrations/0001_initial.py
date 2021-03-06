# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 07:03
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('destination', models.CharField(max_length=200)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.Plan')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TripPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('next_point', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.TripPoint')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='starting_point',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tour.TripPoint'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('plan', 'posted_by')]),
        ),
    ]
