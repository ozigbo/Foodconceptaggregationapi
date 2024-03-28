# msal_utils.py

from msal import ConfidentialClientApplication
from django.conf import settings

def get_msal_app():
    print(settings.MSAL_CLIENT_ID)
    print(settings.MSAL_AUTHORITY)
    return ConfidentialClientApplication(
        settings.MSAL_CLIENT_ID,
        authority=settings.MSAL_AUTHORITY,
        client_credential=settings.MSAL_CLIENT_SECRET
    )

def validate_token(access_token):
    #print('access_token')
    #print(access_token)
    msal_app = get_msal_app()
    print(msal_app)
    result = msal_app.acquire_token_silent(scopes=['profile', 'openid', 'email', 'https://graph.microsoft.com/User.Read'],account=None, token=access_token)
    print('result')
    print(result)
    if 'error' in result:
        return False
    else:
        return True

'''
def authenticate_user(request):
    if 'Authorization' in request.headers:
    


        access_token = request.headers['Authorization']
        if validate_token(access_token):
            return True
    return False
'''

