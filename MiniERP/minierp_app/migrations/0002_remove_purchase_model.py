# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-30 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minierp_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='model',
        ),
    ]
