from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.db import transaction
import pandas as pd

from product.models import ProductImportPage
from product.models import Product

class UploadFileForm(forms.Form):
  file = forms.FileField()


def products_import(request):
  if(request.method == "POST" and request.POST.get('upload')): 
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      inputFile = request.FILES['file']
      inputFileDF = pd.read_csv(inputFile)
      with transaction.atomic():
          Product.objects.all().delete()
          for index, row, in inputFileDF.iterrows():
            t = Product(
              product_code = row['product_code'],
              merchant_id = row['merchant_id'],
              category_id = row['category_id'],
              product_name = row['product_name'],
              product_description = row['product_description'],
              price = row['price'],
              stock = row['stock'],
              product_weight = row['product_weight'],
              ship_out_in = row['ship_out_in'],
              parent_sku_reference_no = row['parent_sku_reference_no'],
              variation1_id = row['variation1_id'],
              variation2_id = row['variation2_id'],
              variation3_id = row['variation3_id'],
              variation4_id = row['variation4_id'],
              variation5_id = row['variation5_id'],
              variation6_id = row['variation6_id'],
              variation7_id = row['variation7_id'],
              image1 = row['image1'],
              image2 = row['image2'],
              image3 = row['image3'],
              image4 = row['image4'],
              image5 = row['image5'],
              image6 = row['image6'],
              image7 = row['image7'],
              other_logistics_provider_setting = row['other_logistics_provider_setting'],
              other_logistics_provider_fee = row['other_logistics_provider_fee']
            )
            t.save()
    return HttpResponseRedirect("/products")
  else:
    form = UploadFileForm()
    
  self = ProductImportPage.objects.get(slug='import')
  
  return render(request, 'product/product_import_page.html', {
    'self': self,
    'form': form,
  })