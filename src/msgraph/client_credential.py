from api import TokenCredential
from api import JwtSigner
from api import AccessToken
import string
import time
import requests

from api.access_token import AccessToken

class ClientCredential(TokenCredential):
    def __init__(self, tenant_id: string, client_id: string, client_secret: string = None, private_key: string = None, sha1_thumbprint: string = None):
        self.token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        self.tenant_id = tenant_id
        self.client_id =client_id
        self.client_secret = client_secret
        self.private_key = private_key
        self.sha1_thumbprint = sha1_thumbprint
        self.signer = None
        if (self.client_secret is None and private_key is not None and sha1_thumbprint is not None):
            self.signer = JwtSigner(private_key, "RS256", sha1_thumbprint=sha1_thumbprint, headers={"typ": "JWT"})
        self.access_token:AccessToken = None
    def get_access_token(self) -> AccessToken:
        if(self.access_token is None):
            self.fetch_token()
        if(self.access_token.is_expired()):
            self.fetch_token()
        return self.access_token
    
    def fetch_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'scope': "https://graph.microsoft.com/.default",
            'client_id': self.client_id
        }
        if self.client_secret:
            payload["client_secret"] = self.client_secret

        if (self.client_secret is None and self.signer is not None):
            audience = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            client_assertion = self.signer.create_normal_assertion(
                audience=audience, issuer=self.client_id, subject=self.client_id)
            payload["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
            payload["client_assertion"] = client_assertion

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(self.token_url, data=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            expires_in = token_data.get('expires_in')
            self.access_token = AccessToken(token, time.time() + expires_in)
