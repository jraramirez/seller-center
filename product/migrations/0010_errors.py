# Generated by Django 2.0.13 on 2019-07-31 08:16

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20190729_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Errors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('product', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='product.Product')),
            ],
        ),
    ]
