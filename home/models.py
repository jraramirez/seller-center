from django.db import models
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock
import json


class HomePage(BasePage):
    body = StreamField(GeneralStreamBlock, blank=True)

    def get_context(self, request):
        # with open('seller_center/static/documents/categories.json', 'r') as f:
        #   categoriesJSON = json.load(f)
        #   for i in categoriesJSON['data']['list']:
        #     c = Category(
        #       unique_id = i['id'] + 1891,
        #       parent_id = i['parent_id'] + 1891,
        #       name = i['name'],
        #     )
        #     c.save()
        context = super().get_context(request)
        subPages = self.get_children().live()
        context['subPages'] = subPages
        return context