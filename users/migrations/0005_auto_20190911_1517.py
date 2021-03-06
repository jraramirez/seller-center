# Generated by Django 2.0.13 on 2019-09-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190908_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='document',
            field=models.ImageField(blank=True, help_text='Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.', null=True, upload_to='documents'),
        ),
        migrations.AddField(
            model_name='sellerdetails',
            name='upload_id_back',
            field=models.ImageField(blank=True, help_text='Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.', null=True, upload_to='documents'),
        ),
        migrations.AddField(
            model_name='sellerdetails',
            name='upload_id_front',
            field=models.ImageField(blank=True, help_text='Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.', null=True, upload_to='documents'),
        ),
    ]
