import os
import urllib.parse
from typing import List
import distutils.util

import requests
import msal
import flask_login

# Authentication options
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
AUTHORITY = os.environ['AUTHORITY']
VALIDATE_AUTHORITY = distutils.util.strtobool(
    os.getenv('VALIDATE_AUTHORITY', 'True'))


class User(flask_login.UserMixin):
    scopes = list()  # type: List[str]

    def __init__(self, user_id: str):
        self.id = user_id

    @classmethod
    def get_config(cls) -> dict:
        """
        Get Oauth2 configuration

        https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc
        """

        # Microsoft example:
        # https://login.microsoftonline.com/common/.well-known/openid-configuration

        # Retrieve endpoint data
        url = urllib.parse.urljoin(AUTHORITY,
                                   '.well-known/openid-configuration')
        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    @classmethod
    def get_app(cls) -> msal.ClientApplication:
        return msal.ConfidentialClientApplication(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=AUTHORITY,
            validate_authority=VALIDATE_AUTHORITY,
        )

    @classmethod
    def get_auth_flow(cls) -> dict:
        """
        Authentication flow

        https://docs.microsoft.com/en-gb/azure/active-directory/develop/scenario-web-app-sign-user-sign-in?tabs=python
        https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-desktop-acquire-token?tabs=python
        """
        client_app = cls.get_app()
        code_flow = client_app.initiate_auth_code_flow(
            scopes=cls.scopes)  # type: dict
        return code_flow
