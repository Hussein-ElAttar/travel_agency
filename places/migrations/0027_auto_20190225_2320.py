# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-25 23:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0026_auto_20190223_2308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='country_Name',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='city_Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='city_is_crawled',
            new_name='is_crawled',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='city_Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='city_Pic',
            new_name='pic',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='country_Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='country_Pic',
            new_name='pic',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='city_Name',
            new_name='name',
        ),
    ]
