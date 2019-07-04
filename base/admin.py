from django.contrib import admin
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

# Register your models here.

content_panels = Page.content_panels + [
  FieldPanel('page_title'),
  FieldPanel('page_subtitle'),
]