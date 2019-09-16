from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.contrib import messages
from wagtail.images.models import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
import numpy as np
import os
import requests
import json
from datetime import datetime

from product.models import ProductsImportPage, Product, Category, Variations, Errors, ProductStatus, Sale

from seller_center.settings.dev import MEDIA_URL
from seller_center.settings.base import CSV_COLUMNS


import VariationsFunctions as vf

media_url = MEDIA_URL 


class UploadFileForm(forms.Form):
  file = forms.FileField(label="Choose a file")


def product_import(request, selected_category):
  '''
  View for adding a singe product
  :param request:
  :return:
  '''
  showVariations = ""
  showWithoutVariation = "active show"

  # View when selecting a category
  if(selected_category == '0'):
    categories = {}
    with open('seller_center/static/documents/categories-full.json', 'r') as f:
      categories = json.load(f)
    return render(request, 'product/product_import_page.html', {
      'categories': categories,
      'selected_category': selected_category
    })

  # View when user decided to change the category. The current product data are stored in sessions
  elif(request.method == "POST" and request.POST.get('action') == 'change'):
    categories = {}
    with open('seller_center/static/documents/categories-full.json', 'r') as f:
      categories = json.load(f)
    selected_category = '0'
    product = {}
    variations = [{}]*7
    request.session['product-code'] = request.POST.get('product-code')
    request.session['product-name'] = request.POST.get('product-name')
    request.session['product-description'] = request.POST.get('product-description')
    request.session['product-brand'] = request.POST.get('product-brand')

    #Shipping Info
    request.session['product-length'] = request.POST.get('product-length')
    request.session['product-width'] = request.POST.get('product-width')
    request.session['product-height'] = request.POST.get('product-height')
    request.session['product-weight'] = request.POST.get('product-weight')

    request.session['product-price'] = request.POST.get('product-price')
    request.session['product-stock'] = request.POST.get('product-stock')
    request.session['product-sale-price'] = request.POST.get('product-sale-price')
    request.session['product-sale-date-start'] = request.POST.get('product-sale-date-start')
    request.session['product-sale-time-start'] = request.POST.get('product-sale-time-start')
    request.session['product-sale-date-end'] = request.POST.get('product-sale-date-end')
    request.session['product-sale-time-end'] = request.POST.get('product-sale-time-end')

    request.session['product-condition'] = request.POST.get('product-condition')
    request.session['product-parent-sku'] = request.POST.get('product-parent-sku')
    for i in range(0,8):
      request.session['product-variation-'+str(i)+'-sku'] = request.POST.get('product-variation-'+str(i)+'-sku')
      request.session['product-variation-'+str(i)+'-stock'] =  request.POST.get('product-variation-'+str(i)+'-stock')
      request.session['product-variation-'+str(i)+'-price'] = request.POST.get('product-variation-'+str(i)+'-price')
      request.session['product-variation-'+str(i)+'-name'] = request.POST.get('product-variation-'+str(i)+'-name')
      request.session['product-variation-'+str(i)+'-sale-price'] = request.POST.get('product-variation-'+str(i)+'-sale-price')
      request.session['product-variation-'+str(i)+'-sale-date-start'] = request.POST.get('product-variation-'+str(i)+'-sale-date-start')
      request.session['product-variation-'+str(i)+'-sale-time-start'] = request.POST.get('product-variation-'+str(i)+'-sale-time-start')
      request.session['product-variation-'+str(i)+'-sale-date-end'] = request.POST.get('product-variation-'+str(i)+'-sale-date-end')
      request.session['product-variation-'+str(i)+'-sale-time-end'] = request.POST.get('product-variation-'+str(i)+'-sale-time-end')
      if(request.FILES):
        request.session['product-variation-'+str(i)+'-image'] = request.FILES['product-variation-'+str(i)+'-image']
    return render(request, 'product/product_import_page.html', {
      'categories': categories,
      'selected_category': selected_category
    })

  # View when the product data is submitted. Form is validated.
  elif(request.method == "POST" and request.POST.get('action') == 'save'):
    if(selected_category == '0'):
      selected_category = request.POST.get('product-category-id')
    product = {}
    variations = [{}]*7
    product['product_code'] = request.POST.get('product-code')
    product['category'] = Category.objects.filter(unique_id=selected_category)[0].name
    product['product_name'] = request.POST.get('product-name')
    product['product_description'] = request.POST.get('product-description')
    product['product_brand'] = request.POST.get('product-brand')

    #Shipping Info
    product['product_length'] = request.POST.get('product-length')
    product['product_width'] = request.POST.get('product-width')
    product['product_height'] = request.POST.get('product-height')
    product['product_weight'] = request.POST.get('product-weight')

    product['product_price'] = request.POST.get('product-price')
    product['stock_sum'] = request.POST.get('product-stock')
    product['product_sale_price'] = request.POST.get('product-sale-price')
    product['product_sale_date_start'] = request.POST.get('product-sale-date-start')
    product['product_sale_time_start'] = request.POST.get('product-sale-time-start')
    product['product_sale_date_end'] = request.POST.get('product-sale-date-end')
    product['product_sale_time_end'] = request.POST.get('product-sale-time-end')

    # product['product_condition'] = request.POST.get('product-condition')
    product['parent_sku_reference_no'] = request.POST.get('product-parent-sku')
    errors = []
    if(not product['product_code']):
      errors.append('Product Code is required.')
    if(not product['category']):
      errors.append('Product Category is required.')
    if(not product['product_name']):
      errors.append('Product Name is required.')
    if(not product['product_description']):
      errors.append('Product Description is required.')
    if(request.POST.get('product-variation-0-sku') == '' and not product['product_price']):
      errors.append('Product Price is required.')
    else:
      if(product['product_sale_price']):
        if(not product['product_sale_date_start']):
          errors.append('Product Sale Start Date is required.')
        if(not product['product_sale_time_start']):
          errors.append('Product Sale Start Time is required.')
        if(not product['product_sale_date_end']):
          errors.append('Product Sale End Date is required.')
        if(not product['product_sale_time_end']):
          errors.append('Product Sale End Time is required.')      
    if(request.POST.get('product-variation-0-sku') == '' and not product['stock_sum']):
      errors.append('Product Stock is required.')
    for i in range(0,7):
      if(request.POST.get('product-variation-'+str(i)+'-sku')):
        if(not request.POST.get('product-variation-'+str(i)+'-name')):
          errors.append('Variation ' + str(i+1) +': name is required.')
        if(not request.POST.get('product-variation-'+str(i)+'-stock')):
          errors.append('Variation ' + str(i+1) +': stock is required.')
        if(not request.POST.get('product-variation-'+str(i)+'-price')):
          errors.append('Variation ' + str(i+1) +': price is required.')
        if(request.POST.get('product-variation-'+str(i)+'-sale-price')):
          if(not request.POST.get('product-variation-'+str(i)+'-sale-date-start')):
            errors.append('Variation ' + str(i+1) + ' Sale Start Date is required.')
          if(not request.POST.get('product-variation-'+str(i)+'-sale-date-end')):
            errors.append('Variation ' + str(i+1) + ' Sale End Date is required.')
          if(not request.POST.get('product-variation-'+str(i)+'-sale-time-start')):
            errors.append('Variation ' + str(i+1) + ' Sale Start Time is required.')
          if(not request.POST.get('product-variation-'+str(i)+'-sale-time-end')):
            errors.append('Variation ' + str(i+1) + ' Sale End Time is required.')
    if(not errors):
      t = Product(
        product_code = request.POST.get('product-code'),
        profile_id = request.user.id,
        category = Category.objects.filter(unique_id=selected_category)[0],
        product_name = request.POST.get('product-name'),
        product_description = request.POST.get('product-description'),
        product_brand = request.POST.get('product-brand'),
        # this may be empty strings so we replace it with None if empty string
        product_price = request.POST.get('product-price') if request.POST.get('product-price') else None, #this is evaluates as tertiary operator
        # product_sale_price = request.POST.get('product-sale-price') if request.POST.get('product-sale-price') else None,
        # product_sale_date_start = request.POST.get('product-sale-date-start') if request.POST.get('product-sale-date-start') else None,
        # product_sale_date_end = request.POST.get('product-sale-date-end') if request.POST.get('product-sale-date-end') else None,
        # product_sale_time_start = request.POST.get('product-sale-time-start') if request.POST.get('product-sale-time-start') else None,
        # product_sale_time_end = request.POST.get('product-sale-time-end') if request.POST.get('product-sale-time-end') else None,

        stock_sum = request.POST.get('product-stock') if request.POST.get('product-stock') else None,
        product_length = request.POST.get('product-length') if request.POST.get('product-length') else None,
        product_width = request.POST.get('product-width') if request.POST.get('product-width') else None,
        product_height = request.POST.get('product-height') if request.POST.get('product-height') else None,
        product_weight = request.POST.get('product-weight') if request.POST.get('product-weight') else None,

        # product_condition = request.POST.get('product-condition'),
        parent_sku_reference_no = request.POST.get('product-parent-sku'),
      )
      t.save()

      if request.POST.get('product-price'):
        s=Sale(
            product_sale_price=product['product_sale_price'] if product['product_sale_price'] != '' else 0,
            product_sale_date_start=product['product_sale_date_start'] if product['product_sale_date_start'] != '' else None,
            product_sale_date_end=product['product_sale_date_end'] if product['product_sale_date_end'] != '' else None,
            product_sale_time_start=product['product_sale_time_start'] if product['product_sale_time_start'] != '' else None,
            product_sale_time_end=product['product_sale_time_end'] if product['product_sale_time_end'] != '' else None,
            product_id=t.id
          )
        s.save()
      else:
        stock_sum = 0
        for i in range(0,8):
          if(request.POST.get('product-variation-'+str(i)+'-sku')):
            variationStock = 0
            if(request.POST.get('product-variation-'+str(i)+'-stock')):
              variationStock = int(request.POST.get('product-variation-'+str(i)+'-stock'))
            stock_sum = stock_sum + variationStock

            v = Variations(
              product_id = t.id,
              image_url = None,
              price =request.POST.get('product-variation-'+str(i)+'-price'),
              sale_price =request.POST.get('product-variation-'+str(i)+'-sale-price'),
              sale_date_start =request.POST.get('product-variation-'+str(i)+'-sale-date-start'),
              sale_date_end =request.POST.get('product-variation-'+str(i)+'-sale-date-end'),
              sale_time_start =request.POST.get('product-variation-'+str(i)+'-sale-time-start'),
              sale_time_end =request.POST.get('product-variation-'+str(i)+'-sale-time-end'),
              sku = request.POST.get('product-variation-'+str(i)+'-sku'),
              stock = variationStock,
              name = request.POST.get('product-variation-'+str(i)+'-name'),
              image_url_from_sku = None
            )
            v.save()
            if(request.FILES):
              image = request.FILES['product-variation-'+str(i)+'-image']
              v.image_upload.save(str(request.user.id) + '/' + image.name, image)
              Variations.objects.filter(id=v.id).update(
                image_url_from_upload = media_url + 'original_images/' + str(request.user.id) + '/'  + str(image.name)
              )
        Product.objects.filter(id=t.id).update(stock_sum=stock_sum)
      messages.success(request, 'Product added successfully.')
      return HttpResponseRedirect("/products/#all")
    else:
      product['category'] = Category.objects.filter(unique_id=selected_category)[0].name
      categoryParentId = Category.objects.filter(unique_id=selected_category)[0].parent_id
      product['parentCategory'] = Category.objects.filter(unique_id=categoryParentId)[0].name
      categoryParentParentId = Category.objects.filter(unique_id=categoryParentId)[0].parent_id
      product['parentParentCategory'] = Category.objects.filter(unique_id=categoryParentParentId)[0].name
      showVariations = ""
      showWithoutVariation = "active show"
      for i in range(0,7):
        if(request.POST.get('product-variation-'+str(i)+'-sku')):
          variationStock = None
          if(request.POST.get('product-variation-'+str(i)+'-stock')):
            variationStock = int(request.POST.get('product-variation-'+str(i)+'-stock'))
          tmp ={
            'variation_sku': request.POST.get('product-variation-'+str(i)+'-sku'),
            'variation_price': request.POST.get('product-variation-'+str(i)+'-price'),
            'variation_sale_price': request.POST.get('product-variation-'+str(i)+'-sale-price'),
            'variation_sale_date_start': request.POST.get('product-variation-'+str(i)+'-sale-date-start'),
            'variation_sale_date_end': request.POST.get('product-variation-'+str(i)+'-sale-date-end'),
            'variation_sale_time_start': request.POST.get('product-variation-'+str(i)+'-sale-time-start'),
            'variation_sale_time_end': request.POST.get('product-variation-'+str(i)+'-sale-time-end'),
            'variation_stock': variationStock,
            'variation_name': request.POST.get('product-variation-'+str(i)+'-name')
          }
          variations[i] = tmp
          showVariations = "active show"
          showWithoutVariation = ""
      return render(request, 'product/product_import_page.html', {
        'product': product,
        'errors': errors,
        'selected_category': selected_category,
        'variations': variations,
        'showVariations': showVariations,
        'showWithoutVariation': showWithoutVariation,
      })

  # View after a category is selected. The product form is prepared. If session data exist, they are inputted to the form.
  else:    
    product = {}
    variations = [{}]*7
    if('product-code' in request.session.keys()):
      product['product_code'] = request.session['product-code']
      del request.session['product-code']
    if('product-name' in request.session.keys()):
      product['product_name'] = request.session['product-name']
      del request.session['product-name']
    if('product-description' in request.session.keys()):
      product['product_description'] = request.session['product-description']
      del request.session['product-description']
    if('product-brand' in request.session.keys()):
      product['product_brand'] = request.session['product-brand']
      del request.session['product-brand']

      #Shipping Info
    if('product-length' in request.session.keys()):
      product['product_length'] = request.session['product-length']
      del request.session['product-length']
    if('product-width' in request.session.keys()):
      product['product_width'] = request.session['product-width']
      del request.session['product-width']
    if('product-height' in request.session.keys()):
      product['product_height'] = request.session['product-height']
      del request.session['product-height']
    if('product-weight' in request.session.keys()):
      product['product_weight'] = request.session['product-weight']
      del request.session['product-weight']
    if('product-price' in request.session.keys()):
      product['product_price'] = request.session['product-price']
      del request.session['product-price']
    if('product-sale-price' in request.session.keys()):
      product['product_sale_price'] = request.session['product-sale-price']
      del request.session['product-sale-price']
    if('product-sale-date-start' in request.session.keys()):
      product['product_sale_date_start'] = request.session['product-sale-date-start']
      del request.session['product-sale-date-start']
    if('product-sale-date-end' in request.session.keys()):
      product['product_sale_date_end'] = request.session['product-sale-date-end']
      del request.session['product-sale-date-end']
    if('product-sale-time-start' in request.session.keys()):
      product['product_sale_time_start'] = request.session['product-sale-time-start']
      del request.session['product-sale-time-start']
    if('product-sale-time-end' in request.session.keys()):
      product['product_sale_time_end'] = request.session['product-sale-time-end']
      del request.session['product-sale-time-end']
    # if('product-condition' in request.session.keys()):
    #   product['product_condition'] = request.session['product-condition']
      del request.session['product-condition']
    if('product-parent-sku' in request.session.keys()):
      product['parent_sku_reference_no'] = request.session['product-parent-sku']
      del request.session['product-parent-sku']

    for i in range(0,7):
      variation_sku = variation_price = variation_stock = variation_name = variation_url = ''
      variation_sale_price = variation_sale_date_start = variation_sale_date_end = variation_sale_time_start = variation_sale_time_end = ''
      if('product-variation-'+str(i)+'-sku' in request.session.keys()):
        variation_sku = request.session['product-variation-'+str(i)+'-sku']
      if('product-variation-'+str(i)+'-stock' in request.session.keys()):
        variation_stock = request.session['product-variation-'+str(i)+'-stock']
      if('product-variation-'+str(i)+'-price' in request.session.keys()):
        variation_price = request.session['product-variation-'+str(i)+'-price']
      if('product-variation-'+str(i)+'-sale-price' in request.session.keys()):
        variation_sale_price = request.session['product-variation-'+str(i)+'-sale-price']
      if('product-variation-'+str(i)+'-sale-date-start' in request.session.keys()):
        variation_sale_date_start = request.session['product-variation-'+str(i)+'-sale-date-start']
      if('product-variation-'+str(i)+'-sale-date-end' in request.session.keys()):
        variation_sale_date_end = request.session['product-variation-'+str(i)+'-sale-date-end']
      if('product-variation-'+str(i)+'-sale-time-start' in request.session.keys()):
        variation_sale_time_start = request.session['product-variation-'+str(i)+'-sale-time-start']
      if('product-variation-'+str(i)+'-sale-time-end' in request.session.keys()):
        variation_sale_time_end = request.session['product-variation-'+str(i)+'-sale-time-end']
      if('product-variation-'+str(i)+'-name' in request.session.keys()):
        variation_name = request.session['product-variation-'+str(i)+'-name']
      tmp = {
        'variation_sku': variation_sku,
        'variation_price': variation_price,
        'variation_stock': variation_stock,
        'variation_sale_price': variation_sale_price,
        'variation_sale_date_start': variation_sale_date_start,
        'variation_sale_date_end': variation_sale_date_end,
        'variation_sale_time_start': variation_sale_time_start,
        'variation_sale_time_end': variation_sale_time_end,
        'variation_url': variation_url
      }
      variations[i] = tmp
    product['category'] = Category.objects.filter(unique_id=selected_category)[0].name
    categoryParentId = Category.objects.filter(unique_id=selected_category)[0].parent_id
    product['parentCategory'] = Category.objects.filter(unique_id=categoryParentId)[0].name
    categoryParentParentId = Category.objects.filter(unique_id=categoryParentId)[0].parent_id
    product['parentParentCategory'] = Category.objects.filter(unique_id=categoryParentParentId)[0].name
    return render(request, 'product/product_import_page.html', {
      'product': product,
      'selected_category': selected_category,
      'variations': variations,
      'showVariations': showVariations,
      'showWithoutVariation': showWithoutVariation,
      'min_date' : datetime.now,
    })


