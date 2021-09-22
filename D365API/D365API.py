"""
D365API
~~~~~~~
"""

from D365API.Access import Access
from D365API.Entity import Entity
from D365API.Constant import D365_API_V

class D365API(Entity):
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

        # Create an instance of Access object and login
        access = Access(hostname=hostname,
                        client_id=client_id,
                        client_secret=client_secret,
                        tenant_id=tenant_id).login()

        # Set the root URL (Uniform Resource Locator)
        self.root_url = f'https://{hostname}.api.crm.dynamics.com/api/data/v{D365_API_V}'

        # Create header
        self.header = {
            'Authorization': 'Bearer ' + access,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'OData-Version': '4.0',
            'OData-MaxVersion': '4.0'
        }
