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
from product.models import Order, OrderCourier, Courier

STATUS_CHOICES = [
	('S', 'To Ship'),
	('H', 'Shipping'),
	('C', 'Completed'),
	('R', 'Received'),
	('D', 'Delivered'),
	('L', 'SellerCanceled'),
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
	allUserProductsIds = Product.objects.filter(profile_id=request.user.id).distinct().values_list('id', flat=True)
	allOrderIds = OrderedProduct.objects.filter(product_id__in=allUserProductsIds).distinct().values_list('order_id', flat=True)

	allProductsByOrder = []
	allToShipProductsByOrder = []
	allShippingProductsByOrder = []
	allDeliveredProductsByOrder = []
	allCompletedProductsByOrder = []
	allReceivedProductsByOrder = []
	allSellerCanceledProductsByOrder = []
	allReturnProductsByOrder = []
	for orderId in allOrderIds:
		allOrderedProductsIds = OrderedProduct.objects.filter(product_id__in=allUserProductsIds, order_id=orderId).distinct().values_list('id', flat=True)
		status = orderStatus = Order.objects.filter(order_reference_number=orderId)[0].status
		username = Order.objects.filter(order_reference_number=orderId)[0].username
		order = {
			'username': username,
			'status': status,
			'order_reference_number': orderId,
			'products': Product.objects.filter(id__in=allOrderedProductsIds).distinct()
		}
		if(orderStatus == 'FOR_SHIPPING'):
			allToShipProductsByOrder.append(order)
		if(orderStatus == 'SHIPPING'):
			allShippingProductsByOrder.append(order)
		if(orderStatus == 'DELIVERED'):
			allDeliveredProductsByOrder.append(order)
		if(orderStatus == 'RECEIVED'):
			allReceivedProductsByOrder.append(order)
		if(orderStatus == 'COMPLETED'):
			allCompletedProductsByOrder.append(order)
		if(orderStatus == 'SELLER_CANCELED'):
			allSellerCanceledProductsByOrder.append(order)
		if(orderStatus == 'RETURN_REFUND'):
			allReturnProductsByOrder.append(order)
		allProductsByOrder.append(order)

	return render(request, 'sales/sales_page.html', {
		'allProductsByOrder': allProductsByOrder,
		'allToShipProductsByOrder': allToShipProductsByOrder,
		'allShippingProductsByOrder': allShippingProductsByOrder,
		'allDeliveredProductsByOrder': allDeliveredProductsByOrder,
		'allCompletedProductsByOrder': allCompletedProductsByOrder,
		'allReceivedProductsByOrder': allReceivedProductsByOrder,
		'allSellerCanceledProductsByOrder': allSellerCanceledProductsByOrder,
		'allReturnProductsByOrder': allReturnProductsByOrder,
		'nAll': len(allProductsByOrder),
		'nToShip': len(allToShipProductsByOrder),
		'nShipping': len(allShippingProductsByOrder),
		'nDelivered': len(allDeliveredProductsByOrder),
		'nReceived': len(allReceivedProductsByOrder),
		'nCompleted': len(allCompletedProductsByOrder),
		'nSellerCanceled': len(allSellerCanceledProductsByOrder),
		'nReturn': len(allReturnProductsByOrder),
		'min_date' : datetime.datetime.now() + timedelta(days=1),
		'LOGISTICS_CHOICES': LOGISTICS_CHOICES
	})

def add_order(request):
	liveProducts = list(Product.objects.filter(product_status="LIVE_APPROVED", profile_id=request.user.id))
	orderedProducts = random.sample(liveProducts, k=20)
	o = Order(
		order_reference_number=1,
		status='FOR_SHIPPING',
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
  currentDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z")
  
  if(orderStatus == 'FOR_SHIPPING' and status == 'SHIPPING'):
    Order.objects.filter(order_reference_number=order_reference_number).update(status=status)
    Order.objects.filter(order_reference_number=order_reference_number).update(status_changed_on=currentDate)

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
      
      # Create logistics instance once order status is changed to SHIPPING
      if(len(Courier.objects.all())):
        oc = OrderCourier(
          courier_id= Courier.objects.filter(courier_name=shippingOption),
          status='default status',
          status_info='default status info',
        )
        oc.save()

  elif(orderStatus == 'SHIPPING' and status == 'DELIVERED'):
    Order.objects.filter(order_reference_number=order_reference_number).update(status=status)
    Order.objects.filter(order_reference_number=order_reference_number).update(status_changed_on=currentDate)

  elif(orderStatus == 'RECEIVED' and status == 'COMPLETED'):
    Order.objects.filter(order_reference_number=order_reference_number).update(status=status)
    Order.objects.filter(order_reference_number=order_reference_number).update(status_changed_on=currentDate)

  else:
    messages.error(request, 'Cannot perform this action.')

  return HttpResponseRedirect("/orders/#all")
