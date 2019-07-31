import requests
import crypt

# Class that handles all endpoints for AWS
class ApiGatewayClient: 
    host = "https://vak4dovce5.execute-api.ap-southeast-1.amazonaws.com/dev"
    version = "v1"
    rootUrl = host + "/api/" + version
    EMAIL = "email",
    MOBILE = "phone_number"


#class that handles user authentication APIs
class AuthClient:

    def __init__(self, apiGateway):
        """
         Initialize this with ApiGatewayClient
        """
        self.apiGateway = apiGateway

    def login(self, clientId, password):
        url = self.apiGateway.rootUrl + "/login"

        json = {
            'username': clientId,
            'password': password
        }
        return requests.post(url, json=json)
        
    def register(self, type, value):
        """
            Register a given user using a mobile number or email \n
            Parameters: \n
            `type`  either email or phone_number \n
            `value` actual email or phone number \n
            Returns 
        """
        url = self.apiGateway.rootUrl + "/register"

        json = {
            'type': type,
            'value': value
        }
        return requests.post(url, json=json)

    def setupPassword(self, clientId, clientSecret, newPassword):
        url = self.apiGateway.rootUrl + "/password-change"

        json = {
            'clientId': clientId,
            'clientSecret': clientSecret,
            'newPassword': newPassword
        }

        return requests.post(url, json=json)

        