def product_edit(request, category_id, product_id):
  '''
  View for editing a product
  :param request:
  :return:
  '''
  showVariations = ""
  showWithoutVariation = "active show"

  if (request.method == "POST"):
    product = {}
    variations = [{}] * 7

    product['product_code'] = request.POST.get('product-code')
    product['product-category-id'] = request.POST.get('product-category-id')
    if(category_id == '0'):
      category = Category.objects.filter(unique_id=int(product['product-category-id']))
    else:
      category = Category.objects.filter(unique_id=category_id)
    product['category'] = category[0].name
    categoryParentId = Category.objects.filter(unique_id=category_id)[0].parent_id
    product['parentCategory'] = Category.objects.filter(unique_id=categoryParentId)[0].name
    categoryParentParentId = Category.objects.filter(unique_id=categoryParentId)[0].parent_id
    product['parentParentCategory'] = Category.objects.filter(unique_id=categoryParentParentId)[0].name
    
    product['product_name'] = request.POST.get('product-name')
    product['product_description'] = request.POST.get('product-description')
    product['product_brand'] = request.POST.get('product-brand')

    product['product_length'] = request.POST.get('product-length')
    product['product_width'] = request.POST.get('product-width')
    product['product_height'] = request.POST.get('product-height')
    product['product_weight'] = request.POST.get('product-weight')

    product['product_price'] = request.POST.get('product-price')
    product['stock_sum'] = request.POST.get('product-stock')
    product['product_sale_price'] = request.POST.get('product-sale-price')
    product['product_sale_date_start'] = request.POST.get('product-sale-date-start')
    product['product_sale_time_start'] = request.POST.get('product-sale-time-start')
    product['product_sale_date_end'] = request.POST.get('product-sale-date-end')
    product['product_sale_time_end'] = request.POST.get('product-sale-time-end')
    # product['product_condition'] = request.POST.get('product-condition')
    product['parent_sku_reference_no'] = request.POST.get('product-parent-sku')

    if 'product-cover-img' in request.FILES:
      product['product_cover_img']=request.FILES['product-cover-img']
    if 'product-img-1' in request.FILES:
      product['product_img1']=request.FILES['product-img-1']
    if 'product-img-2' in request.FILES:
      product['product_img2']=request.FILES['product-img-2']
    if 'product-img-3' in request.FILES:
      product['product_img3']=request.FILES['product-img-3']
    if 'product-img-4' in request.FILES:
      product['product_img4']=request.FILES['product-img-4']
    if 'product-img-5' in request.FILES:
      product['product_img5']=request.FILES['product-img-5']
    errors = []

    if (not product['product_code']):
      errors.append('Product Code is required.')
    if (not product['product-category-id'] or request.POST.get('product-category-id') == "None"):
      errors.append('Product Category is required.')
    if (not product['product_name']):
      errors.append('Product Name is required.')
    if (not product['product_description']):
      errors.append('Product Description is required.')
    if(request.POST.get('product-variation-0-sku') == '' and not product['product_price']):
      errors.append('Product Price is required.')
    else:
      if product['product_sale_price'] and int(product['product_sale_price']) > 0:
        if(not product['product_sale_date_start']):
          errors.append('Product Sale Start Date is required.')
        if(not product['product_sale_time_start']):
          errors.append('Product Sale Start Time is required.')
        if(not product['product_sale_date_end']):
          errors.append('Product Sale End Date is required.')
        if(not product['product_sale_time_end']):
          errors.append('Product Sale End Time is required.')
    for i in range(0, 7):
      if (request.POST.get('product-variation-' + str(i) + '-sku')):
        if (not request.POST.get('product-variation-' + str(i) + '-name')):
          errors.append('Variation ' + str(i + 1) + ': name is required.')
        if (not request.POST.get('product-variation-' + str(i) + '-stock')):
          errors.append('Variation ' + str(i + 1) + ': stock is required.')
        if (not request.POST.get('product-variation-' + str(i) + '-price')):
          errors.append('Variation ' + str(i + 1) + ': price is required.')
        if(request.POST.get('product-variation-'+str(i)+'-sale-price')):
          if(not request.POST.get('product-variation-'+str(i)+'-sale-date-start')):
            errors.append('Variation ' + str(i+1) + ' Sale Start Date is required.')
          if(not request.POST.get('product-variation-'+str(i)+'-sale-date-end')):
            errors.append('Variation ' + str(i+1) + ' Sale End Date is required.')
          if(not request.POST.get('product-variation-'+str(i)+'-sale-time-start')):
            errors.append('Variation ' + str(i+1) + ' Sale Start Time is required.')
          if(not request.POST.get('product-variation-'+str(i)+'-sale-time-end')):
            errors.append('Variation ' + str(i+1) + ' Sale End Time is required.')
    if (not errors):
      p=Product.objects.filter(id=product_id)[0]
      category = Category.objects.filter(unique_id=int(product['product-category-id']))[0]
      t = Product(id=product_id,
        product_code=request.POST.get('product-code'),
        profile_id=request.user.id,
        category=category,
        product_name=request.POST.get('product-name'),
        product_description=request.POST.get('product-description'),
        product_brand=request.POST.get('product-brand') if request.POST.get('product-brand') else None,
        # this may be empty strings so we replace it with None if empty string
        product_price=request.POST.get('product-price') if request.POST.get('product-price') else None,
        product_status=ProductStatus.UNLISTED.value,
        # stock_sum=request.POST.get('product-stock') if request.POST.get('product-stock') else None,
        # product_sale_price = request.POST.get('product-sale-price') if request.POST.get('product-sale-price') else None,
        # product_sale_date_start = request.POST.get('product-sale-date-start') if request.POST.get('product-sale-date-start') else None,
        # product_sale_date_end = request.POST.get('product-sale-date-end') if request.POST.get('product-sale-date-start') else None,
        # product_sale_time_start = request.POST.get('product-sale-time-start') if request.POST.get('product-sale-date-start') else None,
        # product_sale_time_end = request.POST.get('product-sale-time-end') if request.POST.get('product-sale-date-start') else None,

        # this is evaluates as tertiary operator
        stock_sum=request.POST.get('product-stock') if request.POST.get('product-stock') else None,
        product_length=request.POST.get('product-length') if request.POST.get('product-length') else None,
        product_width=request.POST.get('product-width') if request.POST.get('product-width') else None,
        product_height=request.POST.get('product-height') if request.POST.get('product-height') else None,
        product_weight=request.POST.get('product-weight') if request.POST.get('product-weight') else None,

        # product_condition=request.POST.get('product-condition'),
        parent_sku_reference_no=request.POST.get('product-parent-sku'),

        cover_image_url=MEDIA_URL + 'original_images/' + str(request.user.id) + '/' + product['product_cover_img'].name if 'product_cover_img' in product else p.cover_image_url,
        image1_url=MEDIA_URL + 'original_images/' + str(request.user.id) + '/' + product['product_img1'].name if 'product_img1' in product else p.image1_url,
        image2_url=MEDIA_URL + 'original_images/' + str(request.user.id) + '/' + product['product_img2'].name if 'product_img2' in product else p.image2_url,
        image3_url=MEDIA_URL + 'original_images/' + str(request.user.id) + '/' + product['product_img3'].name if 'product_img3' in product else p.image3_url,
        image4_url=MEDIA_URL + 'original_images/' + str(request.user.id) + '/' + product['product_img4'].name if 'product_img4' in product else p.image4_url,
        image5_url=MEDIA_URL + 'original_images/' + str(request.user.id) + '/' + product['product_img5'].name if 'product_img5' in product else p.image5_url
      )
      t.save()

      if 'product_cover_img' in product:
        t.cover_image.save(str(request.user.id) + '/' + product['product_cover_img'].name, product['product_cover_img'])
      else:
        t.cover_image=p.cover_image
      if 'product_img1' in product:
        t.image1.save(str(request.user.id) + '/' + product['product_img1'].name, product['product_img1'])
      else:
        t.image1=p.image1
      if 'product_img2' in product:
        t.image2.save(str(request.user.id) + '/' + product['product_img2'].name, product['product_img2'])
      else:
        t.image2=p.image2
      if 'product_img3' in product:
        t.image3.save(str(request.user.id) + '/' + product['product_img3'].name, product['product_img3'])
      else:
        t.image3=p.image3
      if 'product_img4' in product:
        t.image4.save(str(request.user.id) + '/' + product['product_img4'].name, product['product_img4'])
      else:
        t.image4=p.image4
      if 'product_img5' in product:
        t.image5.save(str(request.user.id) + '/' + product['product_img5'].name, product['product_img5'])
      else:
        t.image5=p.image5

      # this means that product has no variation so we delete any existing variation
      if request.POST.get('product-price'):
        Variations.objects.filter(product_id=product_id).delete()
        s=Sale.objects.filter(product_id=product_id)[0]
        s.product_sale_price=product['product_sale_price'] if 'product_sale_price' in product else s.product_sale_price
        s.product_sale_date_start=product['product_sale_date_start'] if 'product_sale_date_start' in product else s.product_sale_date_start
        s.product_sale_date_end=product['product_sale_date_end'] if 'product_sale_date_end' in product else s.product_sale_date_end
        s.product_sale_time_start=product['product_sale_time_start'] if 'product_sale_time_start' in product else s.product_sale_time_start
        s.product_sale_time_end=product['product_sale_time_end'] if 'product_sale_time_end' in product else s.product_sale_time_end
        s.save()
      else:
        stock_sum = 0
        variations = Variations.objects.filter(product_id=product_id).order_by('-id')
        for i in range(0, 8):
          if (request.POST.get('product-variation-' + str(i) + '-sku')):
            variationStock = 0
            if (request.POST.get('product-variation-' + str(i) + '-stock')):
              variationStock = int(request.POST.get('product-variation-' + str(i) + '-stock'))
            stock_sum = stock_sum + variationStock

            if i < variations.count():
              v=variations[i]
            else:
              v = Variations()
              v.product_id = product_id

            v.image_url=None
            v.price=request.POST.get('product-variation-' + str(i) + '-price')
            v.sku=request.POST.get('product-variation-' + str(i) + '-sku')
            v.stock=variationStock
            v.name=request.POST.get('product-variation-' + str(i) + '-name')
            # v.sale_price=request.POST.get('product-variation-' + str(i) + '-sale-price')
            # v.sale_date_start=request.POST.get('product-variation-' + str(i) + '-sale-date-start')
            # v.sale_date_end=request.POST.get('product-variation-' + str(i) + '-sale-date-end')
            # v.sale_time_start=request.POST.get('product-variation-' + str(i) + '-sale-time-start')
            # v.sale_time_end=request.POST.get('product-variation-' + str(i) + '-sale-time-end')
            v.image_url_from_sku=None

            v.save()
            if 'product-variation-' + str(i) + '-image' in request.FILES:
              image = request.FILES['product-variation-' + str(i) + '-image']
              # Image.objects.create(
              #   file=image,
              #   title=image.name
              # )
              v.image_upload.save(str(request.user.id) + '/' + image.name, image)
              Variations.objects.filter(id=v.id).update(
                image_url_from_upload=media_url + 'original_images/' + str(request.user.id) + '/' + str(image.name)
              )
        Product.objects.filter(id=t.id).update(stock_sum=stock_sum)
      messages.success(request, 'Product edited successfully.')
      return HttpResponseRedirect("/products/#unlisted")
    else:
      showVariations = ""
      showWithoutVariation = "active show"
      for i in range(0, 7):
        if (request.POST.get('product-variation-' + str(i) + '-sku')):
          variationStock = None
          if (request.POST.get('product-variation-' + str(i) + '-stock')):
            variationStock = int(request.POST.get('product-variation-' + str(i) + '-stock'))
          tmp = {
            'variation_sku': request.POST.get('product-variation-' + str(i) + '-sku'),
            'variation_price': request.POST.get('product-variation-' + str(i) + '-price'),
            'variation_sale_price': request.POST.get('product-variation-'+str(i)+'-sale-price'),
            'variation_sale_date_start': request.POST.get('product-variation-'+str(i)+'-sale-date-start'),
            'variation_sale_date_end': request.POST.get('product-variation-'+str(i)+'-sale-date-end'),
            'variation_sale_time_start': request.POST.get('product-variation-'+str(i)+'-sale-time-start'),
            'variation_sale_time_end': request.POST.get('product-variation-'+str(i)+'-sale-time-end'),
            'variation_stock': variationStock,
            'variation_name': request.POST.get('product-variation-' + str(i) + '-name')
          }
          variations[i] = tmp
          showVariations = "active show"
          showWithoutVariation = ""
      return render(request, 'product/product_import_page.html', {
        'product': product,
        'errors': errors,
        'selected_category': request.POST.get('product-category-id'),
        'variations': variations,
        'showVariations': showVariations,
        'showWithoutVariation': showWithoutVariation,
      })
  elif(category_id == '0'):
    categories = {}
    with open('seller_center/static/documents/categories-full.json', 'r') as f:
      categories = json.load(f)
    return render(request, 'product/product_edit_page.html', {
      'product_id': product_id,
      'categories': categories,
      'selected_category': category_id
    })
  else:
    product = {}
    selectedProduct = Product.objects.filter(id=product_id)[0]
    product['product_code'] = selectedProduct.product_code
    product['stock_sum'] = selectedProduct.stock_sum
    category = selectedProduct.category
    if(category != category):
      product['category'] = "None"
    else:
      if(category_id != selectedProduct.category):
        product['product_category_id'] = category_id
        category = Category.objects.filter(unique_id=category_id)
        product['category'] = category[0].name
        categoryParentId = Category.objects.filter(unique_id=category_id)[0].parent_id
        product['parentCategory'] = Category.objects.filter(unique_id=categoryParentId)[0].name
        categoryParentParentId = Category.objects.filter(unique_id=categoryParentId)[0].parent_id
        product['parentParentCategory'] = Category.objects.filter(unique_id=categoryParentParentId)[0].name
      else:
        product['product_category_id'] = selectedProduct.category
        category = Category.objects.filter(unique_id=selectedProduct.category)
        product['category'] = category[0].name
        categoryParentId = Category.objects.filter(unique_id=selectedProduct.category)[0].parent_id
        product['parentCategory'] = Category.objects.filter(unique_id=categoryParentId)[0].name
        categoryParentParentId = Category.objects.filter(unique_id=categoryParentId)[0].parent_id
        product['parentParentCategory'] = Category.objects.filter(unique_id=categoryParentParentId)[0].name
      
    product['product_name'] = selectedProduct.product_name
    product['product_description'] = selectedProduct.product_description
    if selectedProduct.product_brand is not None:
      product['product_brand'] = selectedProduct.product_brand

    product['product_price'] = selectedProduct.product_price
    # product['product_sale_price'] = selectedProduct.product_sale_price
    # product['product_sale_date_start'] = selectedProduct.product_sale_date_start
    # product['product_sale_date_end'] = selectedProduct.product_sale_date_end
    # product['product_sale_time_start'] = selectedProduct.product_sale_time_start
    # product['product_sale_time_end'] = selectedProduct.product_sale_time_end
    product['stock_sum'] = selectedProduct.stock_sum

    product['product_length'] = selectedProduct.product_length if selectedProduct.product_length is not None else ''
    product['product_width'] = selectedProduct.product_width if selectedProduct.product_width is not None else ''
    product['product_height'] = selectedProduct.product_height if selectedProduct.product_height is not None else ''
    product['product_weight'] = selectedProduct.product_weight if selectedProduct.product_weight is not None else ''

    # product['product_condition'] = selectedProduct.product_condition
    product['parent_sku_reference_no'] = selectedProduct.parent_sku_reference_no

    product['cover_image_url']=selectedProduct.cover_image_url
    product['image1_url']=selectedProduct.image1_url
    product['image2_url']=selectedProduct.image2_url
    product['image3_url']=selectedProduct.image3_url
    product['image4_url']=selectedProduct.image4_url
    product['image5_url']=selectedProduct.image5_url

    s=Sale.objects.filter(product_id=product_id)[0]
    product['product_sale_price']=s.product_sale_price
    product['product_sale_date_start']=s.product_sale_date_start
    product['product_sale_date_end']=s.product_sale_date_end
    product['product_sale_time_start']=s.product_sale_time_start
    product['product_sale_time_end']=s.product_sale_time_end

    product['variations'] = Variations.objects.filter(product_id=product_id).order_by('-id')

    variations = [{}]*7
    for index, v in enumerate(product['variations']):
      tmp = {
        'variation_sku': v.sku,
        'variation_price': v.price,
        'variation_sale_price': v.sale_price,
        'variation_sale_date_start': v.sale_date_start,
        'variation_sale_date_end': v.sale_date_end,
        'variation_sale_time_start': v.sale_time_start,
        'variation_sale_time_end': v.sale_time_end,
        'variation_stock': v.stock,
        'variation_name': v.name,
        'variation_image_url_from_upload': v.image_url_from_upload if v.image_url_from_upload is not None else ''
      }

      variations[index] = tmp
      showVariations = "active show"
      showWithoutVariation = ""
    
    return render(request, 'product/product_edit_page.html', {
      'product_id': product_id,
      'selected_category': category_id,
      'product': product,
      'variations': variations,
      'showVariations': showVariations,
      'showWithoutVariation': showWithoutVariation,
    })


