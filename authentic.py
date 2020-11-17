# The simple is just the beginning to open your mind of how everything works in a simple way.

'''
This script is intended to show a "way to validate" 
the token generated for that Azure AD, take into account 
that the idea is to simplify and not create a robust and secure script.
'''

import jwt
from jwt.algorithms import RSAAlgorithm
import json
import requests

tenant_id = "your_tenant_id"
app_id = "yout_app_id"

class Authentic():
    def __init__(self, token) -> None:
        self.token_id = token["id_token"]
        self.claims = token["id_token_claims"]
        self.aud = self.claims["aud"]
        
    '''
    This method uses microsoft discovery to validate the data 
    that is passed through the token, having to return exactly 
    the same information for later comparison, 
    taking into account that whoever passed the token did not have 
    the tenantid and the appid, if the data is not correct returns invalid.        
    '''
    def is_valid(self):
        response = requests.get("https://login.microsoftonline.com/"+tenant_id+"/discovery/v2.0/keys?appid="+app_id).json()
        jwks = None
        if response:
            if "error" in response:
                return response["error"]
            else:
                jwks = json.dumps(response["keys"][0])
                self.rsa_key = RSAAlgorithm.from_jwk(jwks)
        
        if jwks:
            try:
                decoded = jwt.decode(self.token_id, self.rsa_key, algorithms='RS256', audience=self.aud)
                result = decoded==self.claims
            except Exception as er:
                result = er
            return result
        else:
            return {"error": "RSA Key not found."}

Authentic()