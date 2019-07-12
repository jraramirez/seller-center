from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from sign_up.models import SignUpPage

def sign_up(request):
  if(request.method == 'POST'):
    print("!")
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
    return HttpResponseRedirect("/")

  else:
    if(not request.user.is_authenticated):
      print("!!")
      self = SignUpPage.objects.get(slug='sign')
      form = SignUpPage.objects.get(slug='sign').get_form()
      return render(request, 'sign_up/sign_up_page.html', {
        'self': self,
        'form': form,
      })
    else:
      print("!!!")
      return redirect('/')