def products_import(request):
  '''
  Bulk upload via csv
  :param request:
  :return:
  '''
  if(request.method == "POST" and request.POST.get('upload')):
    autoPair = request.POST.get('auto-pair')
    form = UploadFileForm(request.POST, request.FILES)
    invalid = False
    invalidCategory = False
    missingRequiredFields = False
    invalidRows = []
    missingColumns = []
    if form.is_valid():
      inputFile = request.FILES['file']
      inputFileDF = pd.read_csv(inputFile, skip_blank_lines=True)
      inputFileDF = inputFileDF.head(500)

      # Check if there are missing columns
      for column in CSV_COLUMNS: 
        if(column not in inputFileDF.columns.values):
          missingColumns.append(column)
          invalid = True
      if(not invalid):
        # Obtain titles of images
        imageTitles = []
        for title in Image.objects.all().values_list('title', flat=True):
          imageTitles.append(os.path.splitext(title)[0])

        # Insert/Update each product from file to database
        with transaction.atomic():
          for index, row, in inputFileDF.iterrows():
            cat_id=str(row['category_id'])
            if not cat_id.isdigit():
              row['category_id']=None

            unpublished = False
            productID = None

            product = Product.objects.filter(profile_id=request.user.id).filter(product_code=row['product_code'])
            print("product row: %s " % row)
            if(product.count()):
              if row['product_code'] != row['product_code']:
                missingRequiredFields = True
                invalidRows.append(index + 2)

              elif row['category_id'] != row['category_id']:
                missingRequiredFields = True
                invalidRows.append(index + 2)
              else:

                found_category = Category.objects.filter(unique_id=row['category_id'])
                print("product found_category: %s " % found_category)
                if (len(found_category) == 0):
                  invalidCategory = True
                  invalidRows.append(index + 2)
                else:
                  product.update(
                    product_code = row['product_code'],
                    profile_id = request.user.id,
                    category = row['category_id'],
                    product_name = None,
                    product_description = row['product_description'] if row['product_description'] == row['product_description'] else None,
                    product_brand = row['product_brand'] if row['product_brand'] == row['product_brand'] else None,
                    product_weight = row['product_weight'] if row['product_weight'] == row['product_weight'] else None,
                    ship_out_in = row['ship_out_in'] if row['ship_out_in'] == row['ship_out_in'] else None,
                    parent_sku_reference_no = row['parent_sku_reference_no'] if row['parent_sku_reference_no'] == row['parent_sku_reference_no'] else None,
                    # other_logistics_provider_setting = row['other_logistics_provider_setting'] if row['other_logistics_provider_setting'] == row['other_logistics_provider_setting'] else None,
                    # other_logistics_provider_fee = row['other_logistics_provider_fee'] if row['other_logistics_provider_fee'] == row['other_logistics_provider_fee'] else None,
                    # live = False,
                    # suspended = False,
                    # unlisted = False,
                    # unpublished = unpublished
                  )
                  productID = product[0].id

                  s=Sale.objects.filter(product_id=productID)[0]
                  s.product_sale_price=product['product_sale_price'] if row['product_sale_price'] == row['product_sale_price'] else s.product_sale_price
                  s.product_sale_date_start=product['product_sale_date_start'] if row['product_sale_date_start'] == row['product_sale_date_start'] else s.product_sale_date_start
                  s.product_sale_date_end=product['product_sale_date_end'] if row['product_sale_date_end'] == row['product_sale_date_end'] else s.product_sale_date_end
                  s.product_sale_time_start=product['product_sale_time_start'] if row['product_sale_time_start'] == row['product_sale_time_start'] else s.product_sale_time_start
                  s.product_sale_time_end=product['product_sale_time_end'] if row['product_sale_time_end'] == row['product_sale_time_end'] else s.product_sale_time_end
                  s.save()

                  Errors.objects.filter(product_id=productID).delete()
            else:

              # check required fields is not NaN

              if row['product_code'] != row['product_code']:
                missingRequiredFields = True
                invalidRows.append(index + 2)

              elif row['category_id'] != row['category_id']:
                missingRequiredFields = True
                invalidRows.append(index + 2)
              else:

                found_category = Category.objects.filter(unique_id=row['category_id'])

                if (len(found_category) == 0):
                  invalidCategory = True
                  invalidRows.append(index + 2)
                else:
                  t = Product(
                    product_code = row['product_code'],
                    profile_id = request.user.id,
                    category = found_category[0],
                    product_name = None,
                    product_description = row['product_description'] if row['product_description'] == row['product_description'] else None,
                    product_brand = row['product_brand'] if row['product_brand'] == row['product_brand'] else None,
                    product_weight = row['product_weight'] if row['product_weight'] == row['product_weight'] else None,
                    ship_out_in = row['ship_out_in'] if row['ship_out_in'] == row['ship_out_in'] else None,
                    parent_sku_reference_no = row['parent_sku_reference_no'] if row['parent_sku_reference_no'] == row['parent_sku_reference_no'] else None,
                    # other_logistics_provider_setting = row['other_logistics_provider_setting'] if row['other_logistics_provider_setting'] == row['other_logistics_provider_setting'] else None,
                    # other_logistics_provider_fee = row['other_logistics_provider_fee'] if row['other_logistics_provider_fee'] == row['other_logistics_provider_fee'] else None,
                    # live = False,
                    # suspended = False,
                    # unlisted = False,
                    # unpublished = unpublished
                  )
                  t.save()
                  productID = t.id

                  s=Sale(
                      product_sale_price=row['product_sale_price'] if row['product_sale_price'] == row['product_sale_price'] else 0,
                      product_sale_date_start=row['product_sale_date_start'] if row['product_sale_date_start'] == row['product_sale_date_start'] else None,
                      product_sale_date_end=row['product_sale_date_end'] if row['product_sale_date_end'] == row['product_sale_date_end'] else None,
                      product_sale_time_start=row['product_sale_time_start'] if row['product_sale_time_start'] == row['product_sale_time_start'] else None,
                      product_sale_time_end=row['product_sale_time_end'] if row['product_sale_time_end'] == row['product_sale_time_end'] else None,
                      product_id=productID
                    )
                  s.save()

                  Errors.objects.filter(product_id = productID).delete()

            # Product code validation
            if(row['product_code'] != row['product_code']):
              Product.objects.filter(id=productID).update(product_code=None)
              e = Errors(
                product_id = productID,
                name = 'Product Code is required',
              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_code=row['product_code'])
              if(len(str(row['product_code']))>100):
                e = Errors(
                  product_id = productID,
                  name = 'Product Code exceeds maximum lenght of 100',
                )
                e.save()
                unpublished = True
                
            # Product category_id validation
            if(row['category_id'] != row['category_id']):
              Product.objects.filter(id=productID).update(category_id=None)
              e = Errors(
                product_id = productID,
                name = 'Product Category is required',
              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_code=row['product_code'])
              if(len(str(row['product_code']))>100):
                e = Errors(
                  product_id = productID,
                  name = 'Product Code exceeds maximum lenght of 100',
                )
                e.save()
                unpublished = True
            # Product name validation
            if(row['product_name'] != row['product_name']):
              Product.objects.filter(id=productID).update(product_name=None)
              e = Errors(
                product_id = productID,
                name = 'Product Name is required',
              )
              e.save()
              unpublished = True
            else:
              prod_name=row['product_name']
              formatted_prod_name=f'{prod_name}'
              Product.objects.filter(id=productID).update(product_name=formatted_prod_name)
              if(len(formatted_prod_name)<16):
                e = Errors(
                  product_id = productID,
                  name = 'Product Name should have at least 16 characters',
                )
                e.save()
                unpublished = True

            # Product description validation
            if(row['product_description'] == row['product_description']):
              prod_desc=row['product_description']
              formatted_prod_desc=f'{prod_desc}'
              Product.objects.filter(id=productID).update(product_description=formatted_prod_desc)
              if(len(formatted_prod_desc)<100):
                e = Errors(
                  product_id = productID,
                  name = 'Product Description should have at least 100 characters',
                )
                e.save()
                unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_description=None)
              e = Errors(
                product_id = productID,
                name = 'Product Description is required',
              )
              e.save()
              unpublished = True

            # Product price and stock validation
            if(vf.hasVariations(row)):
              Product.objects.filter(id=productID).update(product_price=None)
              Product.objects.filter(id=productID).update(stock_sum=None)
            else:
              if(row['product_price'] != row['product_price']):
                Product.objects.filter(id=productID).update(product_price=None)
                e = Errors(
                  product_id = productID,
                  name = 'Missing Product Price',

                )
                e.save()
                unpublished = True
              else:
                prod_price=str(row['product_price'])
                if not prod_price.isdigit():
                  prod_price=None
                Product.objects.filter(id=productID).update(product_price=prod_price)
              if(row['stock_sum'] != row['stock_sum']):
                Product.objects.filter(id=productID).update(stock_sum=None)
                e = Errors(
                  product_id = productID,
                  name = 'Missing Product Stock',

                )
                e.save()
                unpublished = True
              else:
                Product.objects.filter(id=productID).update(stock_sum=row['stock_sum'])

            # Product image validation
            imageInS3 = False
            if(autoPair):
              image_url_from_sku = None
              if(row['variation1_id'] == row['variation1_id']):
                if(row['image1'] != row['image1']):
                  if(str(row['variation1_id']) in imageTitles):
                    image_url_from_sku = media_url + str(Image.objects.all()[imageTitles.index(str(row['variation1_id']))].file)
                    imageInS3 = True
                  else:
                    unpublished = True
                    e = Errors(
                      product_id = productID,
                      name = 'Product Image is required',
                    )
                    e.save()
            else:
              if(row['image1'] != row['image1']):
                unpublished = True
                e = Errors(
                  product_id = productID,
                  name = 'Product Image is required',
                )
                e.save()
            # Insert/Update each product variation from file to database
            if(vf.hasVariations(row)):
              stock_sum = 0
              for i in range(0,7):
                if 'variation'+str(i+1)+'_id' in row:
                  variationID = row['variation'+str(i+1)+'_id']
                  variationStock = row['variation'+str(i+1)+'_stock']
                  variationPrice = row['variation'+str(i+1)+'_price']
                  variationName = row['variation'+str(i+1)+'_name']

                  # Product variation stock validation
                  if(variationStock != variationStock):
                    variationStock = 0
                  else:
                    stock_sum = stock_sum + int(variationStock)

                  # Product variation image1 validation
                  if(i == 0 and not imageInS3 and not autoPair):
                    image_url_from_sku = None
                  image_url = row['image1']
                  if(row['image1'] != row['image1']):
                    image_url = None
                  
                  # Product variation name validation
                  if(variationName != variationName):
                    variationName = None
                    unpublished = True
                    e = Errors(
                      product_id = productID,
                      name = 'Variation '+str(i+1)+' Name is required',
                    )
                    e.save()

                  # Product variation price validation
                  if(variationPrice != variationPrice):
                    variationPrice = None
                    unpublished = True
                    e = Errors(
                      product_id = productID,
                      name = 'Variation '+str(i+1)+' Price is required',
                    )
                    e.save()

                  variation = Variations.objects.filter(product_id=productID).filter(sku=row['variation'+str(i+1)+'_id'])
                  if(variation.count()):
                    variation.update(
                      product_id = productID,
                      image_url = image_url,
                      price = variationPrice,
                      sku = variationID,
                      stock = variationStock,
                      name = variationName,
                      image_url_from_sku = image_url_from_sku
                    )
                  else:
                    v = Variations(
                      product_id = productID,
                      image_url = image_url,
                      price = variationPrice,
                      sku = variationID,
                      stock = variationStock,
                      name = variationName,
                      image_url_from_sku = image_url_from_sku
                    )
                    v.save()
              if(not unpublished):
                Product.objects.filter(id=productID).update(product_status=ProductStatus.UNLISTED.value)
              Product.objects.filter(id=productID).update(stock_sum=stock_sum, product_status=ProductStatus.UNPUBLISHED.value)

    if (invalidCategory):
      errorMessage = 'Incorrect Category ID on Row/s: '
      for row in invalidRows:
        errorMessage = errorMessage + str(row) + ', '
      messages.error(request, errorMessage)
    elif (missingRequiredFields):
      errorMessage = 'Missing required Product Code / Category ID: '
      for row in invalidRows:
        errorMessage = errorMessage + str(row) + ', '
      messages.error(request, errorMessage)
      return HttpResponseRedirect("/products/add-new-products/")
    elif(invalid):
      errorMessage = 'Invalid csv template please download the correct one. Missing column(s): '
      for column in missingColumns:
        errorMessage = errorMessage + column + ', '
      messages.error(request, errorMessage)
      return HttpResponseRedirect("/products/add-new-products/")
    elif(Errors.objects.all().count()):
      messages.warning(request, 'Products added. Some products have data errors. Check out the unpublished tab to correct them.')
      return HttpResponseRedirect("/products/#unpublished")
    else:
      messages.success(request, 'Products added successfully.')
      return HttpResponseRedirect("/products/#all")
  else:
    form = UploadFileForm()

  self = ProductsImportPage.objects.get(slug='add-new-products')

  return render(request, 'product/products_import_page.html', {
    'self': self,
    'form': form,
  })


