from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from product.models import Product
from product.models import Order
from wagtail.core import hooks
from django.utils.html import format_html
from django.templatetags.static import static
from django.shortcuts import render, redirect
from wagtail.admin.menu import MenuItem

@hooks.register('register_admin_menu_item')
def register_home_menu_item():
  return MenuItem('Dashboard', '/', classnames=' ', order=260)

@hooks.register('register_admin_menu_item')
def register_products_menu_item():
  return MenuItem('My Products', '/products/', classnames=' ', order=280)

@hooks.register('register_admin_menu_item')
def register_images_menu_item():
  return MenuItem('My Images', '/admin/images/', classnames=' ', order=300)

@hooks.register('register_admin_menu_item')
def register_logout_menu_item():
  return MenuItem('Log Out', '/admin/logout/', classnames=' ', order=310)

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/seller_center_admin.css'))

# @hooks.register('construct_main_menu')
# def hide_images_menu_item(request, menu_items):
#   menu_items[:] = [item for item in menu_items if item.name != 'products']

@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
  menu_items[:] = [item for item in menu_items if item.name != 'snippets']

# @hooks.register('construct_main_menu')
# def hide_documents_menu_item(request, menu_items):
#   menu_items[:] = [item for item in menu_items if item.name != 'documents']

@hooks.register('construct_main_menu')
def hide_forms_menu_item(request, menu_items):
  menu_items[:] = [item for item in menu_items if item.name != 'forms']

@hooks.register('construct_main_menu')
def hide_images_menu_item(request, menu_items):
  menu_items[:] = [item for item in menu_items if item.name != 'images']

class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = 'Products'
    menu_icon = ' '
    menu_order = 270
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('product_name',)
    search_fields = ('product_name',)


class SalesAdmin(ModelAdmin):
    model = Order
    menu_label = 'My Orders'
    menu_icon = ' '
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('status', 'countdown', 'shipping_channel')
    search_fields = ('status',)


modeladmin_register(ProductAdmin)
modeladmin_register(SalesAdmin)
