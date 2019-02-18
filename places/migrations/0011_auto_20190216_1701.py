# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-16 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0010_auto_20190216_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercityrate',
            name='rate',
            field=models.IntegerField(choices=[(1, 'Bad'), (2, 'Below Average'), (3, 'Average'), (4, 'Very Good'), (5, 'Excelent')], default=3),
        ),
    ]