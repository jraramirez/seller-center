from base.aws_client import AuthClient
from base.aws_client import ApiGatewayClient
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError

from wagtail.core.models import Collection, GroupCollectionPermission
from django.contrib.auth.models import Group, Permission

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
                # Create a new user.
                user = User.objects.create_user(username=username, password=password)
                Collection.get_first_root_node().add_child(name=str(request.user.id))
                newGroup, created = Group.objects.get_or_create(name=str(request.user.id))
                group = Group.objects.get(name='Seller')
                user.groups.add(group)
                user.groups.add(newGroup)
                access_admin = Permission.objects.get(codename='access_admin')
                newGroup.permissions.add(access_admin)
                GroupCollectionPermission.objects.create(
                    group=newGroup,
                    collection=Collection.objects.get(name=str(request.user.id)),
                    permission=Permission.objects.get(codename='add_image')
                )
  

                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def setupUserPermissions(request):
  userData = User.objects.filter(id=request.user.id)[0]
  Collection.get_first_root_node().add_child(name=str(request.user.id))
  newGroup, created = Group.objects.get_or_create(name=str(request.user.id))
  newGroup.user_set.add(userData)
  group = Group.objects.get(name='Seller')
  group.user_set.add(userData)
  access_admin = Permission.objects.get(codename='access_admin')
  newGroup.permissions.add(access_admin)
  GroupCollectionPermission.objects.create(
    group=newGroup,
    collection=Collection.objects.get(name=str(request.user.id)),
    permission=Permission.objects.get(codename='add_image')
  )
  