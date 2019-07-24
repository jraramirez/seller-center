from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.models import ClusterableModel

from users.models import Profile

@register_snippet
class Order(models.Model):
  total = models.CharField(null=True, blank=True, max_length=500)
  status = models.CharField(null=True, blank=True, max_length=500)
  countdown = models.CharField(null=True, blank=True, max_length=500)
  shipping_channel = models.CharField(null=True, blank=True, max_length=500)
  creation_date = models.CharField(null=True, blank=True, max_length=500)
  paid_date = models.CharField(null=True, blank=True, max_length=500)

  panels = [
    FieldPanel('status'),
    FieldPanel('countdown'),
    FieldPanel('shipping_channel'),
    FieldPanel('creation_date'),
  ]

@register_snippet
class Category(models.Model):
  name = models.CharField(null=True, blank=True, max_length=500)

  panels = [
    FieldPanel('name'),
  ]

@register_snippet
class Product(models.Model):
  product_code = models.CharField(null=True, blank=True, max_length=500)
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
  order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
  profile = models.ForeignKey(Profile, models.DO_NOTHING, blank=True, null=True)
  category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
  live = models.BooleanField(default=False)
  suspended = models.BooleanField(default=False)
  unlisted = models.BooleanField(default=False)

  def save_model(self, request, obj, form, change):
    obj.user_id = request.user.id
    super().save_model(request, obj, form, change)

  # def save(self, *args, **kwargs):
  #   Product.user_id = request.user.id
  #   super(Product, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.product_name


class ProductPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)

  def get_context(self, request):
    context = super().get_context(request)
    return context


class ProductsPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)
  
  def get_context(self, request):
    context = super().get_context(request)
    allProducts = Product.objects.all()
    liveProducts = Product.objects.filter(live=True)
    soldOutProducts = Product.objects.filter(stock='0')
    suspendedProducts = Product.objects.filter(suspended=True)
    unlistedProducts = Product.objects.filter(unlisted=True)
    subPages = self.get_children().live()
    context['allProducts'] = allProducts
    context['liveProducts'] = liveProducts
    context['soldOutProducts'] = soldOutProducts
    context['suspendedProducts'] = suspendedProducts
    context['unlistedProducts'] = unlistedProducts
    context['subPages'] = subPages
    return context


class ProductImportPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)


class ProductsImportPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)
