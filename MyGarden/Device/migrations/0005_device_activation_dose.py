# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Device', '0004_auto_20170203_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='activation_dose',
            field=models.CharField(max_length=32, null=True),
        ),
    ]