from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
	allUnpaidUsers = allToShipUsers = allShippingUsers = allCompletedUsers = allCancellationUsers = allReturnUsers = []
	allUnpaidOrders = Order.objects.filter(status='UNPAID')
	allToShipOrders = Order.objects.filter(status='TO_SHIP')
	allShippingOrders = Order.objects.filter(status='SHIPPING')
	allCompletedOrders = Order.objects.filter(status='COMPLETED')
	allCancellationOrders = Order.objects.filter(status='CANCELLATION')
	allReturnOrders = Order.objects.filter(status='RETURN_REFUND')
	for order in allOrders:
		allUsers.append(User.objects.filter(id=order.profile_id)[0].username)
		allUnpaidUsers.append(User.objects.filter(id=order.profile_id)[0].username)
		allToShipUsers.append(User.objects.filter(id=order.profile_id)[0].username)
		allShippingUsers.append(User.objects.filter(id=order.profile_id)[0].username)
		allCompletedUsers.append(User.objects.filter(id=order.profile_id)[0].username)
		allCancellationUsers.append(User.objects.filter(id=order.profile_id)[0].username)
		allReturnUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	return render(request, 'sales/sales_page.html', {
		'allUsersOrders': zip(allUsers, allOrders),
		'allUnpaidUsersOrders': zip(allUnpaidUsers, allUnpaidOrders),
		'allToShipUsersOrders': zip(allToShipUsers, allToShipOrders),
		'allShippingUsersOrders': zip(allShippingUsers, allShippingOrders),
		'allCompletedUsersOrders': zip(allCompletedUsers, allCompletedOrders),
		'allCancellationUsersOrders': zip(allCancellationUsers, allCancellationOrders),
		'allReturnUsersOrders': zip(allReturnUsers, allReturnOrders),
		'nAll': len(allOrders),
		'nUnpaid': len(allUnpaidOrders),
		'nToShip': len(allToShipOrders),
		'nShipping': len(allShippingOrders),
		'nCompleted': len(allCompletedOrders),
		'nCancellation': len(allCancellationOrders),
		'nReturn': len(allReturnOrders),
	})

def add_order(request):
	liveProducts = list(Product.objects.filter(product_status="LIVE_APPROVED"))
	orderedProducts = random.sample(liveProducts, k=5)
	o = Order(profile_id=request.user.id, status='UNPAID')
	o.save()

	for orderedProduct in orderedProducts:
		o.products.add(orderedProduct)

	return render(request, 'sales/sales_page.html', {
		'orderedProducts': orderedProducts
	})


def set_status(request, order_id, status):
  Order.objects.filter(id=order_id).update(status=status)
  return HttpResponseRedirect("/orders/#all")
