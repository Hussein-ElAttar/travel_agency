# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-20 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0024_auto_20190220_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_Description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='city_Pic',
            field=models.ImageField(blank=True, max_length=250, null=True, upload_to='cities'),
        ),
        migrations.AlterField(
            model_name='country',
            name='country_Pic',
            field=models.ImageField(blank=True, max_length=250, null=True, upload_to='countries'),
        ),
    ]
