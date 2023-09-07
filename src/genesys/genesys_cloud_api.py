

from api import HttpClient
from api import TokenCredential
from api import BearerTokenAuth
import logging
from typing import List
import string
from .region import Region


class GenesysCloudAPI:
    def __init__(self, region: Region,  credential: TokenCredential, max_retries=2, retry_status_codes: List[int] = None, rate_limit=0, rate_limit_period=0, logger: logging.Logger = None, log_requests=False):
        self.api = HttpClient(base_url=region.value.api_url, auth=BearerTokenAuth(credential), max_retries=max_retries, retry_status_codes=retry_status_codes,
                              rate_limit=rate_limit, rate_limit_period=rate_limit_period, logger=logger, log_requests=log_requests)

    def list_user(self) -> List[dict]:
        endpoint = f'/api/v2/users'
        headers = {}
        response = self.api.get(url=endpoint, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            if 'entities' in data and len(data['entities']) > 0:
                return data['entities']
        return []
