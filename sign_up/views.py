from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from users.models import Profile
from sign_up.models import SignUpPage

from django.contrib import messages
import requests

def sign_up(request):
  if(request.method == 'POST'):
    message = ''
    if(request.POST['reg-type'] == 'phone'):
      user = User.objects.create_user(
        username=request.POST['phone-number'],
        email=request.POST['phone-number'],
        password=request.POST['password']
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
      #call api here if success create a user else show necessary errors
      data = {
        'type':'email',
        'value': 'jeramos.dev@gmail.com'
      }

      r = requests.post('https://vak4dovce5.execute-api.ap-southeast-1.amazonaws.com/dev/api/v1/register', json=data)

      response = r.json()
      print(response)

      if (r.status_code == 200):
        user = User.objects.create_user(
          username=request.POST['email-address'],
          email=request.POST['email-address'],
          password=request.POST['password']
        )
        group = Group.objects.get(name='Seller')
        user.groups.add(group)
        new_user = authenticate(
          username=request.POST['email-address'],
          password=request.POST['password'],
        )
        
        #login success
        login(request, new_user)
        return render(request, 'sign_up/sign_up_page_landing.html', {
          'request': request,
        })
      else:
        messages.error(request, response['details'])
        self = SignUpPage.objects.get(slug='sign')
        return render(request, 'sign_up/sign_up_page.html', {
          'self': self,
        })
  else:
    self = SignUpPage.objects.get(slug='sign')
    if(not request.user.is_authenticated):
      return render(request, 'sign_up/sign_up_page.html', {
        'self': self,
      })
    else:
      return redirect('/')
