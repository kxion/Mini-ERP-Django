# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-02 00:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minierp_app', '0004_auto_20170401_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minierp_app.StateSelection'),
        ),
        migrations.AlterField(
            model_name='supply',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minierp_app.StateSelection'),
        ),
    ]
