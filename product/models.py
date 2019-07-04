from django.db import models
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock


class ProductPage(BasePage):
    body = StreamField(GeneralStreamBlock, blank=True)
