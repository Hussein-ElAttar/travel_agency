# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-18 09:53
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0019_auto_20190217_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHotelRes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateFrom', models.DateTimeField(default=datetime.datetime.now)),
                ('datetTo', models.DateTimeField(default=datetime.datetime.now)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
