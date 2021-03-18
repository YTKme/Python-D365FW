"""
D365API
~~~~~~~
"""

from D365API.Access import Access

class D365API(object):
    """D365API Object

    Main object for the Microsoft D365 (Dynamics 365) API (Application
    Programing Interface).

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

        # Create an instance of Access object and login
        access = Access(hostname=self.hostname,
                        client_id=self.client_id,
                        client_secret=self.client_secret,
                        tenant_id=self.tenant_id).login()
