# The simple is just the beginning to open your mind of how everything works in a simple way. "GuiDeLuccaDev"

'''
This script is intended to help in some way to access azure ad 
using a username and password passed through an http.post or using another method in a simplified way.
Do not consider this the only way, or a definitive way.
Feel free to give a good or bad opinion of the code, but remember to be polite.
'''

from msal import PublicClientApplication
import logging, base64

def access_account(token):
    if not token:
        return ""
    else:
        ''' tenantid and appid are Azure AD internal data, 
            it is internal information, do not leave it exposed in the code, 
            it is here to use as an example I advise to have it recorded in a safe.'''
            
        appid = "your_app_id" 
        tenantid = "yout_tenant_id"
        
        ''' The username and password encoding was used base64 but you can use one of your own.'''
        
        auth_decode = base64.b64decode(token).decode()
        username, password = auth_decode.split(":")
        
        if appid and tenantid:
            ''' O scopo você define dentro do Azure AD. '''
            scope = ["User.ReadBasic.All"]

            app = PublicClientApplication(appid, authority="https://login.microsoftonline.com/"+tenantid)
            
            result = None
            
            accounts = app.get_accounts(username=username)
            if accounts:
                logging.info("Account(s) exists in cache, probably with token too. Let's try.")
                result = app.acquire_token_silent(scope, account=accounts[0])

            if not result:
                logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
                result = app.acquire_token_by_username_password(username, password, scopes=scope)
                
                
            ''' If the validation is successful it returns the token, otherwise it prints the errors found. '''
            
            if "access_token" in result:
                return result
            else:
                print(result.get("error"))
                print(result.get("error_description"))
                print(result.get("correlation_id"))  
                if 65001 in result.get("error_codes", []): 
                    print("Visit this to consent:", app.get_authorization_request_url(scope))
                
                return ""
        else:
            return ""
    
token_encoded = base64.b64encode(b'user@domain.onmicrosoft.com:password')
accessed = access_account(token_encoded)
print(accessed)