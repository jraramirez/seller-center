import requests


# Class that handles all endpoints for AWS
class ApiGatewayClient:

    EMAIL = "email",
    MOBILE = "phone_number"

    HOST = "https://ktqc7jhi81.execute-api.ap-southeast-1.amazonaws.com/prod"
    VERSION = "v1"
    ORIGIN = "seller-center"
    rootUrl = HOST + "/api/" + VERSION
    headers = {'Request-Origin-App': ORIGIN}


# class that handles user authentication APIs
class AuthClient:

    def __init__(self, apiGateway):
        """
         Initialize this with ApiGatewayClient
        """
        self.apiGateway = apiGateway

    def login(self, username, password):
        """
        Login the user user a user name and password.
        :param username: username may either be phone number, email or cognito id
        :param password: password
        :return:
        """
        url = self.apiGateway.rootUrl + "/login"

        json = {
            'username': username,
            'password': password
        }
        return requests.post(url, headers=self.apiGateway.headers, json=json)

    def register(self, type, value, password):
        """
        Register a given user using a mobile number or email

        :param type:  either `email` or `phone_number`
        :param value: actual email or phone number
        :return:
        """

        url = self.apiGateway.rootUrl + "/register"

        json = {
            'type': type,
            'value': value,
            'password': password
        }
        return requests.post(url, headers=self.apiGateway.headers, json=json)

    def setupPassword(self, clientId, clientSecret, newPassword):
        url = self.apiGateway.rootUrl + "/password-change"

        json = {
            'clientId': clientId,
            'clientSecret': clientSecret,
            'newPassword': newPassword
        }

        return requests.post(url, headers=self.apiGateway.headers, json=json)

    def resend_code(self, clientId):
        '''
        Resend verification code to a registered client id
        :param clientId: can either be unique cognito id, email or phone number
        :return:
        '''

        url = self.apiGateway.rootUrl + "/resend-code"

        json = {
            'clientId': clientId
        }

        return requests.post(url, headers=self.apiGateway.headers, json=json)

    def forgot_password(self, clientId):
        '''
        Send verification code to a registered client id
        :param clientId: can either be unique cognito id, email or phone number
        :return:
        '''
        url=self.apiGateway.rootUrl + "/password-forgot"
        json={
            'clientId': clientId
        }
        return requests.post(url, headers=self.apiGateway.headers, json=json)
