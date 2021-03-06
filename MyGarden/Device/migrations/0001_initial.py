# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 20:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('type', models.CharField(max_length=10)),
                ('subtype', models.CharField(max_length=10)),
                ('gpio_pin', models.IntegerField(null=True)),
                ('potency', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('potency_unit', models.CharField(max_length=32, null=True)),
                ('activation_mode', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_dt', models.DateTimeField()),
                ('message', models.CharField(max_length=100)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Device.Device')),
            ],
            options={
                'ordering': ('log_dt',),
            },
        ),
        migrations.CreateModel(
            name='DeviceSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_dt', models.DateTimeField()),
                ('change_to', models.IntegerField(null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Device.Device')),
            ],
            options={
                'ordering': ('event_dt',),
            },
        ),
    ]
