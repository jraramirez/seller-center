from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
import pandas as pd
import numpy as np
import os

from product.models import ProductsImportPage
from product.models import Product
from product.models import Variations

class UploadFileForm(forms.Form):
  file = forms.FileField(label="Choose a file")


def product_import(request):
  if(request.method == 'POST'):
    # return render(request, 'product/products_page.html', {
    # })
    return redirect('/products')
  else:
    return render(request, 'product/product_import_page.html', {
    })


def products_import(request):
  if(request.method == "POST" and request.POST.get('upload')): 
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      inputFile = request.FILES['file']
      inputFileDF = pd.read_csv(inputFile)
      with transaction.atomic():
        # Product.objects.all().delete()
        for index, row, in inputFileDF.iterrows():
          t = Product(
            product_code = row['product_code'],
            profile_id = request.user.id,
            category = None,
            order_id = None,
            product_name = row['product_name'],
            product_description = row['product_description'],
            product_weight = row['product_weight'],
            ship_out_in = row['ship_out_in'],
            parent_sku_reference_no = row['parent_sku_reference_no'],
            other_logistics_provider_setting = row['other_logistics_provider_setting'],
            other_logistics_provider_fee = row['other_logistics_provider_fee'],
            live = False,
            suspended = False,
            unlisted = False
          )
          t.save()
          for i in range(0,7):
            if(not np.isnan(row['variation'+str(i+1)+'_id'])):
              print(row['variation'+str(i+1)+'_id'])
              variationStock = 0
              if(row['variation'+str(i+1)+'_stock'] == row['variation'+str(i+1)+'_stock']):
                variationStock = row['variation'+str(i+1)+'_stock']
              v = Variations(
                product_id = t.id,
                image_url = row['image'+str(i+1)],
                price = row['variation'+str(i+1)+'_price'],
                sku = row['variation'+str(i+1)+'_id'],
                stock = variationStock,
                name = row['variation'+str(i+1)+'_id']
              )
              v.save()

    return HttpResponseRedirect("/products")
  else:
    form = UploadFileForm()
    
  self = ProductsImportPage.objects.get(slug='add-new-products')
  
  return render(request, 'product/products_import_page.html', {
    'self': self,
    'form': form,
  })


# function for downloading CPC extractor sample file as Excel file
def download_template(request):
  print(os.getcwd())
  outFileName = 'Import Products Template'
  outFolderName = 'seller_center/static/documents/'
  fileType = '.csv'
  path = outFolderName + outFileName + fileType
  print(os.path.exists(path))
  if os.path.exists(path):
    with open(path, "rb") as excel:
      data = excel.read()
    response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=' + outFileName + fileType
    return response