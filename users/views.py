from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from users.models import Profile
from users.models import Documents
from seller_center.settings.dev import MEDIA_URL

def profile(request):
	return render(request, 'users/profile_page.html', set_user_profile_data(request.user.id))

def profile_edit(request):
	user_id=request.user.id
	if request.method == 'POST':
		User.objects.filter(id=user_id).update(
			first_name=request.POST.get('first-name'),
			last_name=request.POST.get('last-name')
		)

		profile=Profile.objects.filter(id=user_id)[0]
		profile.birthday=request.POST.get('birthday')
		profile.save()

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

		pickup_address_details=profile.pickup_address
		pickup_address_details.street_bldg=request.POST.get('pickup_street_bldg')
		pickup_address_details.country=request.POST.get('pickup_country')
		pickup_address_details.region_state=request.POST.get('pickup_region_state')
		pickup_address_details.city=request.POST.get('pickup_city')
		pickup_address_details.brgy=request.POST.get('pickup_brgy')
		pickup_address_details.postal_code=request.POST.get('pickup_postal_code')
		pickup_address_details.save()

		pickup_contact_details=pickup_address_details.contact_details
		pickup_contact_details.contact_person_name=request.POST.get('pickup_contact_person_name')
		pickup_contact_details.contact_person_phone=request.POST.get('pickup_contact_person_phone')
		pickup_contact_details.contact_person_email=request.POST.get('pickup_contact_person_email')
		pickup_contact_details.save()

		return_address_details=profile.return_address
		return_address_details.street_bldg=request.POST.get('return_street_bldg')
		return_address_details.country=request.POST.get('return_country')
		return_address_details.region_state=request.POST.get('return_region_state')
		return_address_details.city=request.POST.get('return_city')
		return_address_details.brgy=request.POST.get('return_brgy')
		return_address_details.postal_code=request.POST.get('return_postal_code')
		return_address_details.save()

		return_contact_details=return_address_details.contact_details
		return_contact_details.contact_person_name=request.POST.get('return_contact_person_name')
		return_contact_details.contact_person_phone=request.POST.get('return_contact_person_phone')
		return_contact_details.contact_person_email=request.POST.get('return_contact_person_email')
		return_contact_details.save()

		return HttpResponseRedirect("/profile")
	return render(request, 'users/profile_edit_page.html', set_user_profile_data(user_id))

def get_filename_from_url(url):
	url=url[url.rfind('/')+1:]
	return url

def set_user_profile_data(user_id):
	userData=User.objects.filter(id=user_id)[0]

	profileData=Profile.objects.filter(id=user_id)[0]

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
		'return_contact_data': return_contact_data
	}