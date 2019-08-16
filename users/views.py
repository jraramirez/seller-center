from django.shortcuts import render

from django.contrib.auth.models import User
from users.models import Profile

from wagtail.documents.models import get_document_model
from wagtail.documents.forms import get_document_form

def profile(request):
  userData = User.objects.filter(id=request.user.id)[0]
  profileData = Profile.objects.filter(id=request.user.id)[0]
  Document = get_document_model()
  dtiDocument = Document.objects.filter(id=profileData.dti_id)[0] if len(Document.objects.filter(id=profileData.dti_id)) else None
  secDocument = Document.objects.filter(id=profileData.sec_id)[0] if len(Document.objects.filter(id=profileData.sec_id)) else None
  permitDocument = Document.objects.filter(id=profileData.permit_id)[0] if len(Document.objects.filter(id=profileData.permit_id)) else None
  return render(request, 'users/profile_page.html', {
    'profileData': profileData,
    'userData': userData,
    'dtiDocument': dtiDocument,
    'secDocument': secDocument,
    'permitDocument': permitDocument
  })

def profile_edit(request):
  if(request.method == "POST"):
    Document = get_document_model()
    profileData = Profile.objects.filter(id=request.user.id)[0]
    p = Profile()
    p.user_id = request.user.id
    p.dti_id = profileData.dti_id
    p.sec_id = profileData.sec_id
    p.permit_id = profileData.permit_id

    if('dti' in request.FILES.keys()):
      dtiDocument = Document.objects.create(
        file=request.FILES['dti'],
        title=request.FILES['dti'].name
      )
      p.dti_id = dtiDocument.id

    if('sec' in request.FILES.keys()):
      secDocument = Document.objects.create(
        file=request.FILES['sec'],
        title=request.FILES['sec'].name
      )
      p.sec_id = secDocument.id

    if('permit' in request.FILES.keys()):
      permitDocument = Document.objects.create(
        file=request.FILES['permit'],
        title=request.FILES['permit'].name
      )
      p.permit_id = permitDocument.id
    p.save()
    User.objects.filter(id=request.user.id).update(
      first_name = request.POST.get('first-name'),
      last_name = request.POST.get('last-name')
    )
    userData = User.objects.filter(id=request.user.id)[0]
    profileData = Profile.objects.filter(id=request.user.id)[0]
    Document = get_document_model()
    dtiDocument = Document.objects.filter(id=profileData.dti_id)[0] if len(Document.objects.filter(id=profileData.dti_id)) else None
    secDocument = Document.objects.filter(id=profileData.sec_id)[0] if len(Document.objects.filter(id=profileData.sec_id)) else None
    permitDocument = Document.objects.filter(id=profileData.permit_id)[0] if len(Document.objects.filter(id=profileData.permit_id)) else None
    return render(request, 'users/profile_page.html', {
      'profileData': profileData,
      'userData': userData,
      'dtiDocument': dtiDocument,
      'secDocument': secDocument,
      'permitDocument': permitDocument
    })

  userData = User.objects.filter(id=request.user.id)[0]
  profileData = Profile.objects.filter(id=request.user.id)[0]
  return render(request, 'users/profile_edit_page.html', {
    'profileData': profileData,
    'userData': userData,
  })