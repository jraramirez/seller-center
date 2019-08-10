from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from users.models import Profile
from sign_up.models import SignUpPage
from base.aws_client import AuthClient
from base.aws_client import ApiGatewayClient

import requests


def showErrorMessage(request, message):
    messages.error(request, message)
    self = SignUpPage.objects.get(slug='sign')
    return render(request, 'sign_up/sign_up_page.html', {
        'self': self,
    })


def showInfoMessage(request, message):
    messages.info(request, message)
    self = SignUpPage.objects.get(slug='sign')
    return render(request, 'sign_up/sign_up_page.html', {
        'self': self,
    })


def showWarningMessage(request, message):
    messages.info(request, message)
    self = SignUpPage.objects.get(slug='sign')
    return render(request, 'sign_up/sign_up_page.html', {
        'self': self,
    })


def verify_email(request):
    authClient = AuthClient(ApiGatewayClient())
    print("verify_email")
    email = request.POST['email-address']
    response = authClient.register("email", request.POST['email-address'])

    json = response.json()
    print("Verify email response: status: ", response.status_code, response.json())

    if (response.status_code == 200):

        messages.info(request, "An activation link has been sent to email")
        clientId = json['clientId']
        clientSecret = json['clientSecret']

        self = SignUpPage.objects.get(slug='sign')
        return render(request, 'sign_up/sign_up_page.html', {
            'self': self,
            'username': email,
            'clientId': clientId,
            'clientSecret': clientSecret,
            'visibility': "show active"
        })
    elif (response.status_code == 409 and json['code'] == 'ALREADY_EXISTS'):
        # resend verification code here
        pass
    else:
        return showErrorMessage(request, json['code'])


def continueSignup(request):
    if (request.POST['reg-type'] == 'phone'):
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
        # call api here
        login(request, new_user)
        HttpResponseRedirect('/')
    else:
        email = request.POST['email-address']
        password = request.POST['password']
        reenterPassword = request.POST['password-reenter']
        clientId = request.POST['clientId']
        clientSecret = request.POST['clientSecret']

        if password != reenterPassword:
            return showErrorMessage(request, "password must be the same")

        authClient = AuthClient(ApiGatewayClient())
        # login account to get token for password setup
        loginResponse = authClient.login(clientId, clientSecret)

        jsonLogin = loginResponse.json()
        print("code %s - jsonLogin %s", loginResponse.status_code, jsonLogin)

        # checker for user is not confirmed
        if (loginResponse.status_code == 401 and jsonLogin['code'] == 'UNVERIFIED_LOGIN'):
            messages.error(request, "Please activate your email first")
            self = SignUpPage.objects.get(slug='sign')
            return render(request, 'sign_up/sign_up_page.html', {
                'self': self,
                'username': email,
                'clientId': clientId,
                'clientSecret': clientSecret,
                'visibility': "show active"
            })

        # TODO: validate inpunt on client side first if validateInput(email, password, reenterPassword)

        # call api here if success create a user else show necessary errors
        authClient = AuthClient(ApiGatewayClient())

        response = authClient.register("email", request.POST['email-address'])
        # TODO: Add button to resend verification link

        json = response.json()
        print(response.json())
        if (response.status_code == 200):
            json = response.json()
            response = authClient.login(json['clientId'], json['clientSecret'])

            if (response.status_code == 200):
                json = response.json()
                if (json['message'] == "User is not confirmed."):
                    return showErrorMessage(request, json['message'])

            # print("Status: %s - %s",response.status_code, response.json())

            # response = authClient.setupPassword(json['clientId'], json['clientSecret'], request.POST['password'])
            # print(response.json())
            # user = User.objects.create_user(
            #   username=request.POST['email-address'],
            #   email=request.POST['email-address'],
            #   password=request.POST['password']
            # )
            # group = Group.objects.get(name='Seller')
            # user.groups.add(group)
            # new_user = authenticate(
            #   username=request.POST['email-address'],
            #   password=request.POST['password'],
            # )

            # login success
            # ogin(request, new_user)
            return render(request, 'sign_up/sign_up_page_landing.html', {
                'request': request,
            })
        else:
            return showErrorMessage(request, json['details'])


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                HttpResponseRedirect('/')
            else:
                # Return an 'invalid login' error message.
                messages.error(request, 'username or password not correct')
                return HttpResponseRedirect('/')
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')

def sign_up(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if not validate_email(email=username):
            messages.error(request, "Please enter a valid email address.")
            return HttpResponseRedirect('sign_up/sign_up_page.html')

        if password != confirm_password:
            messages.error(request, 'Password does not match')
            return HttpResponseRedirect('sign_up/sign_up_page.html')

        authClient = AuthClient(ApiGatewayClient())

        response = authClient.register("email", username, password)

        json = response.json()
        print("%s code", response.status_code)
        print(response.json())
        if response.status_code == 200:
            print("success")
            return render(request, 'sign_up/confirm_link.html', {
                'request': request,
                'email': username
            })
        else:
            messages.error(request, json['details'])
            return HttpResponseRedirect('sign_up/sign_up_page.html')

    else:
        return render(request, 'sign_up/sign_up_page.html')


def signUpWithEmail(request):
    username = request.POST['username']
    password = request.POST['password']
    confirmPassword = request.POST['confirm-password']

    authClient = AuthClient(ApiGatewayClient())

    response = authClient.register("email", username)

    json = response.json()
    print(response.json())
    if (response.status_code == 200):
        json = response.json()
        response = authClient.login(json['clientId'], json['clientSecret'])
        print(response)

    self = SignUpPage.objects.get(slug='sign')
    if (not request.user.is_authenticated):
        return render(request, 'sign_up/sign_up_page.html', {
            'self': self,
        })


def reset_password(request):
    if (request.method == 'POST'):
        if (request.POST['reg-type'] == 'phone'):
            return render(request, 'signup/reset_password_page.html', {

            })
        if (request.POST['reg-type'] == 'email'):
            return render(request, 'signup/reset_password_page.html', {

            })

def confirm_link(request):
    return render(request, 'sign_up/confirm_link.html')


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False