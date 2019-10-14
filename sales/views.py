from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import random
import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models import F

from product.models import Product, OrderedProduct
from product.models import Order

STATUS_CHOICES = [
	('S', 'To Ship'),
	('H', 'Shipping'),
	('C', 'Completed'),
	('L', 'Cancellation'),
	('R', 'Return/Refund'),
]

LOGISTICS_CHOICES = [
    'LOGISTIKUS',
    'QUADX',
    'MRSPEEDY',
    'XDE',
    'ELTM',
    'ABEST'
    'ZOOM',
    'NINJAVAN',
]

def orders(request):
	allOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id).distinct()
	allToShipOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id, status='TO_SHIP').distinct()
	allShippingOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id, status='SHIPPING').distinct()
	allDeliveredOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id, status='DELIVERED').distinct()
	allCompletedOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id, status='COMPLETED').distinct()
	allCancellationOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id, status='CANCELLATION').distinct()
	allReturnOrders = Order.objects.filter(orderedproduct__product__profile_id=request.user.id, status='RETURN_REFUND').distinct()
	return render(request, 'sales/sales_page.html', {
		'allOrders': allOrders,
		'allToShipOrders': allToShipOrders,
		'allShippingOrders': allShippingOrders,
		'allDeliveredOrders': allDeliveredOrders,
		'allCompletedOrders': allCompletedOrders,
		'allCancellationOrders': allCancellationOrders,
		'allReturnOrders': allReturnOrders,
		'nAll': len(allOrders),
		'nToShip': len(allToShipOrders),
		'nShipping': len(allShippingOrders),
		'nDelivered': len(allDeliveredOrders),
		'nCompleted': len(allCompletedOrders),
		'nCancellation': len(allCancellationOrders),
		'nReturn': len(allReturnOrders),
		'min_date' : datetime.datetime.now() + timedelta(days=1),
		'LOGISTICS_CHOICES': LOGISTICS_CHOICES
	})

def add_order(request):
	liveProducts = list(Product.objects.filter(product_status="LIVE_APPROVED", profile_id=request.user.id))
	orderedProducts = random.sample(liveProducts, k=20)
	o = Order(
		order_reference_number=1,
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
  shippingOption = request.POST.get('shipping-option')
  orderDate = request.POST.get('order-date')
  orderRemark = request.POST.get('order-remark')
  orderStatus = Order.objects.filter(order_reference_number=order_reference_number)[0].status

  if(orderStatus == 'TO_SHIP' and status != 'CANCELLATION'):
    Order.objects.filter(order_reference_number=order_reference_number).update(status=status)

		# Update quantity if status is changed to SHIPPING
    if(status == 'SHIPPING'):
      Order.objects.filter(order_reference_number=order_reference_number).update(
				courier=shippingOption, 
				order_date=orderDate, 
				order_remark=orderRemark, 
			)
      orderProducts = Order.objects.filter(order_reference_number=order_reference_number)[0].products.through.objects.all()
      for product in orderProducts:
        Product.objects.filter(id=product.id).update(stock_sum=F('stock_sum') - product.quantity)

    return HttpResponseRedirect("/orders/#all")
  else:
    messages.error(request, 'Only "To Ship" orders can be cancelled.')
    return HttpResponseRedirect("/orders/#all")
