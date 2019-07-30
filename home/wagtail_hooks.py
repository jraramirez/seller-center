from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from product.models import Product
from product.models import Order
from django.shortcuts import render, redirect

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

@hooks.register('register_admin_menu_item')
def register_home_menu_item():
  return MenuItem('Home', '/', classnames='icon icon-home', order=260)

@hooks.register('register_admin_menu_item')
def register_import_menu_item():
  return MenuItem('Add Products', '/products/add-new-products/', classnames='icon icon-plus', order=270)

@hooks.register('register_admin_menu_item')
def register_image_import_menu_item():
  return MenuItem('Add Images', '/admin/images/multiple/add/', classnames='icon icon-image', order=280)

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
