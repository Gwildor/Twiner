import base64
import urllib

import requests


class Api:

    def __init__(self, consumer_key='', consumer_secret='', bearer_token=''):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = bearer_token
        self.encode_credentials()

        if not self.bearer_token:
            self.request_bearer_token()

    def make_request(self, url, params={}):
        headers = {
            'Authorization': 'Bearer {0}'.format(self.bearer_token)
        }
        return requests.get('https://api.twitter.com/{0}'.format(url),
                            headers=headers, params=params)

    def encode_credentials(self):
        encoded_key = urllib.urlencode({'': self.consumer_key})[1:]
        encoded_secret = urllib.urlencode({'': self.consumer_secret})[1:]
        credentials = '{0}:{1}'.format(encoded_key, encoded_secret)
        self.encoded_credentials = base64.b64encode(credentials)

    def request_bearer_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Basic {0}'.format(self.encoded_credentials)
        }

        req = requests.post('https://api.twitter.com/oauth2/token',
                            data={'grant_type': 'client_credentials'},
                            headers=headers)

        if req.ok and req.json['token_type'] == 'bearer':
            self.bearer_token = req.json['access_token']

    def invalidate_bearer_token(self):
        headers = {
            'Authorization': 'Basic {0}'.format(self.encoded_credentials)
        }

        req = requests.post('https://api.twitter.com/oauth2/invalidate_token',
                            data={'access_token': self.bearer_token},
                            headers=headers)

        if req.ok and req.json['access_token'] == self.bearer_token:
            self.bearer_token = ''

    def get_user_timeline(self, **kwargs):
        req = self.make_request('1.1/statuses/user_timeline.json', kwargs)

        return req.json if req.ok else []
