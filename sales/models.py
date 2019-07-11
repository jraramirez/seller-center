from django.db import models
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock
from wagtail.snippets.models import register_snippet


@register_snippet
class Order(models.Model):
  total = models.CharField(null=True, blank=True, max_length=500)
  status = models.CharField(null=True, blank=True, max_length=500)
  countdown = models.CharField(null=True, blank=True, max_length=500)
  shipping_channel = models.CharField(null=True, blank=True, max_length=500)
  creation_date = models.CharField(null=True, blank=True, max_length=500)
  paid_date = models.CharField(null=True, blank=True, max_length=500)

  def save(self, *args, **kwargs):
    super(Order, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.product_name


class SalesPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)
