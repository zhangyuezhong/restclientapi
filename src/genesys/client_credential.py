from api import TokenCredential
from api import AccessToken
from .region import Region
import string
import time
import requests
from requests.auth import HTTPBasicAuth

from api.access_token import AccessToken

class ClientCredential(TokenCredential):
    def __init__(self, region: Region, client_id: string, client_secret: string = None, private_key: string = None, sha1_thumbprint: string = None):
        self.token_url = f"{region.value.auth_url}/oauth/token"
        self.client_id =client_id
        self.client_secret = client_secret
        self.access_token:AccessToken = None
    def get_access_token(self) -> AccessToken:
        if(self.access_token is None):
            self.fetch_token()
        if(self.access_token.is_expired()):
            self.fetch_token()
        return self.access_token
    def fetch_token(self):
        payload = {
            'grant_type': 'client_credentials'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(self.token_url, data=payload, headers=headers, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        response.raise_for_status()
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            expires_in = token_data.get('expires_in')
            self.access_token = AccessToken(token, time.time() + expires_in)
