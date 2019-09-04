from django.shortcuts import render
import random

from product.models import Product
from product.models import Order

STATUS_CHOICES = [
	('U', 'Unpaid'),
	('S', 'To Ship'),
	('H', 'Shipping'),
	('C', 'Completed'),
	('L', 'Cancellation'),
	('R', 'Return/Refund'),
]

def orders(request):
	print(request.user.id) # use merchant id to get all his/her orders
	return render(request, 'sales/sales_page.html', {})

def add_order(request):
	liveProducts = Product.objects.filter(live=True)
	print(liveProducts)
	orderedProducts = random.sample(liveProducts, k=5)
	o = Order(status=STATUS_CHOICES[0])

	for orderedProduct in orderedProducts:
		o.products.add(orderedProduct)

	return render(request, 'sales/sales_page.html', {
		'orderedProducts': orderedProducts
	})