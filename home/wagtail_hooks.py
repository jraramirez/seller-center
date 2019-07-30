from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from product.models import Product
from product.models import Order
from wagtail.core import hooks
from django.utils.html import format_html
from django.templatetags.static import static


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/seller_center.css'))

@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
  menu_items[:] = [item for item in menu_items if item.name != 'snippets']

class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = 'Products'
    menu_icon = 'group'
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('product_name',)
    search_fields = ('product_name',)


class SalesAdmin(ModelAdmin):
    model = Order
    menu_label = 'Orders'
    menu_icon = 'group'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('status', 'countdown', 'shipping_channel')
    search_fields = ('status',)


modeladmin_register(ProductAdmin)
modeladmin_register(SalesAdmin)
