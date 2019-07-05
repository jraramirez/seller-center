from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel


class FormField(AbstractFormField):
  page = ParentalKey('SignUpPage', related_name='form_fields')


class SignUpPage(AbstractEmailForm):

  content_panels = AbstractEmailForm.content_panels + [
    InlinePanel('form_fields', label="Form fields"),
    MultiFieldPanel([
      FieldRowPanel([
        FieldPanel('from_address', classname="col6"),
        FieldPanel('to_address', classname="col6"),
      ]),
      FieldPanel('subject'),
    ], "Email"),
  ]

  def get_context(self, request):
    context = super().get_context(request)
    return context
    