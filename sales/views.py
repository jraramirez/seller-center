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
	for order in allOrders:
		allUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	allUnpaidOrders = Order.objects.filter(status='Unpaid')
	for order in allOrders:
		allUnpaidUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	allToShipOrders = Order.objects.filter(status='To Ship')
	for order in allOrders:
		allToShipUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	allShippingOrders = Order.objects.filter(status='Shipping')
	for order in allOrders:
		allShippingUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	allCompletedOrders = Order.objects.filter(status='Completed')
	for order in allOrders:
		allCompletedUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	allCancellationOrders = Order.objects.filter(status='Cancellation')
	for order in allOrders:
		allCancellationUsers.append(User.objects.filter(id=order.profile_id)[0].username)
	allReturnOrders = Order.objects.filter(status='Return/Refund')
	for order in allOrders:
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
	liveProducts = list(Product.objects.filter(live=True))
	orderedProducts = random.sample(liveProducts, k=5)
	o = Order(profile_id=request.user.id, status=STATUS_CHOICES[0][1])
	o.save()

	for orderedProduct in orderedProducts:
		o.products.add(orderedProduct)

	return render(request, 'sales/sales_page.html', {
		'orderedProducts': orderedProducts
	})