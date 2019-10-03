from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import random
import datetime

from django.contrib.auth.models import User
from django.db.models import Sum, Count
from product.models import Product, OrderedProduct
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
	allOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id).distinct()
	allUnpaidOrders = Order.objects.filter(status='UNPAID')
	allToShipOrders = Order.objects.filter(status='TO_SHIP')
	allShippingOrders = Order.objects.filter(status='SHIPPING')
	allCompletedOrders = Order.objects.filter(status='COMPLETED')
	allCancellationOrders = Order.objects.filter(status='CANCELLATION')
	allReturnOrders = Order.objects.filter(status='RETURN_REFUND')
	return render(request, 'sales/sales_page.html', {
		'allOrders': allOrders,
		'allUnpaidOrders': allUnpaidOrders,
		'allToShipOrders': allToShipOrders,
		'allShippingOrders': allShippingOrders,
		'allCompletedOrders': allCompletedOrders,
		'allCancellationOrders': allCancellationOrders,
		'allReturnOrders': allReturnOrders,
		'nAll': len(allOrders),
		'nUnpaid': len(allUnpaidOrders),
		'nToShip': len(allToShipOrders),
		'nShipping': len(allShippingOrders),
		'nCompleted': len(allCompletedOrders),
		'nCancellation': len(allCancellationOrders),
		'nReturn': len(allReturnOrders),
	})

def add_order(request):
	liveProducts = list(Product.objects.filter(product_status="LIVE_APPROVED", profile_id=request.user.id))
	orderedProducts = random.sample(liveProducts, k=20)
	o = Order(
		status='TO_SHIP',
		user_id=request.user.id,
		username=request.user.username,
		creation_date=datetime.datetime.now
	)
	o.save()

	for orderedProduct in orderedProducts:
		op = OrderedProduct.objects.create(
			product = orderedProduct, 
			order=o, 
			quantity=1, 
			product_price=orderedProduct.product_price, 
			product_name=orderedProduct.product_name, 
			product_description=orderedProduct.product_description, 
			cover_image_url=orderedProduct.cover_image_url, 
		)
		op.save()
	return HttpResponseRedirect("/orders/#all")


def set_status(request, order_reference_number, status):
  Order.objects.filter(order_reference_number=order_reference_number).update(status=status)
  return HttpResponseRedirect("/orders/#all")
