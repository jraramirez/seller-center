from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

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

class Category(models.Model):
  unique_id = models.IntegerField(null=True, blank=True)
  parent_id = models.IntegerField(null=True, blank=True)
  level = models.IntegerField(null=True, blank=True)
  name = models.CharField(null=True, blank=True, max_length=500)

@register_snippet
class Product(ClusterableModel):
  CONDITION_CHOICES = [
    ('N', 'New'),
    ('U', 'Used'),
  ]
  product_code = models.CharField(null=True, blank=True, max_length=500)
  product_name = models.CharField(null=True, blank=True, max_length=500)
  product_description = models.CharField(null=True, blank=True, max_length=500)
  product_weight = models.CharField(null=True, blank=True, max_length=500)
  product_condition = models.CharField(null=True, blank=True, choices=CONDITION_CHOICES, default=CONDITION_CHOICES[0], max_length=500)
  ship_out_in = models.CharField(null=True, blank=True, max_length=500)
  parent_sku_reference_no = models.CharField(null=True, blank=True, max_length=500)
  other_logistics_provider_setting = models.CharField(null=True, blank=True, max_length=500)
  other_logistics_provider_fee = models.CharField(null=True, blank=True, max_length=500)
  order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
  profile = models.ForeignKey(Profile, models.DO_NOTHING, blank=True, null=True)
  # category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
  category = models.IntegerField(blank=True, null=True)
  stock_sum = models.IntegerField(blank=True, null=True)
  live = models.BooleanField(default=False)
  suspended = models.BooleanField(default=False)
  unlisted = models.BooleanField(default=False)
  unpublished = models.BooleanField(default=False)

  panels = [
    FieldPanel('product_code'),
    FieldPanel('product_name'),
    FieldPanel('product_description'),
    FieldPanel('product_weight'),
    FieldPanel('product_condition'),
    FieldPanel('ship_out_in'),
    FieldPanel('parent_sku_reference_no'),
    FieldPanel('other_logistics_provider_setting'),
    FieldPanel('other_logistics_provider_fee'),
    InlinePanel('variations', label='Variations'),
    FieldPanel('live'),
    FieldPanel('suspended'),
    FieldPanel('unlisted'),
  ]

  def save_model(self, request, obj, form, change):
    obj.user_id = request.user.id
    super().save_model(request, obj, form, change)

  def save(self, *args, **kwargs):
    if(self.product_name):
      Errors.objects.filter(product_id=self.id).filter(name='Product name is required').delete()
      if(len(self.product_name)>=16):
        Errors.objects.filter(product_id=self.id).filter(name='Product name should have at least 16 characters').delete()
    if(self.product_code):
      Errors.objects.filter(product_id=self.id).filter(name='Product code is required').delete()
      if(len(self.product_code)<=100):
        Errors.objects.filter(product_id=self.id).filter(name='Product code exceeds maximum lenght of 100').delete()
    if(self.product_description):
      Errors.objects.filter(product_id=self.id).filter(name='Product description is required').delete()
      if(len(self.product_description)>=100):
        Errors.objects.filter(product_id=self.id).filter(name='Product description should have at least 100 characters').delete()
    if(len(Errors.objects.filter(product_id=self.id)) == 0):
      Product.objects.filter(id=self.id).update(unpublished=False)
    super(Product, self).save(*args, **kwargs)
    return HttpResponseRedirect("/products/#all")



  def __unicode__(self):
    return self.product_name


class Variations(Orderable, models.Model):  
  name = models.CharField(null=True, blank=True, max_length=500)
  sku = models.CharField(null=True, blank=True, max_length=500)
  price = models.CharField(null=True, blank=True, max_length=500)
  stock = models.IntegerField(null=True, blank=True)
  image_url = models.CharField(null=True, blank=True, max_length=2000, help_text='Optional: If your image is already hosted')
  image_upload = models.ForeignKey(
    'wagtailimages.Image',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+',
    help_text='Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.'
  )
  image_url_from_sku = models.CharField(null=True, blank=True, max_length=2000)
  product = ParentalKey('Product', related_name='variations', null=True, blank=True)

  panels = [
    FieldPanel('name'),
    FieldPanel('sku'),
    FieldPanel('price'),
    FieldPanel('stock'),
    # FieldPanel('image_url'),
    ImageChooserPanel('image_upload'),
  ]

  def save(self, *args, **kwargs):
    if(self.image_upload):
      Errors.objects.filter(product_id=self.product_id).filter(name='Product image is required').delete()
    if(len(Errors.objects.filter(product_id=self.product_id)) == 0):
      Product.objects.filter(id=self.product_id).update(unpublished=False)
    super(Variations, self).save(*args, **kwargs)
    return redirect('/products/#all')


class Errors(models.Model):  
  name = models.CharField(null=True, blank=True, max_length=500)
  product = ParentalKey('Product', related_name='errors', null=True, blank=True)


class ProductPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)

  def get_context(self, request):
    context = super().get_context(request)
    return context


class ProductsPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)
  
  def get_context(self, request):
    context = super().get_context(request)
    allProducts = Product.objects.filter(profile_id=request.user.id, unpublished=False)
    liveProducts = Product.objects.filter(profile_id=request.user.id, live=True)
    soldOutProducts = Product.objects.filter(profile_id=request.user.id, stock_sum=0)
    suspendedProducts = Product.objects.filter(profile_id=request.user.id, suspended=True)
    unlistedProducts = Product.objects.filter(profile_id=request.user.id, unlisted=True)
    unpublishedProducts = Product.objects.filter(profile_id=request.user.id, unpublished=True)
    subPages = self.get_children().live()
    context['allProducts'] = allProducts
    context['liveProducts'] = liveProducts
    context['soldOutProducts'] = soldOutProducts
    context['suspendedProducts'] = suspendedProducts
    context['unlistedProducts'] = unlistedProducts
    context['unpublishedProducts'] = unpublishedProducts
    context['nUnpublished'] = len(unpublishedProducts)
    context['subPages'] = subPages
    return context


class ProductImportPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)


class ProductsImportPage(BasePage):
  body = StreamField(GeneralStreamBlock, blank=True)
