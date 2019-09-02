from django.shortcuts import render

def orders(request):
	print(request.user.id) # use merchant id to get all his/her orders
	return render(request, 'sales/sales_page.html', {})