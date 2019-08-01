from base.aws_client import AuthClient
from base.aws_client import ApiGatewayClient
from django.contrib.auth.models import User, Group

class AwsBackend:
    def authenticate(self, request, username=None, password=None):
        print('using custom authenticator')
        authClient = AuthClient(ApiGatewayClient())

        loginResponse = authClient.login(username, password)

        json = loginResponse.json()

        statusCode = loginResponse.status_code

        if (statusCode == 200):
            try:
                user = User.objects.get(username=username)
                print('user: %s', user)
                return user
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=username, password=password)
                group = Group.objects.get(name='Seller')
                user.groups.add(group)
                return user

        return None

    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None