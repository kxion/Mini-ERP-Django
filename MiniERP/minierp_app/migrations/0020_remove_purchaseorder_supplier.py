# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-24 08:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minierp_app', '0019_purchaseorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='supplier',
        ),
    ]
