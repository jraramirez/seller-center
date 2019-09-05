from django.shortcuts import render

from django.contrib.auth.models import User
from users.models import Profile
from users.models import Address

from wagtail.documents.models import get_document_model
from wagtail.documents.forms import get_document_form

def profile(request):
  userData = User.objects.filter(id=request.user.id)[0]
  profileData = Profile.objects.filter(id=request.user.id)[0]
  seller_details_data=profileData.seller_details
  shop_details_data=seller_details_data.shop_details
  front_name=seller_details_data.upload_id_front_url
  front_name=front_name[front_name.rfind('/')+1:]
  seller_details_data.upload_id_front_url=front_name
  back_name=seller_details_data.upload_id_back_url
  back_name=back_name[back_name.rfind('/')+1:]
  seller_details_data.upload_id_back_url=back_name
  seller_details_data.has_agreed_to_terms='Agreed' if seller_details_data.has_agreed_to_terms else 'Not yet agreed'
  shop_details_data.holiday_mode='On' if shop_details_data.holiday_mode else 'Off'
  # addresses = Address.objects.filter(profile_id=request.user.id)
  # Document = get_document_model()
  # dtiDocument = Document.objects.filter(id=profileData.dti_id)[0] if len(Document.objects.filter(id=profileData.dti_id)) else None
  # secDocument = Document.objects.filter(id=profileData.sec_id)[0] if len(Document.objects.filter(id=profileData.sec_id)) else None
  # permitDocument = Document.objects.filter(id=profileData.permit_id)[0] if len(Document.objects.filter(id=profileData.permit_id)) else None
  return render(request, 'users/profile_page.html', {
    'profileData': profileData,
    'userData': userData,
    'seller_details_data': seller_details_data,
    'shop_details_data': shop_details_data,
    # 'dtiDocument': dtiDocument,
    # 'secDocument': secDocument,
    # 'permitDocument': permitDocument,
    # 'addresses': addresses
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
    for i in range(0,8):
      if(request.POST.get('address-'+str(i)+'-name')):
        if(Address.objects.filter(profile_id=request.user.id).filter(index=i)):
          Address.objects.filter(profile_id=request.user.id).filter(index=i).update(
            name = request.POST.get('address-'+str(i)+'-name'),
          )
        else:
          a = Address(
            profile_id = request.user.id,
            name = request.POST.get('address-'+str(i)+'-name'),
            index = i
          )
          a.save()

    userData = User.objects.filter(id=request.user.id)[0]
    profileData = Profile.objects.filter(id=request.user.id)[0]
    addresses = Address.objects.filter(profile_id=request.user.id)
    Document = get_document_model()
    dtiDocument = Document.objects.filter(id=profileData.dti_id)[0] if len(Document.objects.filter(id=profileData.dti_id)) else None
    secDocument = Document.objects.filter(id=profileData.sec_id)[0] if len(Document.objects.filter(id=profileData.sec_id)) else None
    permitDocument = Document.objects.filter(id=profileData.permit_id)[0] if len(Document.objects.filter(id=profileData.permit_id)) else None
    return render(request, 'users/profile_page.html', {
      'profileData': profileData,
      'userData': userData,
      'dtiDocument': dtiDocument,
      'secDocument': secDocument,
      'permitDocument': permitDocument,
      'addresses': addresses
    })

  userData = User.objects.filter(id=request.user.id)[0]
  profileData = Profile.objects.filter(id=request.user.id)[0]
  
  addresses = [{}]*7
  profileAddresses = Address.objects.filter(profile_id=request.user.id)
  if(profileAddresses.count()):
    for i, a in zip(range(0, len(profileAddresses)), profileAddresses):
      addresses[i] = a
    for i in range(len(profileAddresses), 7):
      addresses.append({})
  else:
    for i, a in zip(range(0,7), addresses):
      addresses[i] = {}
  
  return render(request, 'users/profile_edit_page.html', {
    'profileData': profileData,
    'userData': userData,
    'addresses': addresses
  })