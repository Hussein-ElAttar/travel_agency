# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-16 17:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0011_auto_20190216_1701'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercityrate',
            unique_together=set([('user', 'city')]),
        ),
    ]
