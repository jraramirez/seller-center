from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.core.fields import RichTextField, StreamField


class FormField(AbstractFormField):
  page = ParentalKey('SignUpPage', related_name='form_fields')


class SignUpPage(AbstractEmailForm):
  agreement_message = RichTextField(null=True, blank=True)
  content_panels = AbstractEmailForm.content_panels + [
    InlinePanel('form_fields', label="Form fields"),
    FieldPanel('agreement_message'),
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
    