from abc import ABC, abstractmethod
from .access_token import AccessToken
class TokenCredential:

    @abstractmethod
    def get_access_token() -> AccessToken:
       pass
