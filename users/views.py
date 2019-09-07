from django.shortcuts import render

from django.contrib.auth.models import User
from users.models import Profile
from users.models import Documents

from wagtail.documents.models import get_document_model
from wagtail.documents.forms import get_document_form

from seller_center.settings.dev import MEDIA_URL

def profile(request):
	return render(request, 'users/profile_page.html', set_user_profile_data(request.user.id))

def profile_edit(request):
	if request.method == 'POST':
		user_id=request.user.id
		print(request.POST.get('company_name'))
		User.objects.filter(id=user_id).update(
			first_name=request.POST.get('first-name'),
			last_name=request.POST.get('last-name')
		)

		profile=Profile.objects.filter(id=user_id)[0]

		seller_details=profile.seller_details
		seller_details.name_on_id=request.POST.get('last-name') + ', ' + request.POST.get('first-name')
		seller_details.id_type=request.POST.get('id_type')
		if 'id_front' in request.FILES:
			seller_details.upload_id_front_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + request.FILES['id_front'].name
		if 'id_back' in request.FILES:
			seller_details.upload_id_back_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + request.FILES['id_back'].name
		seller_details.email=request.POST.get('email')
		seller_details.phone=request.POST.get('phone')
		if request.POST.get('terms_conditions') is None:
			seller_details.has_agreed_to_terms=False
		else:
			seller_details.has_agreed_to_terms=True
		seller_details.save()

		shop_details=seller_details.shop_details
		shop_details.shop_name=request.POST.get('shop_name')
		if request.POST.get('holiday') is None:
			shop_details.holiday_mode=False
		else:
			shop_details.holiday_mode=True
		if request.POST.get('holiday_start_date'):
			shop_details.start_date=request.POST.get('holiday_start_date')
		else:
			shop_details.start_date=None
		if request.POST.get('holiday_start_time'):
			shop_details.start_time=request.POST.get('holiday_start_time')
		else:
			shop_details.start_time=None
		if request.POST.get('holiday_end_date'):
			shop_details.end_date=request.POST.get('holiday_end_date')
		else:
			shop_details.end_date=None
		if request.POST.get('holiday_end_time'):
			shop_details.end_time=request.POST.get('holiday_end_time')
		else:
			shop_details.end_time=None
		shop_details.save()

		business_details=profile.business_details
		business_details.company_name=request.POST.get('company_name')
		business_details.business_tin=request.POST.get('business_tin')
		business_details.business_registration_number=request.POST.get('business_registration_number')
		business_details.save()

		business_address_details=business_details.business_address
		business_address_details.street_bldg=request.POST.get('business_street_bldg')
		business_address_details.country=request.POST.get('business_country')
		business_address_details.region_state=request.POST.get('business_region_state')
		business_address_details.city=request.POST.get('business_city')
		business_address_details.brgy=request.POST.get('business_brgy')
		business_address_details.postal_code=request.POST.get('business_postal_code')
		business_address_details.save()

		if 'bir' in request.FILES:
			Documents.objects.filter(profile_id=user_id, document_type='bir').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + request.FILES['bir'].name)
		if 'dti' in request.FILES:
			Documents.objects.filter(profile_id=user_id, document_type='dti').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + request.FILES['dti'].name)
		if 'sec' in request.FILES:
			Documents.objects.filter(profile_id=user_id, document_type='sec').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + request.FILES['sec'].name)
		if 'permit' in request.FILES:
			Documents.objects.filter(profile_id=user_id, document_type='permit').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + request.FILES['permit'].name)

		print(request.POST.get('business_street_bldg'))
		# p.user_id = user_id
		# p.dti_id = profileData.dti_id
		# p.sec_id = profileData.sec_id
		# p.permit_id = profileData.permit_id
		
		#   p.dti_id = dtiDocument.id

		# if('sec' in request.FILES.keys()):
		#   secDocument = Document.objects.create(
		#     file=request.FILES['sec'],
		#     title=request.FILES['sec'].name
		#   )
		#   p.sec_id = secDocument.id

		# if('permit' in request.FILES.keys()):
		#   permitDocument = Document.objects.create(
		#     file=request.FILES['permit'],
		#     title=request.FILES['permit'].name
		#   )
		#   p.permit_id = permitDocument.id
		# p.save()
		
		# for i in range(0,8):
		#   if(request.POST.get('address-'+str(i)+'-name')):
		#     if(Address.objects.filter(profile_id=user_id).filter(index=i)):
		#       Address.objects.filter(profile_id=user_id).filter(index=i).update(
		#         name = request.POST.get('address-'+str(i)+'-name'),
		#       )
		#     else:
		#       a = Address(
		#         profile_id = user_id,
		#         name = request.POST.get('address-'+str(i)+'-name'),
		#         index = i
		#       )
		#       a.save()

		userData = User.objects.filter(id=user_id)[0]
		profileData = Profile.objects.filter(id=user_id)[0]
		# addresses = Address.objects.filter(profile_id=request.user.id)
		# Document = get_document_model()
		# dtiDocument = Document.objects.filter(id=profileData.dti_id)[0] if len(Document.objects.filter(id=profileData.dti_id)) else None
		# secDocument = Document.objects.filter(id=profileData.sec_id)[0] if len(Document.objects.filter(id=profileData.sec_id)) else None
		# permitDocument = Document.objects.filter(id=profileData.permit_id)[0] if len(Document.objects.filter(id=profileData.permit_id)) else None
		return render(request, 'users/profile_page.html', {
			'profileData': profileData,
			'userData': userData,
			# 'dtiDocument': dtiDocument,
			# 'secDocument': secDocument,
			# 'permitDocument': permitDocument,
			# 'addresses': addresses
		})
	return render(request, 'users/profile_edit_page.html', set_user_profile_data(request.user.id))

