from django.shortcuts import render

def verify_email(request):
	print('verify')
	return render(request, 'account/verify_email.html', {})

def reset_password(request):
	print('reset')
	return render(request, 'account/reset_password.html', {})