from base.aws_client import AuthClient
from base.aws_client import ApiGatewayClient
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError


class AwsBackend:
    def authenticate(self, request, username=None, password=None):
        print('using custom authenticator')
        authClient = AuthClient(ApiGatewayClient())

        loginResponse = authClient.login(username, password)

        json = loginResponse.json()

        status_code = loginResponse.status_code


        if status_code == 401 and json['code'] == 'UNVERIFIED_LOGIN':
            raise ValidationError(message="User not yet verified.", code=401)

        if status_code == 403 and json['code'] == 'UNAUTHORIZED_ORIGIN':
            raise ValidationError(message="Unauthorized access.", code=401)


        if status_code == 200:
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User.objects.create_user(username=username, password=password)
                group = Group.objects.get(name='Seller')
                user.groups.add(group)
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
