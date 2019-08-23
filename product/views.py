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

from product.models import ProductsImportPage
from product.models import Product
from product.models import Category
from product.models import Variations
from product.models import Errors

from seller_center.settings.dev import MEDIA_URL
from seller_center.settings.base import CSV_COLUMNS

media_url = MEDIA_URL 


class UploadFileForm(forms.Form):
  file = forms.FileField(label="Choose a file")

def product_import(request, selected_category):
  CONDITION_CHOICES = [
    ('N', 'New'),
    ('U', 'Used'),
  ]
  showVariations = ""
  showWithoutVariation = "active show"

  if(selected_category == '0'):
    categories = {}
    with open('seller_center/static/documents/categories-full.json', 'r') as f:
      categories = json.load(f)
    return render(request, 'product/product_import_page.html', {
      'categories': categories,
      'selected_category': selected_category
    })

  elif(request.method == "POST"):
    product = {}
    variations = [{}]*7
    product['product_code'] = request.POST.get('product-code')
    product['category'] = Category.objects.filter(unique_id=selected_category)[0].name
    product['product_name'] = request.POST.get('product-name')
    product['product_description'] = request.POST.get('product-description')

    #Shipping Info
    product['product_length'] = request.POST.get('product-length')
    product['product_width'] = request.POST.get('product-width')
    product['product_height'] = request.POST.get('product-height')
    product['product_weight'] = request.POST.get('product-weight')

    product['product_price'] = request.POST.get('product-price')
    product['product_stock'] = request.POST.get('product-stock')

    product['product_condition'] = request.POST.get('product-condition')
    product['parent_sku_reference_no'] = request.POST.get('product-parent-sku')
    errors = []
    if(not product['product_code']):
      errors.append('Product Code is required; ')
    if(not product['category']):
      errors.append('Product Category is required; ')
    if(not product['product_name']):
      errors.append('Product Name is required; ')
    if(not product['product_description']):
      errors.append('Product Description is required; ')
    if(request.POST.get('product-variation-0-sku') == '' and not product['product_price']):
      errors.append('Product Price is required; ')
    if(request.POST.get('product-variation-0-sku') == '' and not product['product_stock']):
      errors.append('Product Stock is required; ')
    for i in range(0,7):
      if(request.POST.get('product-variation-'+str(i)+'-sku')):
        if(not request.POST.get('product-variation-'+str(i)+'-name')):
          errors.append('Variation ' + str(i+1) +': name is required; ')
        if(not request.POST.get('product-variation-'+str(i)+'-stock')):
          errors.append('Variation ' + str(i+1) +': stock is required; ')
        if(not request.POST.get('product-variation-'+str(i)+'-price')):
          errors.append('Variation ' + str(i+1) +': price is required; ')
    if(not errors):
      t = Product(
        product_code = request.POST.get('product-code'),
        profile_id = request.user.id,
        category = selected_category,
        product_name = request.POST.get('product-name'),
        product_description = request.POST.get('product-description'),
        # this may be empty strings so we replace it with None if empty string
        product_price = request.POST.get('product-price') if request.POST.get('product-price') else None, #this is evaluates as tertiary operator
        stock_sum = request.POST.get('product-stock') if request.POST.get('product-stock') else None,
        product_length = request.POST.get('product-length') if request.POST.get('product-length') else None,
        product_width = request.POST.get('product-width') if request.POST.get('product-width') else None,
        product_height = request.POST.get('product-height') if request.POST.get('product-height') else None,
        product_weight = request.POST.get('product-weight') if request.POST.get('product-weight') else None,

        product_condition = request.POST.get('product-condition'),
        parent_sku_reference_no = request.POST.get('product-parent-sku'),
        live = False,
        suspended = False,
        unlisted = True,
        unpublished = False
      )
      t.save()
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
        'CONDITION_CHOICES': CONDITION_CHOICES
      })

  else:
    product = {}
    variations = [{}]*7
    product['category'] = Category.objects.filter(unique_id=selected_category)[0].name
    return render(request, 'product/product_import_page.html', {
      'product': product,
      'selected_category': selected_category,
      'variations': variations,
      'showVariations': showVariations,
      'showWithoutVariation': showWithoutVariation,
      'CONDITION_CHOICES': CONDITION_CHOICES
    })


