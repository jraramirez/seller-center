# Generated by Django 2.0.2 on 2019-07-10 12:42

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImportPage',
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
