# Generated by Django 2.0.13 on 2019-07-26 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20190726_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='variations',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
