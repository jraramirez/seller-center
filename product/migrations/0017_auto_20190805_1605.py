# Generated by Django 2.0.13 on 2019-08-05 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20190801_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]