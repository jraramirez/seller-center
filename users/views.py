from django.shortcuts import render

from django.contrib.auth.models import User
from users.models import Profile

def profile(request):
  userData = User.objects.filter(id=request.user.id)[0]
  profileData = Profile.objects.filter(id=request.user.id)[0]
  return render(request, 'users/profile_page.html', {
    'profileData': profileData,
    'userData': userData,
  })

def profile_edit(request):
  if(request.method == "POST"):
    User.objects.filter(id=request.user.id).update(
      first_name = request.POST.get('first-name'),
      last_name = request.POST.get('last-name'),
    )
    userData = User.objects.filter(id=request.user.id)[0]
    profileData = Profile.objects.filter(id=request.user.id)[0]
    return render(request, 'users/profile_page.html', {
      'profileData': profileData,
      'userData': userData,
    })

  userData = User.objects.filter(id=request.user.id)[0]
  profileData = Profile.objects.filter(id=request.user.id)[0]
  return render(request, 'users/profile_edit_page.html', {
    'profileData': profileData,
    'userData': userData,
  })