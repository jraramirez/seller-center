# Generated by Django 2.0.13 on 2019-08-14 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_auto_20190814_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='errors',
            name='profile_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
