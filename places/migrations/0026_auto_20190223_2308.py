# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-23 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0025_auto_20190220_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityPics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='city_is_crawled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='citypics',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.City'),
        ),
    ]
