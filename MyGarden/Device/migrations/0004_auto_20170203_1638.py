# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Device', '0003_auto_20170203_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='activation_duration',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='activation_status',
            field=models.CharField(max_length=32, null=True),
        ),
    ]