def product_delete(request, product_id):
  Product.objects.filter(id=product_id).delete()
  return HttpResponseRedirect("/products/#unpublished")


def product_unlist(request, product_id):
  Product.objects.filter(id=product_id).update(unlisted=True)
  return HttpResponseRedirect("/products/#all")


def product_suspend(request, product_id):
  Product.objects.filter(id=product_id).update(suspended=True)
  return HttpResponseRedirect("/products/#all")


def product_live(request, product_id):
  Product.objects.filter(id=product_id).update(live=True)
  return HttpResponseRedirect("/products/#all")


# function for downloading sample file as Excel file
def download_template(request):
  outFileName = 'Import Products Template'
  outFolderName = 'seller_center/static/documents/'
  fileType = '.csv'
  path = outFolderName + outFileName + fileType
  if os.path.exists(path):
    with open(path, "rb") as excel:
      data = excel.read()
    response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=' + outFileName + fileType
    return response

# function for downloading product categories as Excel file
def download_categories(request):
  outFileName = 'lyka-categories-v1'
  outFolderName = 'seller_center/static/documents/'
  fileType = '.csv'
  path = outFolderName + outFileName + fileType
  if os.path.exists(path):
    with open(path, "rb") as excel:
      data = excel.read()
    response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=' + outFileName + fileType
    return response

