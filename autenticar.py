# Código simplificado para entender como tudo funciona de uma forma simples. "GuiDeLuccaDev"
# Não é a melhor maneira, não é o mais robusto, o mais seguro mas é uma forma defazer.

import jwt
from jwt.algorithms import RSAAlgorithm
import json
import requests

id_diretorio = "seu ID do diretorio" 
    # Você pode encontr-lo dentro Azure Active Directory 
    # No menu "Visão Geral" ou no menu "Propriedades"
    # Ou no próprio token recebido para validar
id_aplicativo = "seu ID do aplicativo"
    # Você pode encontra-lo no menu "Registro de Aplicativo"
    # Selecione o aplicativo desejado e procure "ID do aplicativo (cliente)"

class Autenticar():
    def __init__(self, token) -> None:
        self.token_id = token["id_token"]
        self.claims = token["id_token_claims"]
        self.aud = self.claims["aud"]
        
    def is_valid(self):
        response = requests.get("https://login.microsoftonline.com/"+id_diretorio+
                                "/discovery/v2.0/keys?appid="+id_aplicativo).json()
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

token = ""
Autenticar(token)

# Um exemplo de como pode parecer um token gerado ao acessar o Azure AD.
# Se o token vier criptografado e você descriptografa-lo terá esse mesmo resultado.

exemplo_token = {
    "token_type": "Bearer",
    "scope": "openid profile User.ReadBasic.All email",
    "expires_in": 3599,
    "ext_expires_in": 3599,
    "access_token": "xxxxx",
    "refresh_token": "yyyyy",
    "id_token": "zzzzz",
    "client_info": "wwwww",
    "id_token_claims": {
        "aud": "123xxx",
        "iss": "https://login.microsoftonline.com/xxx123/v2.0",
        "iat": 1605707120,
        "nbf": 1605707120,
        "exp": 1605711020,
        "aio": "ATQAy/xxx123",
        "name": "Nome do usuario",
        "oid": "xxx123",
        "preferred_username": "nome do usuario preferido",
        "rh": "xxx123",
        "sub": "xxx123",
        "tid": "xxx123",
        "uti": "xxx123",
        "ver": "2.0"
    }
}
