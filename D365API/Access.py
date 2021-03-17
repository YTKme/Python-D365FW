"""
D365API.Access
~~~~~~~~~~~~~~
"""

import requests

class Access(object):
    """Access.
    """

    def __init__(self, hostname, client_id, client_secret, tenant_id):
        """Constructor.

        Args:
            hostname (str): The Hostname of the environment.
            client_id (str): The Application (client) ID of the application.
            client_secret (str): The client secret of the application.
            tenant_id (str): The Directory (tenant) ID of the application.
        """

        self.hostname = hostname
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.version = 1
        self.rest_v1_url = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/token'
        self.resource = f'https://{hostname}.api.crm.dynamics.com/'
        self.rest_v2_url = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token'
        self.scope = f'https://{hostname}.api.crm.dynamics.com/.default'
    

    def login(self):
        """Login to Microsoft Dynamics 365.

        Returns:
            A string for the Microsoft Dynamics 365 access (bearer) token
            depending whether if request is OAuth 1.0 or OAuth 2.0.
        """

        if self.version == 1:
            return self._login_rest_v1()
        elif self.version == 2:
            return self._login_rest_v2()
        else:
            return None


    def _login_rest_v1(self):
        """Login via REST (REpresentational State Transfer) Version 1.

        Returns:
            A string for the Microsoft Dynamics 365 access (bearer) token if
            call was successful, or None otherwise.
        """

        # Create header
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Create payload
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'resource': self.resource
        }

        # Send the request
        r = requests.post(url=self.rest_v1_url,
                          headers=header,
                          data=payload)

        # Check the status code
        if r.status_code == 200:
            # Parse the access token
            access_token = r.json()['access_token']
            return access_token

        # There was an error
        return None


    def _login_rest_v2(self):
        pass