def delete_all_products(request):
  Product.objects.all().delete()
  Variations.objects.all().delete()
  return HttpResponseRedirect("/products/#all")

def uploadJSONCategoriesToDB():
  with open('ShopeeTempCategory.json', 'r') as f:
    categoriesJSON = json.load(f)
    for i in categoriesJSON['data']['list']:
      c = Category(
        unqiue_id = i['id'] + 1891,
        parent_id = i['parent_id'] + 1891,
        name = i['name'],
      )
      c.save()

def queryCategories():
    l1Categories = Category.objects.filter(parent_id=1891)
    categories = [{} for _ in range(len(l1Categories))]
    for i, c in zip(range(len(l1Categories)), l1Categories):
      categories[i]['name'] = c.name
      categories[i]['unique_id'] = c.unique_id
      categories[i]['level'] = 1
      categories[i]['top'] = str(-39*(i))+'px'
      l2Categories = Category.objects.filter(parent_id=c.unique_id)
      categories[i]['children'] = [{} for _ in range(len(l2Categories))]
      for j, c2 in zip(range(len(l2Categories)), l2Categories):
        categories[i]['children'][j]['name'] = c2.name
        categories[i]['children'][j]['unique_id'] = c2.unique_id
        categories[i]['children'][j]['level'] = c2.level
        categories[i]['children'][j]['top'] = str(-39*(j))+'px'
        l3Categories = Category.objects.filter(parent_id=c2.unique_id)
        categories[i]['children'][j]['children'] = [{} for _ in range(len(l3Categories))]
        for k, c3 in zip(range(len(l3Categories)), l3Categories):
          categories[i]['children'][j]['children'][k]['name'] = c3.name
          categories[i]['children'][j]['children'][k]['unique_id'] = c3.unique_id
          categories[i]['children'][j]['children'][k]['level'] = c3.level

def generateCategoriesList():
    categories = {}
    with open('seller_center/static/documents/categories-full.json', 'r') as f:
      categories = json.load(f)
  
    df = pd.DataFrame()
    primaryCategories = []
    secondaryCategories = []
    level3Categories = []
    categoryIDs = []
    for c1 in categories:
      for c2 in c1['children']:
        for c3 in c2['children']:
          primaryCategories.append(c1['name'])
          secondaryCategories.append(c2['name'])
          level3Categories.append(c3['name'])
          categoryIDs.append(c3['unique_id'])
    df['Primary Category'] = primaryCategories
    df['Secondary Category'] = secondaryCategories
    df['Level 3 Category'] = level3Categories
    df['Category ID'] = categoryIDs
    df.reset_index().to_csv('seller_center/static/documents/lyka-categories-v1.csv')
    
    return 