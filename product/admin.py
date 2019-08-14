from .models import *
from django.contrib import admin
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


class ErrorsAdmin(admin.ModelAdmin):
  def save_model(self, request, obj, form, change):
    print("!")
    obj.user = request.user
    super().save_model(request, obj, form, change)
      

ProductPage.content_panels = Page.content_panels + [
  FieldPanel('page_title'),
  FieldPanel('page_subtitle'),
  StreamFieldPanel('body'),
]