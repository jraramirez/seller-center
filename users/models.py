from django.db import models
from django.contrib.auth.models import User
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

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
  def save(self, *args, **kwargs):
    self.id = self.user_id
    super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)

class AddressContactDetails(models.Model):  
  contact_person_name=models.TextField(null=True, blank=True)
  contact_person_phone=models.TextField(null=True, blank=True)
  contact_person_email=models.TextField(null=True, blank=True)

class Address(Orderable, models.Model):  
  name = models.TextField(null=True, blank=True)
  index = models.IntegerField(null=True, blank=True)
  profile = ParentalKey('Profile', related_name='address', null=True, blank=True)
  contact_details=models.ForeignKey(AddressContactDetails, models.DO_NOTHING, blank=True, null=True)
  street_bldg=models.TextField(null=True, blank=True)
  country=models.TextField(null=True, blank=True)
  region_state=models.TextField(null=True, blank=True)
  city=models.TextField(null=True, blank=True)
  brgy=models.TextField(null=True, blank=True)
  postal_code=models.IntegerField(null=True, blank=True)

class BusinessDetails(models.Model):  
  company_name=models.TextField(null=True, blank=True)
  business_address=models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
  business_tin=models.TextField(null=True, blank=True)
  business_registration_number=models.TextField(null=True, blank=True)

class Documents(models.Model):  
  profile=ParentalKey('Profile', related_name='document', null=True, blank=True)
  document_type=models.TextField(null=True, blank=True)
  document_url=models.TextField(null=True, blank=True)