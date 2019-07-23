from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from users.models import Profile
from sign_up.models import SignUpPage


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
      login(request, new_user)
      HttpResponseRedirect('/')
    else:
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
      login(request, new_user)
      return render(request, 'sign_up/sign_up_page_landing.html', {
        'request': request,
      })
  else:
    self = SignUpPage.objects.get(slug='sign')
    if(request.user):
      print(dir(request.user))
    if(not request.user.is_authenticated):
      return render(request, 'sign_up/sign_up_page.html', {
        'self': self,
      })
    else:
      return redirect('/')
