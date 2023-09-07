from abc import abstractmethod
from requests.auth import AuthBase
from .token_credential import TokenCredential


class BearerTokenAuth(AuthBase):
    def __init__(self, token_credential: TokenCredential):
        self.token_credential = token_credential

    def __call__(self, r):
        if self.token_credential:
            access_token = self.token_credential.get_access_token()
            if access_token:
                token = access_token.get_token()
                r.headers['Authorization'] = f'Bearer {token}'
        return r
