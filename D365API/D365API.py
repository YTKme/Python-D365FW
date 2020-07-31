"""
D365API
~~~~~~~
"""

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

        self._hostname = hostname
        self._client_id = client_id
        self._client_secret = client_secret
        self._tenant_id = tenant_id
        self._version = 1
        self._rest_v1_url = "https://login.microsoftonline.com/{}/oauth2/token".format(self._tenant_id)
        self._resource = "https://{}.api.crm.dynamics.com/".format(hostname)
        self._rest_v2_url = "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(self._tenant_id)
        self._scope = "https://{}.api.crm.dynamics.com/.default".format(hostname)