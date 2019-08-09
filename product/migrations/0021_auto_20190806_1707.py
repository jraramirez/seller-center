# Generated by Django 2.0.13 on 2019-08-06 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_auto_20190806_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variations',
            name='image_upload',
            field=models.ImageField(blank=True, help_text='Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.', null=True, upload_to='images'),
        ),
    ]