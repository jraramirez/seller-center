from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel


@register_snippet
class Product(models.Model):
  product_code = models.CharField(null=True, blank=True, max_length=500)
  merchant_id = models.CharField(null=True, blank=True, max_length=500)
  category_id = models.CharField(null=True, blank=True, max_length=500)
  product_name = models.CharField(null=True, blank=True, max_length=500)
  product_description = models.CharField(null=True, blank=True, max_length=500)
  price = models.CharField(null=True, blank=True, max_length=500)
  stock = models.CharField(null=True, blank=True, max_length=500)
  product_weight = models.CharField(null=True, blank=True, max_length=500)
  ship_out_in = models.CharField(null=True, blank=True, max_length=500)
  parent_sku_reference_no = models.CharField(null=True, blank=True, max_length=500)
  variation1_id = models.CharField(null=True, blank=True, max_length=500)
  variation2_id = models.CharField(null=True, blank=True, max_length=500)
  variation3_id = models.CharField(null=True, blank=True, max_length=500)
  variation4_id = models.CharField(null=True, blank=True, max_length=500)
  variation5_id = models.CharField(null=True, blank=True, max_length=500)
  variation6_id = models.CharField(null=True, blank=True, max_length=500)
  variation7_id = models.CharField(null=True, blank=True, max_length=500)
  image1 = models.CharField(null=True, blank=True, max_length=500)
  image2 = models.CharField(null=True, blank=True, max_length=500)
  image3 = models.CharField(null=True, blank=True, max_length=500)
  image4 = models.CharField(null=True, blank=True, max_length=500)
  image5 = models.CharField(null=True, blank=True, max_length=500)
  image6 = models.CharField(null=True, blank=True, max_length=500)
  image7 = models.CharField(null=True, blank=True, max_length=500)
  other_logistics_provider_setting = models.CharField(null=True, blank=True, max_length=500)
  other_logistics_provider_fee = models.CharField(null=True, blank=True, max_length=500)

  def save(self, *args, **kwargs):
    super(Product, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.product_name


class ProductPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)
