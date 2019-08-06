from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
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

AWS_STORAGE_BUCKET_NAME = 'lyka-seller-center'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
media_url = "https://%s/media/original_images/" % AWS_S3_CUSTOM_DOMAIN


class UploadFileForm(forms.Form):
  file = forms.FileField(label="Choose a file")

def product_import(request, selected_category):
  nVariations = 7
  if(selected_category == 'index'):
    categories = {}
    with open('seller_center/static/documents/categories-full.json', 'r') as f:
      categories = json.load(f)
    # l1Categories = Category.objects.filter(parent_id=1891)
    # categories = [{} for _ in range(len(l1Categories))]
    # for i, c in zip(range(len(l1Categories)), l1Categories):
    #   categories[i]['name'] = c.name
    #   categories[i]['unique_id'] = c.unique_id
    #   categories[i]['level'] = 1
    #   categories[i]['top'] = str(-39*(i))+'px'
    #   l2Categories = Category.objects.filter(parent_id=c.unique_id)
    #   categories[i]['children'] = [{} for _ in range(len(l2Categories))]
    #   for j, c2 in zip(range(len(l2Categories)), l2Categories):
    #     categories[i]['children'][j]['name'] = c2.name
    #     categories[i]['children'][j]['unique_id'] = c2.unique_id
    #     categories[i]['children'][j]['level'] = c2.level
    #     categories[i]['children'][j]['top'] = str(-39*(j))+'px'
    #     l3Categories = Category.objects.filter(parent_id=c2.unique_id)
    #     categories[i]['children'][j]['children'] = [{} for _ in range(len(l3Categories))]
    #     for k, c3 in zip(range(len(l3Categories)), l3Categories):
    #       categories[i]['children'][j]['children'][k]['name'] = c3.name
    #       categories[i]['children'][j]['children'][k]['unique_id'] = c3.unique_id
    #       categories[i]['children'][j]['children'][k]['level'] = c3.level
    return render(request, 'product/product_import_page.html', {
      'categories': categories,
      'selected_category': selected_category
    })
  elif(request.method == "POST"):
    t = Product(
      product_code = request.POST.get('product-code'),
      profile_id = request.user.id,
      category = selected_category,
      order_id = None,
      product_name = request.POST.get('product-name'),
      product_description = request.POST.get('product-description'),
      product_weight = request.POST.get('product-weight'),
      ship_out_in = None,
      parent_sku_reference_no = request.POST.get('product-parent-sku'),
      other_logistics_provider_setting = None,
      other_logistics_provider_fee = None,
      live = False,
      suspended = False,
      unlisted = False,
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
          name = request.POST.get('product-variation-'+str(i)+'-sku'),
          image_url_from_sku = None
        )
        v.save()
        image = request.FILES['product-variation-'+str(i)+'-image']
        Image.objects.create(
          file=image,
          title=image.name
        )
        # v.image_upload.save(image.name, image)
    return HttpResponseRedirect("/products/#all")
  else:
    selected_category = Category.objects.filter(unique_id=selected_category)[0].name
    return render(request, 'product/product_import_page.html', {
      'selected_category': selected_category,
      'variations': range(nVariations)
    })
    

def products_import(request):
  if(request.method == "POST" and request.POST.get('upload')): 
    autoPair = request.POST.get('auto-pair')
    print(autoPair)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      inputFile = request.FILES['file']
      inputFileDF = pd.read_csv(inputFile)
      with transaction.atomic():
        for index, row, in inputFileDF.iterrows():
          unpublished = False
          t = Product(
            product_code = row['product_code'],
            profile_id = request.user.id,
            category = None,
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

          # Product name validation
          if(row['product_name'] != row['product_name']):
            Product.objects.filter(id=t.id).update(product_name=None)
            e = Errors(
              product_id = t.id,
              name = 'Product name is required'
            )
            e.save()
            unpublished = True
          else:
            Product.objects.filter(id=t.id).update(product_name=row['product_name'])
            if(len(row['product_name'])<16):
              e = Errors(
                product_id = t.id,
                name = 'Product name should have at least 16 characters'
              )
              e.save()
              unpublished = True

          # Product code validation
          if(row['product_code'] != row['product_code']):
            Product.objects.filter(id=t.id).update(product_code=None)
            e = Errors(
              product_id = t.id,
              name = 'Product code is required'
            )
            e.save()
            unpublished = True
          else:
            Product.objects.filter(id=t.id).update(product_code=row['product_code'])
            if(len(row['product_code'])>100):
              e = Errors(
                product_id = t.id,
                name = 'Product code exceeds maximum lenght of 100'
              )
              e.save()
              unpublished = True

          # Product description validation
          if(row['product_description'] != row['product_description']):
            Product.objects.filter(id=t.id).update(product_description=None)
            e = Errors(
              product_id = t.id,
              name = 'Product description is required'
            )
            e.save()
            unpublished = True
          else:
            Product.objects.filter(id=t.id).update(product_description=row['product_description'])
            if(len(row['product_description'])<100):
              e = Errors(
                product_id = t.id,
                name = 'Product description should have at least 100 characters'
              )
              e.save()
              unpublished = True

          # Product weight validation
          if(row['product_weight'] != row['product_weight']):
            Product.objects.filter(id=t.id).update(product_description=None)
            e = Errors(
              product_id = t.id,
              name = 'Product weight is required'
            )
            e.save()
            unpublished = True

          # Product image validation
          imageInS3 = False
          if(autoPair):
            image_url_from_sku = None
            if(row['variation1_id'] == row['variation1_id']):
              if(row['image1'] != row['image1']):
                url = media_url + str(row['variation1_id']) + '.jpg'
                r = requests.get(url)
                if r.status_code == 200:
                  image_url_from_sku = url
                  imageInS3 = True
                else:
                  url = media_url + str(row['variation1_id']) + '.png'
                  r = requests.get(url)
                  if r.status_code == 200:
                    image_url_from_sku = url
                    imageInS3 = True
                  else:
                    unpublished = True
                    e = Errors(
                      product_id = t.id,
                      name = 'Product image is required'
                    )
                    e.save()
          else:
            if(row['image1'] != row['image1']):
              unpublished = True
              e = Errors(
                product_id = t.id,
                name = 'Product image is required'
              )
              e.save()
          stock_sum = 0
          for i in range(0,7):
            if(not np.isnan(row['variation'+str(i+1)+'_id'])):
              variationStock = 0
              if(row['variation'+str(i+1)+'_stock'] == row['variation'+str(i+1)+'_stock']):
                variationStock = row['variation'+str(i+1)+'_stock']
              stock_sum = stock_sum + variationStock
              if(i == 0 and not imageInS3 and not autoPair):
                image_url_from_sku = None
              v = Variations(
                product_id = t.id,
                image_url = row['image'+str(i+1)],
                price = row['variation'+str(i+1)+'_price'],
                sku = row['variation'+str(i+1)+'_id'],
                stock = variationStock,
                name = row['variation'+str(i+1)+'_id'],
                image_url_from_sku = image_url_from_sku
              )
              v.save()
          Product.objects.filter(id=t.id).update(stock_sum=stock_sum, unpublished=unpublished)

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