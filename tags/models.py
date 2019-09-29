from django.db import models

# Create your models here.

from product.models import Product, Category


class Tag(models.Model):
  name = models.CharField(null=True, blank=True, max_length=500)
  products = models.ManyToManyField(Product)
  categories = models.ManyToManyField(Category)

