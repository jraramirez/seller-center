from django.db import models
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey


class SalesPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)
