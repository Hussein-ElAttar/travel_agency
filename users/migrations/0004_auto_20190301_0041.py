# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-03-01 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190215_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(upload_to='avatar/'),
        ),
    ]
