# Generated by Django 2.0.2 on 2019-07-29 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_stock_sum'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variations',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='variations',
            name='sort_order',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
