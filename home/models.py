from django.db import models
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock


class HomePage(BasePage):
    body = StreamField(GeneralStreamBlock, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        subPages = self.get_children().live()
        context['subPages'] = subPages
        return context