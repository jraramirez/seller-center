from django.shortcuts import render
import random

from django.contrib.auth.models import User
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
	allOrders = Order.objects.all()
	allUsers = []
	for order in allOrders:
		allUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	return render(request, 'sales/sales_page.html', {
		'allUsersOrders': zip(allUsers, allOrders)	
	})

def add_order(request):
	liveProducts = list(Product.objects.filter(live=True))
	orderedProducts = random.sample(liveProducts, k=5)
	o = Order(profile_id=request.user.id, status=STATUS_CHOICES[0][1])
	o.save()

	for orderedProduct in orderedProducts:
		o.products.add(orderedProduct)

	return render(request, 'sales/sales_page.html', {
		'orderedProducts': orderedProducts
	})