def get_filename_from_url(url):
	url=url[url.rfind('/')+1:]
	return url

def set_user_profile_data(user_id):
	userData = User.objects.filter(id=user_id)[0]

	profileData = Profile.objects.filter(id=user_id)[0]

	seller_details_data=profileData.seller_details
	seller_details_data.upload_id_front_url=get_filename_from_url(seller_details_data.upload_id_front_url)
	seller_details_data.upload_id_back_url=get_filename_from_url(seller_details_data.upload_id_back_url)
	seller_details_data.has_agreed_to_terms='Agreed' if seller_details_data.has_agreed_to_terms else 'Not yet agreed'
	shop_details_data=seller_details_data.shop_details
	shop_details_data.holiday_mode='On' if shop_details_data.holiday_mode else 'Off'

	business_details_data=profileData.business_details
	business_address_data=business_details_data.business_address
	business_address=business_address_data.street_bldg + ' ' + business_address_data.brgy + ' ' + business_address_data.city + ' ' + business_address_data.region_state + ' ' + business_address_data.country + ' ' + str(business_address_data.postal_code)

	bir_documents_data=Documents.objects.filter(profile_id=user_id, document_type='bir')[0]
	bir=get_filename_from_url(bir_documents_data.document_url)
	dti_documents_data=Documents.objects.filter(profile_id=user_id, document_type='dti')[0]
	dti=get_filename_from_url(dti_documents_data.document_url)
	sec_documents_data=Documents.objects.filter(profile_id=user_id, document_type='sec')[0]
	sec=get_filename_from_url(sec_documents_data.document_url)
	permit_documents_data=Documents.objects.filter(profile_id=user_id, document_type='permit')[0]
	permit=get_filename_from_url(permit_documents_data.document_url)

	pickup_address_data=profileData.pickup_address
	pickup_contact_data=pickup_address_data.contact_details

	return_address_data=profileData.return_address
	return_contact_data=return_address_data.contact_details

	return {
		'profileData': profileData,
		'userData': userData,
		'seller_details_data': seller_details_data,
		'shop_details_data': shop_details_data,
		'business_details_data': business_details_data,
		'business_address_data': business_address_data,
		'business_address': business_address,
		'bir_documents_data': bir_documents_data,
		'bir': bir,
		'dti_documents_data': dti_documents_data,
		'dti': dti,
		'sec_documents_data': sec_documents_data,
		'sec': sec,
		'permit_documents_data': permit_documents_data,
		'permit': permit,
		'pickup_address_data': pickup_address_data,
		'pickup_contact_data': pickup_contact_data,
		'return_address_data': return_address_data,
		'return_contact_data': return_contact_data,
	}