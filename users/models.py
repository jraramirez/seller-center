from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
  verified = models.BooleanField(default=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def save(self, *args, **kwargs):
    self.id = self.user_id
    super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)