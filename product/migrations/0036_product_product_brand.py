# Generated by Django 2.0.2 on 2019-09-01 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_auto_20190831_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_brand',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
