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
    dtiDocument = None
    # secDocument = None
    # permitDocument = None
    # if(request.FILES['dti']):
    #   dtiDocument = request.FILES['dti']
    # if(request.FILES['sec']):
    #   secDocument = request.FILES['sec']
    # if(request.FILES['permit']):
    #   permitDocument = request.FILES['permit']
    # p = Profile()
    # p.user_id = request.user.id
    # p.dti = dtiDocument.file
    # p.save()
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