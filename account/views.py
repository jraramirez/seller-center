from django.shortcuts import render
from base.aws_client import AuthClient
from base.aws_client import ApiGatewayClient

def verify_email(request):
	if request.method == 'POST':
		username=request.POST['username']
		if not validate_email(email=username):
			return render(request, 'account/verify_email.html', {
				'error': "Please enter a valid email address"
			})
		authClient=AuthClient(ApiGatewayClient())
		response=authClient.forgot_password(username)
		json=response.json()
		if response.status_code == 200:
			return render(request, 'account/reset_password.html', {
				'email': username,
				'success': 'Email verification link sent',
				'error': ''
			})
	return render(request, 'account/verify_email.html', {})

def reset_password(request):
	if request.method == 'POST':
		username=request.POST['username']
		veri_code=request.POST['veri_code']
		new_pw=request.POST['new_pw']
		if not validate_email(email=username):
			return render(request, 'account/verify_email.html', {
				'error': "Please enter a valid email address"
			})
		authClient=AuthClient(ApiGatewayClient())
		response=authClient.reset_password(username, veri_code, new_pw)
		json=response.json()
		if response.status_code == 200:
			return render(request, 'wagtailadmin/login.html', {
				'success': 'Reset password was successful.',
				'error': ''
			})
	return render(request, 'account/reset_password.html', {})

def validate_email(email):
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email( email )
		return True
	except ValidationError:
		return False