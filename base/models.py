from django.db import models
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock


class BasePage(Page):
  # Page Header
  page_title = models.CharField(max_length=200, blank=True, verbose_name='Title', help_text="Optional. If nothing is entered, the page title will be used.")
  page_subtitle = models.TextField(max_length=500, blank=True, verbose_name='Subtitle')
  

class GeneralStreamBlock(blocks.StreamBlock):
    content = blocks.RichTextBlock(icon="pilcrow")
    image_block = ImageChooserBlock(icon="image", label='Image Block')