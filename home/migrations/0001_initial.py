# Generated by Django 2.0.13 on 2019-07-04 07:49

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.BasePage')),
                ('body', wagtail.core.fields.StreamField([('content', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_block', wagtail.images.blocks.ImageChooserBlock(icon='image', label='Image Block'))], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('base.basepage',),
        ),
    ]
