from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from product.models import Product
from product.models import Order


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
