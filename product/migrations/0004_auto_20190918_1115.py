# Generated by Django 2.0.13 on 2019-09-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_order_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cover_image_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]