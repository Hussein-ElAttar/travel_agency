# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-15 16:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_auto_20190215_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='country_Id',
            new_name='country_Name',
        ),
    ]
