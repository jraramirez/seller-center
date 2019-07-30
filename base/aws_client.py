import requests

# Class that handles all endpoints for AWS
class ApiGatewayClient: 
    host = "https://vak4dovce5.execute-api.ap-southeast-1.amazonaws.com/dev"
    version = "v1"
    rootUrl = host + "/api/" + version


#class that handles user authentication APIs
class AuthClient:

    def __init__(self, apiGateway):
        """
         Initialize this with ApiGatewayClient
        """
        self.apiGateway = apiGateway

    def register(self, type, value, result):
        """
            Register a given user using a mobile number or email \n
            Parameters: \n
            `type`  either RegistrationType.EMAIL or RegistrationType.MOBILE \n
            `value` 
        """
        url = self.apiGateway.rootUrl + "/register"

        json = {
            'type': type,
            'value': value
        }
        response = requests.post(url, json=json)

        result(response)




class RegistrationType(Enum):
    EMAIL = "email",
    MOBILE = "phone_number"

        


