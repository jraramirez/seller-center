# Generated by Django 2.0.2 on 2019-08-10 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20190806_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_width',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
