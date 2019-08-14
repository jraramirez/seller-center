from .models import *
from django.contrib import admin
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


ProductPage.content_panels = Page.content_panels + [
  FieldPanel('page_title'),
  FieldPanel('page_subtitle'),
  StreamFieldPanel('body'),
]