def product_edit(request, selected_category, product_id):
  CONDITION_CHOICES = [
    ('N', 'New'),
    ('U', 'Used'),
  ]

  showVariations = ""
  showWithoutVariation = "active show"


  if (request.method == "POST"):
    product = {}
    variations = [{}] * 7
    print("EDIT POST %s" % request.POST)

    product['product_code'] = request.POST.get('product-code')
    product['product-category-id'] = request.POST.get('product-category-id')
    if(selected_category == '0'):
      category = Category.objects.filter(unique_id=int(product['product-category-id']))
    else:
      category = Category.objects.filter(unique_id=int(selected_category))
    product['category'] = category[0].name
    
    product['product_name'] = request.POST.get('product-name')
    product['product_description'] = request.POST.get('product-description')

    product['product_length'] = request.POST.get('product-length')
    product['product_width'] = request.POST.get('product-width')
    product['product_height'] = request.POST.get('product-height')
    product['product_weight'] = request.POST.get('product-weight')

    product['product_price'] = request.POST.get('product-price')

    product['product_stock'] = request.POST.get('product-stock')
    product['product_condition'] = request.POST.get('product-condition')
    product['parent_sku_reference_no'] = request.POST.get('product-parent-sku')
    errors = []

    if (not product['product_code']):
      errors.append('Product Code is required; ')
    if (not product['product-category-id'] or request.POST.get('product-category-id') == "None"):
      errors.append('Product Category is required; ')
    if (not product['product_name']):
      errors.append('Product Name is required; ')
    if (not product['product_description']):
      errors.append('Product Description is required; ')
    for i in range(0, 7):
      if (request.POST.get('product-variation-' + str(i) + '-sku')):
        if (not request.POST.get('product-variation-' + str(i) + '-name')):
          errors.append('Variation ' + str(i + 1) + ': name is required; ')
        if (not request.POST.get('product-variation-' + str(i) + '-stock')):
          errors.append('Variation ' + str(i + 1) + ': stock is required; ')
        if (not request.POST.get('product-variation-' + str(i) + '-price')):
          errors.append('Variation ' + str(i + 1) + ': price is required; ')
    if (not errors):

      t = Product(id=product_id,
        product_code=request.POST.get('product-code'),
        profile_id=request.user.id,
        category=request.POST.get('product-category-id'),
        product_name=request.POST.get('product-name'),
        product_description=request.POST.get('product-description'),
        # this may be empty strings so we replace it with None if empty string
        product_price=request.POST.get('product-price') if request.POST.get('product-price') else None,
        # this is evaluates as tertiary operator
        stock_sum=request.POST.get('product-stock') if request.POST.get('product-stock') else None,
        product_length=request.POST.get('product-length') if request.POST.get('product-length') else None,
        product_width=request.POST.get('product-width') if request.POST.get('product-width') else None,
        product_height=request.POST.get('product-height') if request.POST.get('product-height') else None,
        product_weight=request.POST.get('product-weight') if request.POST.get('product-weight') else None,

        product_condition=request.POST.get('product-condition'),
        parent_sku_reference_no=request.POST.get('product-parent-sku'),

        live=False,
        suspended=False,
        unlisted=True,
        unpublished=False
      )
      t.save()

      # this means that product has no variation so we delete any existing variation
      if request.POST.get('product-price'):
        Variations.objects.filter(product_id=product_id).delete()
      else:
        stock_sum = 0
        variations = Variations.objects.filter(product_id=product_id)
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
            v.image_url_from_sku=None

            v.save()
            if (request.FILES):
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
        'CONDITION_CHOICES': CONDITION_CHOICES
      })
  elif(selected_category == '0'):
    categories = {}
    with open('seller_center/static/documents/categories-full.json', 'r') as f:
      categories = json.load(f)
    return render(request, 'product/product_edit_page.html', {
      'product_id': product_id,
      'categories': categories,
      'selected_category': selected_category
    })
  else:
    product = {}
    selectedProduct = Product.objects.filter(id=product_id)[0]
    product['product_code'] = selectedProduct.product_code
    product['product_stock'] = selectedProduct.stock_sum
    category = Category.objects.filter(unique_id=selectedProduct.category)
    if len(category) == 0:
      product['category'] = "None"
    else:
      print(selected_category != selectedProduct.category)
      if(selected_category != selectedProduct.category):
        product['product_category_id'] = selected_category
        category = Category.objects.filter(unique_id=selected_category)
        product['category'] = category[0].name
      else:
        print("!")
        product['product_category_id'] = selectedProduct.category
        category = Category.objects.filter(unique_id=selectedProduct.category)
        product['category'] = category[0].name
      
    product['product_name'] = selectedProduct.product_name
    product['product_description'] = selectedProduct.product_description

    product['product_price'] = selectedProduct.product_price
    product['stock_sum'] = selectedProduct.stock_sum



    product['product_length'] = selectedProduct.product_length
    product['product_width'] = selectedProduct.product_width
    product['product_height'] = selectedProduct.product_height
    product['product_weight'] = selectedProduct.product_weight

    product['product_condition'] = selectedProduct.product_condition
    product['parent_sku_reference_no'] = selectedProduct.parent_sku_reference_no

    product['variations'] = Variations.objects.filter(product_id=product_id)

    variations = [{}]*7
    for index, v in enumerate(product['variations']):
      tmp = {
        'variation_sku': v.sku,
        'variation_price': v.price,
        'variation_stock': v.stock,
        'variation_name': v.name,
        'variation_url': v.image_url
      }
      variations[index] = tmp
      showVariations = "active show"
      showWithoutVariation = ""
    return render(request, 'product/product_edit_page.html', {
      'product_id': product_id,
      'selected_category': product['product_category_id'],
      'CONDITION_CHOICES': CONDITION_CHOICES,
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
          for index, row, in inputFileDF.head(500).iterrows():

            unpublished = False
            productID = None

            product = Product.objects.filter(profile_id=request.user.id).filter(product_code=row['product_code'])

            if(len(product)):
              print("Updating product %s" % product)

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
                  product.update(
                    product_code = row['product_code'],
                    profile_id = request.user.id,
                    category = row['category_id'],
                    order_id = None,
                    product_name = None,
                    product_description = None,
                    product_weight = row['product_weight'] if row['product_weight'] else None,
                    ship_out_in = row['ship_out_in'] if row['ship_out_in'] else None,
                    parent_sku_reference_no = row['parent_sku_reference_no'] if row['parent_sku_reference_no'] else None,
                    other_logistics_provider_setting = row['other_logistics_provider_setting'] if row['other_logistics_provider_setting'] else None,
                    other_logistics_provider_fee = row['other_logistics_provider_fee'] if row['other_logistics_provider_fee'] else None,
                    live = False,
                    suspended = False,
                    unlisted = False,
                    unpublished = unpublished
                  )
                  productID = product[0].id

                  Errors.objects.filter(product_id=productID).delete()
            else:
              print("Creating product %s" % row['product_code'])

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
                    category = row['category_id'],
                    order_id = None,
                    product_name = None,
                    product_description = None,
                    product_weight = row['product_weight'] if row['product_weight'] else None,
                    ship_out_in = row['ship_out_in'] if row['ship_out_in'] else None,
                    parent_sku_reference_no = row['parent_sku_reference_no'] if row['parent_sku_reference_no'] else None,
                    other_logistics_provider_setting = row['other_logistics_provider_setting'] if row['other_logistics_provider_setting'] else None,
                    other_logistics_provider_fee = row['other_logistics_provider_fee'] if row['other_logistics_provider_fee'] else None,
                    live = False,
                    suspended = False,
                    unlisted = False,
                    unpublished = unpublished
                  )
                  t.save()
                  productID = t.id

                  Errors.objects.filter(product_id = productID).delete()

            # Product name validation

            print("Product name checking required")
            if(row['product_name'] != row['product_name']):
              print("Product name is required")
              Product.objects.filter(id=productID).update(product_name=None)
              e = Errors(
                product_id = productID,
                name = 'Product name is required',
              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_name=row['product_name'])
              if(len(row['product_name'])<16):
                e = Errors(
                  product_id = productID,
                  name = 'Product name should have at least 16 characters',
                )
                e.save()
                unpublished = True

            # Product code validation
            if(row['product_code'] != row['product_code']):
              Product.objects.filter(id=productID).update(product_code=None)
              e = Errors(
                product_id = productID,
                name = 'Product code is required',
              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_code=row['product_code'])
              if(len(str(row['product_code']))>100):
                e = Errors(
                  product_id = productID,
                  name = 'Product code exceeds maximum lenght of 100',
                )
                e.save()
                unpublished = True

            # Product description validation
            if(row['product_description'] != row['product_description']):
              Product.objects.filter(id=productID).update(product_description=None)
              e = Errors(
                product_id = productID,
                name = 'Product description is required',

              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_description=row['product_description'])
              if(len(row['product_description'])<100):
                e = Errors(
                  product_id = productID,
                  name = 'Product description should have at least 100 characters',
                )
                e.save()
                unpublished = True

            # Product weight validation
            if(row['product_weight'] != row['product_weight']):
              Product.objects.filter(id=productID).update(product_description=None)
              e = Errors(
                product_id = productID,
                name = 'Product weight is required',
              )
              e.save()
              unpublished = True

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
                      name = 'Product image is required',
                    )
                    e.save()
            else:
              if(row['image1'] != row['image1']):
                unpublished = True
                e = Errors(
                  product_id = productID,
                  name = 'Product image is required',
                )
                e.save()
            
            # Insert/Update each product variation from file to database
            stock_sum = 0
            for i in range(0,7):
              if(row['variation'+str(i+1)+'_id'] == row['variation'+str(i+1)+'_id']):
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
                    name = 'Variation '+str(i+1)+' name is required',
                  )
                  e.save()

                # Product variation price validation
                if(variationPrice != variationPrice):
                  variationPrice = None
                  unpublished = True
                  e = Errors(
                    product_id = productID,
                    name = 'Variation '+str(i+1)+' price is required',
                  )
                  e.save()

                variation = Variations.objects.filter(product_id=productID).filter(sku=row['variation'+str(i+1)+'_id'])
                if(len(variation)):
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
              Product.objects.filter(id=productID).update(unlisted=True)  
            Product.objects.filter(id=productID).update(stock_sum=stock_sum, unpublished=unpublished)

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
    elif(len(Errors.objects.all())):
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