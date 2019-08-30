# Generated by Django 2.0.13 on 2019-08-30 08:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_auto_20190829_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_sale_date_end',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_sale_date_start',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_sale_time_end',
            field=models.TimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_sale_time_start',
            field=models.TimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='variations',
            name='sale_date_end',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='variations',
            name='sale_date_start',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='variations',
            name='sale_time_end',
            field=models.TimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='variations',
            name='sale_time_start',
            field=models.TimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
