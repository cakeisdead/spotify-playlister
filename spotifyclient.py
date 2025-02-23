'''Spotify client'''
import http.server
import logging
from utils import random_string
import requests
import socketserver
import urllib.parse
import webbrowser
from threading import Thread
import base64
from contextlib import contextmanager
import time

# logger settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    '''Simple HTTP server to catch the OAuth callback'''

    def do_GET(self):
        '''Handler for get requests'''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.server.path = self.path
        self.wfile.write(b"Authorization received. You can close this window.")


class SpotifyClient:
    '''A simple Spotify client'''
    token = None
    BASE_URL = 'https://api.spotify.com/v1'
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    REDIRECT_URI = 'http://127.0.0.1:8888/callback'
    auth_result = None
    client_id = None
    client_secret = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def token_is_valid(self):
        '''Validate the access token'''
        logger.info("Checking if token is valid...")
        return self.token is not None

    def fetch_playlists(self, user_name):
        '''Fetch the playlists for the specified user'''
        endpoint = f'/users/{user_name}/playlists'
        playlists = []

        try:
            if not self.token_is_valid():
                self.get_token()

            headers = {
                'Authorization': f'Bearer {self.token}'
            }

            r = requests.get(self.BASE_URL + endpoint,
                             headers=headers, timeout=20)
            r.raise_for_status()
            playlists = r.json()

        except requests.exceptions.HTTPError as err:
            print(f"Error: {err}")
            playlists = None

        return playlists

    @contextmanager
    def get_authorization(self, auth_url):
        '''Set up a temporary server to catch the OAuth callback'''
        logger.info("Setting up temporary server...")
        httpd = socketserver.TCPServer(('', 8888), OAuthHandler)
        server_thread = Thread(target=httpd.serve_forever)
        server_thread.daemon = True

        try:
            server_thread.start()
            webbrowser.open(auth_url, autoraise=False)

            while not hasattr(httpd, 'path'):
                time.sleep(1)

            params = dict(urllib.parse.parse_qsl(
                urllib.parse.urlparse(getattr(httpd, 'path')).query))
            self.auth_result = params.get('code')
            yield httpd
        finally:
            logger.info("Shutting down temporary server...")
            httpd.shutdown()
            httpd.server_close()
        logger.info("Authorization received")

    def get_token(self):
        '''Get an access token from Spotify'''
        logger.info("Getting access token...")

        if not self.client_id or not self.client_secret:
            logger.error("Missing credentials")
            raise ValueError("Missing Spotify credentials")

        state = random_string(16)
        scope = 'playlist-read-private playlist-read-collaborative'

        # First, redirect user to auth URL
        logger.info("Redirecting user to authorization URL...")
        auth_url = (
            f'{self.AUTH_URL}'
            f'?response_type=code'
            f'&client_id={self.client_id}'
            f'&scope={scope}'
            f'&redirect_uri={self.REDIRECT_URI}'
            f'&state={state}'
        )

        with self.get_authorization(auth_url) as auth_result:
            auth_code = auth_result

        auth_header = base64.urlsafe_b64encode(
            (self.client_id + ':' + self.client_secret).encode())
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % auth_header.decode('ascii')
        }

        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.REDIRECT_URI,
        }

        # Make a request to the token endpoint to get an access token
        access_token_request = requests.post(
            url=self.TOKEN_URL, data=payload, headers=headers, timeout=20)

        # convert the response to JSON
        access_token_response_data = access_token_request.json()
        self.token = access_token_response_data['access_token']
