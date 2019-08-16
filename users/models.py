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


class Address(Orderable, models.Model):  
  name = models.TextField(null=True, blank=True)
  profile = ParentalKey('Profile', related_name='address', null=True, blank=True)
