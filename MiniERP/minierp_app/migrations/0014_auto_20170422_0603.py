# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-22 06:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minierp_app', '0013_pendingpurchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profit',
            name='order_number',
        ),
        migrations.RemoveField(
            model_name='profit',
            name='purchase_number',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='product',
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='company_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='pendingpurchase',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='supply',
            name='address',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='supply',
            name='company_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='supply',
            name='contact_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='supply',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='supply',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.DeleteModel(
            name='Profit',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
    ]
