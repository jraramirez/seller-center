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

from seller_center.settings.production import MEDIA_URL
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

  if(selected_category == 'index'):
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
        product_length = request.POST.get('product_length') if request.POST.get('product_length') else None,
        product_width = request.POST.get('product_width') if request.POST.get('product_width') else None,
        product_height = request.POST.get('product_height') if request.POST.get('product_height') else None,
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
            # Image.objects.create(
            #   file=image,
            #   title=image.name
            # )
            v.image_upload.save(image.name, image)
            Variations.objects.filter(id=v.id).update(
              image_url_from_upload = media_url + 'original_images/' + str(image.name)
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


def product_edit(request, product_id):
  CONDITION_CHOICES = [
    ('N', 'New'),
    ('U', 'Used'),
  ]

  showVariations = ""
  showWithoutVariation = "active show"

  # if(selected_category == 'index'):
  #   categories = {}
  #   with open('seller_center/static/documents/categories-full.json', 'r') as f:
  #     categories = json.load(f)
  #   return render(request, 'product/product_import_page.html', {
  #     'categories': categories,
  #     'selected_category': selected_category
  #   })
  if(request.method == "POST"):
    Product.objects.filter(id=product_id).update(
      product_code = request.POST.get('product-code'),
      product_name = request.POST.get('product-name'),
      product_description = request.POST.get('product-description'),
      product_weight = request.POST.get('product-weight'),
      parent_sku_reference_no = request.POST.get('product-parent-sku'),
      product_condition = request.POST.get('product-condition'),
    )
    # stock_sum = 0
    # for i in range(0,8):
    #   if(request.POST.get('product-variation-'+str(i)+'-sku')):
    #     variationStock = 0
    #     if(request.POST.get('product-variation-'+str(i)+'-stock')):
    #       variationStock = int(request.POST.get('product-variation-'+str(i)+'-stock'))
    #     stock_sum = stock_sum + variationStock
    #     v = Variations(
    #       product_id = t.id,
    #       image_url = None,
    #       price =request.POST.get('product-variation-'+str(i)+'-price'),
    #       sku = request.POST.get('product-variation-'+str(i)+'-sku'),
    #       stock = variationStock,
    #       name = request.POST.get('product-variation-'+str(i)+'-sku'),
    #       image_url_from_sku = None
    #     )
    #     v.save()
    #     image = request.FILES['product-variation-'+str(i)+'-image']
    #     Image.objects.create(
    #       file=image,
    #       title=image.name
    #     )
    #     # v.image_upload.save(image.name, image)
    messages.success(request, 'Product edited successfully.')
    return HttpResponseRedirect("/products/#all")
  else:
    product = {}
    selectedProduct = Product.objects.filter(id=product_id)[0]
    product['product_code'] = selectedProduct.product_code
    product['category'] = Category.objects.filter(unique_id=selectedProduct.category)[0].name
    product['product_name'] = selectedProduct.product_name
    product['product_description'] = selectedProduct.product_description
    product['product_price'] = selectedProduct.product_price
    product['stock_sum'] = selectedProduct.stock_sum
    product['product_weight'] = selectedProduct.product_weight
    product['parent_sku_reference_no'] = selectedProduct.parent_sku_reference_no
    product['product_category'] = Category.objects.filter(unique_id=selectedProduct.category)[0].name
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
    print("Variations: %s" % product['variations'])
    return render(request, 'product/product_edit_page.html', {
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
    missingColumns = []
    if form.is_valid():
      inputFile = request.FILES['file']
      inputFileDF = pd.read_csv(inputFile)

      # Check if there are missing columns
      for column in CSV_COLUMNS: 
        if(column not in inputFileDF.columns.values):
          missingColumns.append(column)
          invalid = True
      if(not invalid):
        # Obtain titles of images
        imageTitles = []
        for title in Image.objects.values_list('title', flat=True):
          imageTitles.append(os.path.splitext(title)[0])
        
        # Insert/Update each product from file to database
        with transaction.atomic():
          for index, row, in inputFileDF.head(500).iterrows():
            unpublished = False
            productID = None
            product = Product.objects.filter(profile_id=request.user.id).filter(product_code=row['product_code'])
            if(len(product)):
              product.update(
                product_code = row['product_code'],
                profile_id = request.user.id,
                category = row['category_id'],
                order_id = None,
                product_name = None,
                product_description = None,
                product_weight = row['product_weight'],
                ship_out_in = row['ship_out_in'],
                parent_sku_reference_no = row['parent_sku_reference_no'],
                other_logistics_provider_setting = row['other_logistics_provider_setting'],
                other_logistics_provider_fee = row['other_logistics_provider_fee'],
                live = False,
                suspended = False,
                unlisted = False,
                unpublished = unpublished
              )
              productID = product[0].id
            else:
              t = Product(
                product_code = row['product_code'],
                profile_id = request.user.id,
                category = row['category_id'],
                order_id = None,
                product_name = None,
                product_description = None,
                product_weight = row['product_weight'],
                ship_out_in = row['ship_out_in'],
                parent_sku_reference_no = row['parent_sku_reference_no'],
                other_logistics_provider_setting = row['other_logistics_provider_setting'],
                other_logistics_provider_fee = row['other_logistics_provider_fee'],
                live = False,
                suspended = False,
                unlisted = False,
                unpublished = unpublished
              )
              t.save()
              productID = t.id
            
            Errors.objects.filter(product_id = productID).delete()

            # Product name validation
            if(row['product_name'] != row['product_name']):
              Product.objects.filter(id=productID).update(product_name=None)
              e = Errors(
                product_id = productID,
                name = 'Product name is required',
                profile_id = request.user.id
              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_name=row['product_name'])
              if(len(row['product_name'])<16):
                e = Errors(
                  product_id = productID,
                  name = 'Product name should have at least 16 characters',
                  profile_id = request.user.id
                )
                e.save()
                unpublished = True

            # Product code validation
            if(row['product_code'] != row['product_code']):
              Product.objects.filter(id=productID).update(product_code=None)
              e = Errors(
                product_id = productID,
                name = 'Product code is required',
                profile_id = request.user.id
              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_code=row['product_code'])
              if(len(str(row['product_code']))>100):
                e = Errors(
                  product_id = productID,
                  name = 'Product code exceeds maximum lenght of 100',
                  profile_id = request.user.id
                )
                e.save()
                unpublished = True

            # Product description validation
            if(row['product_description'] != row['product_description']):
              Product.objects.filter(id=productID).update(product_description=None)
              e = Errors(
                product_id = productID,
                name = 'Product description is required',
                profile_id = request.user.id

              )
              e.save()
              unpublished = True
            else:
              Product.objects.filter(id=productID).update(product_description=row['product_description'])
              if(len(row['product_description'])<100):
                e = Errors(
                  product_id = productID,
                  name = 'Product description should have at least 100 characters',
                  profile_id = request.user.id
                )
                e.save()
                unpublished = True

            # Product weight validation
            if(row['product_weight'] != row['product_weight']):
              Product.objects.filter(id=productID).update(product_description=None)
              e = Errors(
                product_id = productID,
                name = 'Product weight is required',
                profile_id = request.user.id
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
                      profile_id = request.user.id
                    )
                    e.save()
            else:
              if(row['image1'] != row['image1']):
                unpublished = True
                e = Errors(
                  product_id = productID,
                  name = 'Product image is required',
                  profile_id = request.user.id
                )
                e.save()
            
            # Insert/Update each product variation from file to database
            stock_sum = 0
            for i in range(0,7):
              if(row['variation'+str(i+1)+'_id'] == row['variation'+str(i+1)+'_id']):
                variationStock = 0
                if(row['variation'+str(i+1)+'_stock'] == row['variation'+str(i+1)+'_stock']):
                  variationStock = row['variation'+str(i+1)+'_stock']
                stock_sum = stock_sum + variationStock
                if(i == 0 and not imageInS3 and not autoPair):
                  image_url_from_sku = None
                image_url = row['image1']
                if(row['image1'] != row['image1']):
                  image_url = None
                variation = Variations.objects.filter(product_id=productID).filter(sku=row['variation'+str(i+1)+'_id'])
                if(len(variation)):
                  variation.update(
                    product_id = productID,
                    image_url = image_url,
                    price = row['variation'+str(i+1)+'_price'],
                    sku = row['variation'+str(i+1)+'_id'],
                    stock = variationStock,
                    name = row['variation'+str(i+1)+'_name'],
                    image_url_from_sku = image_url_from_sku
                  )
                else:
                  v = Variations(
                    product_id = productID,
                    image_url = image_url,
                    price = row['variation'+str(i+1)+'_price'],
                    sku = row['variation'+str(i+1)+'_id'],
                    stock = variationStock,
                    name = row['variation'+str(i+1)+'_name'],
                    image_url_from_sku = image_url_from_sku
                  )
                  v.save()
            if(not unpublished):
              Product.objects.filter(id=productID).update(unlisted=True)  
            Product.objects.filter(id=productID).update(stock_sum=stock_sum, unpublished=unpublished)

    if(invalid):
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