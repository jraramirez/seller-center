from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import random

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
	liveProducts = Product.objects.filter(product_status="LIVE_APPROVED", profile_id=request.user.id)
	allOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id).distinct()

	# for order in allOrders:
	allUnpaidUsers = allToShipUsers = allShippingUsers = allCompletedUsers = allCancellationUsers = allReturnUsers = []
	allUnpaidOrders = Order.objects.filter(status='UNPAID')
	allToShipOrders = Order.objects.filter(status='TO_SHIP')
	allShippingOrders = Order.objects.filter(status='SHIPPING')
	allCompletedOrders = Order.objects.filter(status='COMPLETED')
	allCancellationOrders = Order.objects.filter(status='CANCELLATION')
	allReturnOrders = Order.objects.filter(status='RETURN_REFUND')
	# for order in allOrders:
	# 	allUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	# 	allUnpaidUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	# 	allToShipUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	# 	allShippingUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	# 	allCompletedUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	# 	allCancellationUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	# 	allReturnUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	return render(request, 'sales/sales_page.html', {
		'allUsersOrders': zip(allOrders),
		'allUnpaidUsersOrders': zip(allUnpaidOrders),
		'allToShipUsersOrders': zip( allToShipOrders),
		'allShippingUsersOrders': zip(allShippingOrders),
		'allCompletedUsersOrders': zip(allCompletedOrders),
		'allCancellationUsersOrders': zip(allCancellationOrders),
		'allReturnUsersOrders': zip(allReturnOrders),
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
	orderedProducts = random.sample(liveProducts, k=5)
	o = Order(status='UNPAID')
	o.save()

	for orderedProduct in orderedProducts:
		OrderedProduct.objects.create(product = orderedProduct, order=o, quantity=5)

	return render(request, 'sales/sales_page.html', {
		'orderedProducts': orderedProducts
	})


def set_status(request, order_id, status):
  Order.objects.filter(id=order_id).update(status=status)
  return HttpResponseRedirect("/orders/#all")
