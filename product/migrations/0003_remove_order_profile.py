# Generated by Django 2.0.13 on 2019-09-17 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190917_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='profile',
        ),
    ]
