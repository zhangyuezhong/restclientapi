
import logging
import string
import requests
from requests.auth import AuthBase
import time
import threading
import http.cookiejar
from typing import List


class HttpClient:
    def __init__(self, base_url: string, auth: AuthBase, max_retries=0, retry_status_codes: List[int] = None, rate_limit=0, rate_limit_period=0, logger: logging.Logger = None, log_requests=False):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = auth
        self.session.cookies = http.cookiejar.CookieJar()
        self.max_retries = max_retries
        self.retry_status_codes = retry_status_codes if retry_status_codes is not None else []

        # Validate that rate_limit is greater than or equal to 0
        if rate_limit < 0:
            raise ValueError("rate_limit must be greater than or equal to 0")
        self.rate_limit = rate_limit

        # Validate that rate_limit_period is greater than or equal to 0
        if rate_limit_period < 0:
            raise ValueError(
                "rate_limit_period must be greater than or equal to 0")
        self.rate_limit_period = rate_limit_period
        self.last_request_time = 0

        self.lock = threading.Lock() if self.rate_limit > 0 and self.rate_limit_period > 0 else None
        # Create a lock specifically for updating last_request_time
        self.last_request_time_lock = threading.Lock(
        ) if self.rate_limit > 0 and self.rate_limit_period > 0 else None

        # Initialize the logger for the ClientAPI class, or use the provided logger
        self.logger = logger if logger is not None else logging.getLogger(__name__)

        # Control whether requests should be logged or not
        self.log_requests = log_requests

    def _handle_response(self, response, retry_count):
        if response.status_code in self.retry_status_codes and retry_count < self.max_retries:
            return True

        if response.status_code == 401 and retry_count < self.max_retries:
            self.session.auth.fetch_token()
            return True

        return False

    def _make_request(self, method, url, data=None, retry_count=0, headers=None):
        if headers is None:
            headers = {}

        if self.lock:
            with self.lock:
                current_time = time.time()
                time_elapsed = current_time - self.last_request_time
                min_sleep_duration = self.rate_limit_period / self.rate_limit
                if time_elapsed < min_sleep_duration:
                    time.sleep(min_sleep_duration - time_elapsed)

        response = self.session.request(
            method, url, json=data, headers=headers)
        # Use a separate lock to update last_request_time after the request
        if self.last_request_time_lock:
            with self.last_request_time_lock:
                self.last_request_time = time.time()

        if self._handle_response(response, retry_count):
            return self._make_request(method, url, data, retry_count + 1, headers=headers)

        # Log the request and response conditionally based on log_requests
        if self.log_requests:
            self._log_request_response(method, url, response)

        return response

    def _log_request_response(self, method, url, response):
        if self.logger is not None:
            self.logger.debug(
                f'Request: {method} {url}, Status Code: {response.status_code}')
            self.logger.debug(f'Response Content: {response.text}')

    # Add GET method
    def get(self, url, headers=None):
        return self._make_request('GET', self.base_url + url, headers=headers)

    # Add PUT method
    def put(self, url, data=None, headers=None):
        return self._make_request('PUT', self.base_url + url, data=data, headers=headers)

    # Add POST method
    def post(self, url, data=None, headers=None):
        return self._make_request('POST', self.base_url + url, data=data, headers=headers)

    # Add PATCH method
    def patch(self, url, data=None, headers=None):
        return self._make_request('PATCH', self.base_url + url, data=data, headers=headers)

    # Add DELETE method
    def delete(self, url, headers=None):
        return self._make_request('DELETE', self.base_url + url, headers=headers)
