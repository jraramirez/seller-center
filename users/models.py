from django.db import models
from django.contrib.auth.models import User
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class AddressContactDetails(models.Model):  
  contact_person_name=models.TextField(null=True, blank=True)
  contact_person_phone=models.CharField(null=True, blank=True, max_length=500)
  contact_person_email=models.EmailField(null=True, blank=True)

class Address(Orderable, models.Model):  
  name = models.TextField(null=True, blank=True)
  profile = ParentalKey('Profile', related_name='address', null=True, blank=True)
  contact_details=models.OneToOneField(AddressContactDetails, on_delete=models.CASCADE, null=True)
  street_bldg=models.TextField(null=True, blank=True)
  country=models.TextField(null=True, blank=True)
  region_state=models.TextField(null=True, blank=True)
  city=models.TextField(null=True, blank=True)
  brgy=models.TextField(null=True, blank=True)
  postal_code=models.IntegerField(null=True, blank=True)

class BusinessDetails(models.Model):  
  company_name=models.TextField(null=True, blank=True)
  business_address=models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
  business_tin=models.TextField(null=True, blank=True)
  business_registration_number=models.TextField(null=True, blank=True)

class ShopDetails(models.Model):  
  shop_name=models.TextField(null=True, blank=True)
  holiday_mode=models.BooleanField(default=False)
  start_date=models.DateField(default=datetime.now, blank=True, null=True)
  start_time=models.DateField(default=datetime.now, blank=True, null=True)
  end_date=models.TimeField(default=datetime.now, blank=True, null=True)
  end_time=models.TimeField(default=datetime.now, blank=True, null=True)

class SellerDetails(models.Model):  
  seller_id=models.CharField(null=True, blank=True, max_length=500, unique=True)
  seller_status=models.CharField(null=True, blank=True, max_length=500)
  name_on_id=models.TextField(null=True, blank=True)
  id_type=models.TextField(null=True, blank=True)
  upload_id_front_url=models.TextField(null=True, blank=True)
  upload_id_back_url=models.TextField(null=True, blank=True)
  email=models.EmailField(null=True, blank=True)
  phone=models.TextField(null=True, blank=True)
  has_agreed_to_terms=models.BooleanField(default=False)
  shop_details=models.OneToOneField(ShopDetails, on_delete=models.CASCADE, null=True)

class Profile(ClusterableModel):
  birthday = models.DateField(default=datetime.now)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  dti = models.ForeignKey(
    'wagtaildocs.Document',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+'
  )
  sec = models.ForeignKey(
    'wagtaildocs.Document',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+'
  )
  permit = models.ForeignKey(
    'wagtaildocs.Document',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+'
  )
  seller_details=models.OneToOneField(SellerDetails, on_delete=models.CASCADE, null=True)
  business_details=models.ForeignKey(BusinessDetails, models.DO_NOTHING, blank=True, null=True)
  pickup_address=models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True, related_name='pickup_address')
  return_address=models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True, related_name='return_address')
  def save(self, *args, **kwargs):
    self.id = self.user_id
    super(Profile, self).save(*args, **kwargs)

class Documents(models.Model):  
  profile=ParentalKey('Profile', related_name='document', null=True, blank=True)
  document_type=models.TextField(null=True, blank=True)
  document_url=models.TextField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)