from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from users.models import Profile
from sign_up.models import SignUpPage
from base.aws_client import AuthClient
from base.aws_client import ApiGatewayClient

from django.contrib import messages
import requests

def showErrorMessage(request, message):
    messages.error(request, message)
    self = SignUpPage.objects.get(slug='sign')
    return render(request, 'sign_up/sign_up_page.html', {
      'self': self,
    })

def sign_up(request):
  if(request.method == 'POST'):
    message = ''

    if(request.POST['reg-type'] == 'phone'):
      user = User.objects.create_user(
        username=request.POST['phone-number'],
        email=request.POST['phone-number'],
        password = request.POST['password']
      )
      group = Group.objects.get(name='Seller')
      user.groups.add(group)
      new_user = authenticate(
        username=request.POST['phone-number'],
        password=request.POST['password'],
      )
      #call api here
      login(request, new_user)
      HttpResponseRedirect('/')
    else:
      email = request.POST['email']
      password = request.POST['password']
      reenterPassword = request.POST['password-reenter']

      #TODO: validate inpunt on client side first if validateInput(email, password, reenterPassword)

      #call api here if success create a user else show necessary errors
      authClient = AuthClient(ApiGatewayClient())

      response = authClient.register("email", request.POST['email-address'])
      #TODO: Add button to resend verification link

      json = response.json()
      print(response.json())
      if (response.status_code == 200):
        json = response.json()
        response = authClient.login(json['clientId'], json['clientSecret'])
        
        if (response.status_code == 200):
          json = response.json()
          if  (json['message'] == "User is not confirmed."):
            return showErrorMessage(request, json['message'])

        # print("Status: %s - %s",response.status_code, response.json())

        # response = authClient.setupPassword(json['clientId'], json['clientSecret'], request.POST['password'])
        # print(response.json())
        # user = User.objects.create_user(
        #   username=request.POST['email-address'],
        #   email=request.POST['email-address'],
        #   password=request.POST['password']
        # )
        # group = Group.objects.get(name='Seller')
        # user.groups.add(group)
        # new_user = authenticate(
        #   username=request.POST['email-address'],
        #   password=request.POST['password'],
        # )
        
        #login success
        #ogin(request, new_user)
        return render(request, 'sign_up/sign_up_page_landing.html', {
          'request': request,
        })
      else:
        return showErrorMessage(request, json['details'])
  else:
    self = SignUpPage.objects.get(slug='sign')
    if(not request.user.is_authenticated):
      return render(request, 'sign_up/sign_up_page.html', {
        'self': self,
      })
    else:
      return redirect('/')

