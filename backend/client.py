"""Small synchronous PocketBase client. Worker credentials never go to the browser."""
import json
import urllib.error
import urllib.request


class ApiError(Exception):
    def __init__(self, status, message, details=None):
        super().__init__(message)
        self.status = status
        self.details = details or {}


class Client:
    def __init__(self, url='http://127.0.0.1:8090', token=''):
        self.url = url.rstrip('/')
        self.token = token

    def request(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = self.token
        request = urllib.request.Request(self.url + path, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            with error:
                payload = json.load(error)
            # Avoid including request bodies/passwords/tokens in diagnostic output.
            raise ApiError(error.code, payload.get('message', 'API request failed'), payload.get('data')) from None

    def login(self, username, password, collection='accounts'):
        result = self.request('POST', f'/api/collections/{collection}/auth-with-password', {'identity': username, 'password': password})
        self.token = result['token']
        return result['record']
