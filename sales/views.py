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
	allUnpaidUsers = allToShipUsers = allShippingUsers = allCompletedUsers = allCancellationUsers = allReturnUsers = []
	allUnpaidOrders = Order.objects.filter(status='Unpaid')
	allToShipOrders = Order.objects.filter(status='To Ship')
	allShippingOrders = Order.objects.filter(status='Shipping')
	allCompletedOrders = Order.objects.filter(status='Completed')
	allCancellationOrders = Order.objects.filter(status='Cancellation')
	allReturnOrders = Order.objects.filter(status='Return/Refund')
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
	o = Order(profile_id=request.user.id, status=STATUS_CHOICES[0][1])
	o.save()

	for orderedProduct in orderedProducts:
		o.products.add(orderedProduct)

	return render(request, 'sales/sales_page.html', {
		'orderedProducts': orderedProducts
	})