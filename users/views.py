from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from users.models import Profile, SellerDetails, ShopDetails, BusinessDetails, Documents, Address, AddressContactDetails
from seller_center.settings.dev import MEDIA_URL
import requests

def profile(request):
	return render(request, 'users/profile_page.html', set_user_profile_data(request.user.id))

def profile_edit(request):
	user_id=request.user.id
	data=set_user_profile_data(user_id)

	if not data['enable_fields']:
		return HttpResponseRedirect("/profile")

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
			fn=trim_file_upload(request.FILES['id_front'].name)
			seller_details.upload_id_front.save(str(profile.id) + '/' + str(user_id) + '/'  + fn, request.FILES['id_front'])
			seller_details.upload_id_front_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + fn
		if 'id_back' in request.FILES:
			fn=trim_file_upload(request.FILES['id_back'].name)
			seller_details.upload_id_back.save(str(profile.id) + '/' + str(user_id) + '/'  + fn, request.FILES['id_back'])
			seller_details.upload_id_back_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + fn
		seller_details.email=request.POST.get('email') if request.POST.get('email') != None else ''
		seller_details.phone=request.POST.get('phone') if request.POST.get('phone') != None else ''
		if request.POST.get('terms_conditions') is None:
			seller_details.has_agreed_to_terms=False
		else:
			seller_details.has_agreed_to_terms=True
		seller_details.save()

		shop_details=seller_details.shop_details
		shop_details.shop_name=request.POST.get('shop_name') if request.POST.get('shop_name') != None else ''
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
		business_details.company_name=request.POST.get('company_name') if request.POST.get('company_name') != None else ''
		business_details.business_tin=request.POST.get('business_tin') if request.POST.get('business_tin') != None else ''
		business_details.business_registration_number=request.POST.get('business_registration_number') if request.POST.get('business_registration_number') != None else ''
		business_details.save()

		business_address_details=business_details.business_address
		business_address_details.street_bldg=request.POST.get('business_street_bldg') if request.POST.get('business_registration_number') != None else ''
		business_address_details.country=request.POST.get('business_country')
		business_address_details.region_state=request.POST.get('business_region_state')
		business_address_details.city=request.POST.get('business_city')
		business_address_details.barangay=request.POST.get('business_brgy')
		pc=str(request.POST.get('business_postal_code'))
		if pc.isdigit():
			business_address_details.postal_code=pc
		else:
			business_address_details.postal_code=0
		business_address_details.save()

		if 'bir' in request.FILES:
			docu=Documents.objects.filter(profile_id=user_id, document_type='bir')[0]
			fn=trim_file_upload(request.FILES['bir'].name)
			docu.document.save(str(profile.id) + '/' + str(user_id) + '/'  + fn, request.FILES['bir'])
			Documents.objects.filter(profile_id=user_id, document_type='bir').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + fn)
		if 'dti' in request.FILES:
			docu=Documents.objects.filter(profile_id=user_id, document_type='dti')[0]
			fn=trim_file_upload(request.FILES['dti'].name)
			docu.document.save(str(profile.id) + '/' + str(user_id) + '/'  + fn, request.FILES['dti'])
			Documents.objects.filter(profile_id=user_id, document_type='dti').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + fn)
		if 'sec' in request.FILES:
			docu=Documents.objects.filter(profile_id=user_id, document_type='sec')[0]
			fn=trim_file_upload(request.FILES['sec'].name)
			docu.document.save(str(profile.id) + '/' + str(user_id) + '/'  + fn, request.FILES['sec'])
			Documents.objects.filter(profile_id=user_id, document_type='sec').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + fn)
		if 'permit' in request.FILES:
			docu=Documents.objects.filter(profile_id=user_id, document_type='permit')[0]
			fn=trim_file_upload(request.FILES['permit'].name)
			docu.document.save(str(profile.id) + '/' + str(user_id) + '/'  + fn, request.FILES['permit'])
			Documents.objects.filter(profile_id=user_id, document_type='permit').update(document_url=MEDIA_URL + 'documents/' + str(profile.id) + '/' + str(user_id) + '/'  + fn)

		pickup_address_details=profile.pickup_address
		pickup_address_details.street_bldg=request.POST.get('pickup_street_bldg') if request.POST.get('pickup_street_bldg') != None else ''
		pickup_address_details.country=request.POST.get('pickup_country')
		pickup_address_details.region_state=request.POST.get('pickup_region_state')
		pickup_address_details.city=request.POST.get('pickup_city')
		pickup_address_details.barangay=request.POST.get('pickup_brgy')
		pc=str(request.POST.get('pickup_postal_code'))
		if pc.isdigit():
			pickup_address_details.postal_code=pc
		else:
			pickup_address_details.postal_code=0
		pickup_address_details.save()

		pickup_contact_details=pickup_address_details.contact_details
		pickup_contact_details.contact_person_name=request.POST.get('pickup_contact_person_name') if request.POST.get('pickup_contact_person_name') != None else ''
		pickup_contact_details.contact_person_phone=request.POST.get('pickup_contact_person_phone') if request.POST.get('pickup_contact_person_phone') != None else ''
		pickup_contact_details.contact_person_email=request.POST.get('pickup_contact_person_email') if request.POST.get('pickup_contact_person_email') != None else ''
		pickup_contact_details.save()

		return_address_details=profile.return_address
		return_address_details.street_bldg=request.POST.get('return_street_bldg') if request.POST.get('return_street_bldg') != None else ''
		return_address_details.country=request.POST.get('return_country')
		return_address_details.region_state=request.POST.get('return_region_state')
		return_address_details.city=request.POST.get('return_city')
		return_address_details.barangay=request.POST.get('return_brgy')
		pc=str(request.POST.get('return_postal_code'))
		if pc.isdigit():
			return_address_details.postal_code=pc
		else:
			return_address_details.postal_code=0
		return_address_details.save()

		return_contact_details=return_address_details.contact_details
		return_contact_details.contact_person_name=request.POST.get('return_contact_person_name') if request.POST.get('return_contact_person_name') != None else ''
		return_contact_details.contact_person_phone=request.POST.get('return_contact_person_phone') if request.POST.get('return_contact_person_phone') != None else ''
		return_contact_details.contact_person_email=request.POST.get('return_contact_person_email') if request.POST.get('return_contact_person_email') != None else ''
		return_contact_details.save()

		return HttpResponseRedirect("/profile")

	return render(request, 'users/profile_edit_page.html', data)

