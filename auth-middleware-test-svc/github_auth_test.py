from connexion.exceptions import OAuthProblem

import logging
import os

from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv('CLIENT_ID', '')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')

def verify_githubauth(token_str):
    id_info = None
    if not token_str:
        logger.warning("Request missing id token")
        raise OAuthProblem('Missing id token')
    try:
        access_token = {'access_token': token_str, 'token_type': 'bearer', 'scope': ['']}
        github = OAuth2Session(CLIENT_ID, token=access_token)
        resp = github.get('https://api.github.com/user')
        if resp.status_code == 200:
            id_info = resp.json()
            print(id_info)
        else:
            logger.warning("The token provides is invalid")
            raise OAuthProblem('Invalid token')
    except:
        logger.warning("The token provides is invalid")
        raise OAuthProblem('Invalid token')

    return id_info

# def test1():
#     import requests, json
#     import subprocess
#     import sys
#
#     # callback url specified when the application was defined
#     callback_uri = "http://localhost:5050/contributions/catalog/auth/callback"
#     test_api_url = "<<the URL of the API you want to call, along with any parameters, goes here>>"
#
#
#     # step A - simulate a request from a browser on the authorize_url - will return an authorization code after the user is
#     # prompted for credentials.
#
#     authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri=' + callback_uri + '&scope=openid'
#
#     print("go to the following url on the browser and enter the code from the returned url: ")
#     print("---  " + authorization_redirect_url + "  ---")
#     authorization_code = input('code: ')
#
#     # step I, J - turn the authorization code into a access token, etc
#     data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
#     print("requesting access token")
#     access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False,
#                                           auth=(client_id, client_secret))
#
#     print("response")
#     print(access_token_response.headers)
#     print('body: ' + access_token_response.text)
#
#     # we can now use the access_token as much as we want to access protected resources.
#     tokens = json.loads(access_token_response.text)
#     access_token = tokens['access_token']
#     print("access token: " + access_token)
#
#     api_call_headers = {'Authorization': 'Bearer ' + access_token}
#     api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
#
#     print(api_call_response.text)


if __name__ == '__main__':
    token_str = os.getenv('TOKEN_STR')
    verify_githubauth(token_str)
    # test1()