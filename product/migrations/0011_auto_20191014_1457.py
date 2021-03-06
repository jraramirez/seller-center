# Generated by Django 2.0.13 on 2019-10-14 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20191004_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_remark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, default='TO_SHIP', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='status',
            field=models.CharField(blank=True, default='TO_SHIP', max_length=500, null=True),
        ),
    ]