def get_filename_from_url(url):
	url=url[url.rfind('/')+1:]
	return url

def set_user_profile_data(user_id):
	userData=User.objects.filter(id=user_id)[0]

	profileData=Profile.objects.filter(id=user_id)[0]

	if profileData.seller_details is None:
		shop_details_data=ShopDetails()
		shop_details_data.save()
		seller_details_data=SellerDetails()
		seller_details_data.shop_details=shop_details_data
		seller_details_data.save()
		profileData.seller_details=seller_details_data
		profileData.save()
	else:
		seller_details_data=profileData.seller_details
	seller_details_data.upload_id_front_url=seller_details_data.upload_id_front_url if seller_details_data.upload_id_front_url else None
	upload_id_front_name=get_filename_from_url(seller_details_data.upload_id_front_url) if seller_details_data.upload_id_front_url else None
	seller_details_data.upload_id_back_url=seller_details_data.upload_id_back_url if seller_details_data.upload_id_back_url else None
	upload_id_back_name=get_filename_from_url(seller_details_data.upload_id_back_url) if seller_details_data.upload_id_back_url else None
	seller_details_data.has_agreed_to_terms='Agreed' if seller_details_data.has_agreed_to_terms else 'Not yet agreed'

	shop_details_data=seller_details_data.shop_details
	shop_details_data.holiday_mode='On' if shop_details_data.holiday_mode else 'Off'

	if profileData.business_details is None:
		business_address_data=Address()
		business_address_data.save()
		business_details_data=BusinessDetails()
		business_details_data.business_address=business_address_data
		business_details_data.save()
		profileData.business_details=business_details_data
		profileData.save()
	else:
		business_details_data=profileData.business_details
	business_address_data=business_details_data.business_address
	street_bldg=business_address_data.street_bldg + ' ' if business_address_data.street_bldg != None else ''
	barangay=business_address_data.barangay + ' ' if business_address_data.barangay != None else ''
	city=business_address_data.city + ' ' if business_address_data.city != None else ''
	region_state=business_address_data.region_state + ' ' if business_address_data.region_state != None else ''
	country=business_address_data.country + ' ' if business_address_data.country != None else ''
	postal_code=str(business_address_data.postal_code) + ' ' if business_address_data.postal_code != None else ''
	business_address=street_bldg + barangay + city + region_state + country + postal_code

	if business_address == '':
		business_address=None

	bir_documents_data=Documents.objects.filter(profile_id=user_id, document_type='bir')

	if len(bir_documents_data) == 0:
		bir_documents_data=Documents()
		bir_documents_data.document_type='bir'
		bir_documents_data.profile_id=profileData.id
		bir_documents_data.save()
	else:
		bir_documents_data=bir_documents_data[0]
	bir=get_filename_from_url(bir_documents_data.document_url) if bir_documents_data.document_url else None
	dti_documents_data=Documents.objects.filter(profile_id=user_id, document_type='dti')
	if len(dti_documents_data) == 0:
		dti_documents_data=Documents()
		dti_documents_data.document_type='dti'
		dti_documents_data.profile_id=profileData.id
		dti_documents_data.save()
	else:
		dti_documents_data=dti_documents_data[0]
	dti=get_filename_from_url(dti_documents_data.document_url) if dti_documents_data.document_url else None
	sec_documents_data=Documents.objects.filter(profile_id=user_id, document_type='sec')
	if len(sec_documents_data) == 0:
		sec_documents_data=Documents()
		sec_documents_data.document_type='sec'
		sec_documents_data.profile_id=profileData.id
		sec_documents_data.save()
	else:
		sec_documents_data=sec_documents_data[0]
	sec=get_filename_from_url(sec_documents_data.document_url) if sec_documents_data.document_url else None
	permit_documents_data=Documents.objects.filter(profile_id=user_id, document_type='permit')
	if len(permit_documents_data) == 0:
		permit_documents_data=Documents()
		permit_documents_data.document_type='permit'
		permit_documents_data.profile_id=profileData.id
		permit_documents_data.save()
	else:
		permit_documents_data=permit_documents_data[0]
	permit=get_filename_from_url(permit_documents_data.document_url) if permit_documents_data.document_url else None

	if profileData.pickup_address is None:
		pickup_contact_data=AddressContactDetails()
		pickup_contact_data.save()
		pickup_address_data=Address()
		pickup_address_data.contact_details=pickup_contact_data
		pickup_address_data.save()
		profileData.pickup_address=pickup_address_data
		profileData.save()
	else:
		pickup_address_data=profileData.pickup_address
	pickup_contact_data=pickup_address_data.contact_details
	street_bldg=pickup_address_data.street_bldg + ' ' if pickup_address_data.street_bldg != None else ''
	barangay=pickup_address_data.barangay + ' ' if pickup_address_data.barangay != None else ''
	city=pickup_address_data.city + ' ' if pickup_address_data.city != None else ''
	region_state=pickup_address_data.region_state + ' ' if pickup_address_data.region_state != None else ''
	country=pickup_address_data.country + ' ' if pickup_address_data.country != None else ''
	postal_code=str(pickup_address_data.postal_code) + ' ' if pickup_address_data.postal_code != None else ''
	pickup_address=street_bldg + barangay + city + region_state + country + postal_code

	if pickup_address == '':
		pickup_address=None

	if profileData.return_address is None:
		return_contact_data=AddressContactDetails()
		return_contact_data.save()
		return_address_data=Address()
		return_address_data.contact_details=return_contact_data
		return_address_data.save()
		profileData.return_address=return_address_data
		profileData.save()
	else:
		return_address_data=profileData.return_address
	return_contact_data=return_address_data.contact_details

	ctr=0
	enable_fields=True
	if seller_details_data.name_on_id:
		ctr+=1
	if seller_details_data.id_type:
		ctr+=1
	if seller_details_data.upload_id_front_url:
		ctr+=1
	if seller_details_data.upload_id_back_url:
		ctr+=1
	if seller_details_data.has_agreed_to_terms == 'Agreed':
		ctr+=1
	if shop_details_data.shop_name:
		ctr+=1
	if pickup_address_data.street_bldg:
		ctr+=1
	if pickup_address_data.country:
		ctr+=1
	if pickup_address_data.region_state:
		ctr+=1
	if pickup_address_data.city:
		ctr+=1
	if pickup_address_data.barangay:
		ctr+=1
	if pickup_address_data.postal_code:
		ctr+=1
	if return_address_data.street_bldg:
		ctr+=1
	if return_address_data.country:
		ctr+=1
	if return_address_data.region_state:
		ctr+=1
	if return_address_data.city:
		ctr+=1
	if return_address_data.barangay:
		ctr+=1
	if return_address_data.postal_code:
		ctr+=1
	if seller_details_data.seller_status == 'Pending for Review' and ctr == 18:
		enable_fields=False

	countries_data=get_countries()
	countries_filtered_data=[]
	for v in countries_data:
		countries_filtered_data.append({'name': v['name']})

	return {
		'profileData': profileData,
		'userData': userData,
		'seller_details_data': seller_details_data,
		'upload_id_front_name': upload_id_front_name,
		'upload_id_back_name': upload_id_back_name,
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
		'pickup_address': pickup_address,
		'return_address_data': return_address_data,
		'return_contact_data': return_contact_data,
		'enable_fields': enable_fields,
		'countries_filtered_data': countries_filtered_data
	}

def trim_file_upload(file):
	file=file.replace(' ', '_')
	file=file.replace('(', '')
	file=file.replace(')', '')
	return file

def get_countries():
	url='https://restcountries.eu/rest/v2/all'
	response=requests.get(url)
	data=response.json()
	return data