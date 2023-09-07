

from api import HttpClient
from api import TokenCredential
from api import BearerTokenAuth
import logging
from typing import List


class MicrosoftGraphAPI:
    def __init__(self, credential: TokenCredential, max_retries=2, retry_status_codes: List[int] = None, rate_limit=0, rate_limit_period=0, logger: logging.Logger = None, log_requests=False):
        base_url = "https://graph.microsoft.com/v1.0"
        self.api = HttpClient(base_url=base_url, auth=BearerTokenAuth(credential), max_retries=max_retries, retry_status_codes=retry_status_codes,
                              rate_limit=rate_limit, rate_limit_period=rate_limit_period, logger=logger, log_requests=log_requests)

    def find_user_by_mobile_phone(self, mobile_phone) -> List[dict]:
        # Make a GET request to Microsoft Graph API to find a user by mobile phone
        endpoint = f'/users?$filter=mobilePhone eq \'{mobile_phone}\'&$count=true'
        headers = {"ConsistencyLevel": "eventual"}
        response = self.api.get(url=endpoint, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            if 'value' in data and len(data['value']) > 0:
                return data['value']
        return []

    def update_user_password(self, user_id, new_password, force_change_password_next_sign_in: True) -> bool:
        # Make a PATCH request to update the user's password
        endpoint = f'/users/{user_id}'
        payload = {
            "passwordProfile": {
                "forceChangePasswordNextSignIn": force_change_password_next_sign_in,
                "password": new_password
            }
        }
        headers = {"Content-Type": "application/json"}
        response = self.api.patch(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.status_code == 204
