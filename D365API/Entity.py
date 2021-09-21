"""
D365API.Entity
~~~~~~~~~~~~~~
"""

import json
from urllib.parse import urlparse
import requests

from D365API.Constant import D365_API_V

class Entity(object):
    """Entity.
    """

    def __init__(self, access, hostname):
        """Constructor.

        Args:
            access (str): The Microsoft Dynamics 365 access token.
            hostname (str): The Hostname of the environment.
        """

        # Get the access token and set the URL (Uniform Resource Locator)
        self.access_token = access
        self.root_url = f'https://{hostname}.api.crm.dynamics.com/api/data/v{D365_API_V}'

        # Create header
        self.header = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'OData-Version': '4.0',
            'OData-MaxVersion': '4.0'
        }


    def __getattr__(self, label):
        """Get Attribute Passed In.

        Args:
            label (str): The attribute passed in.

        Returns:
            A instance of the Entity class.
        """
        # Set the name / label
        self.label = label

        # Return the self instance
        return self


    def create(self, payload):
        """Create Entity.

        Args:
            payload (dict): The payload (message body) passed in.

        Returns:
            A string for the unique identifier (ID) of the Entity.
        """

        # Create the request URL
        request_url = f'{self.root_url}/{self.label}'

        # Send the request for a response
        r = requests.post(url=request_url,
                          headers=self.header,
                          data=payload)

        # Check the status code
        if r.status_code == 204:
            # Parse the unique identifier (ID) of the entity
            entity_url = r.headers['OData-EntityId']
            begin_id = entity_url.find('(') + 1
            end_id = entity_url.find(')')
            entity_id = entity_url[begin_id:end_id]
            # Return the unique identifier (ID) of the entity
            return entity_id

        # There was an error
        return None


    def read(self, id=None):
        """Read Entity.

        Args:
            id (str): The unique identifier (ID) of the entity.

        Returns:
            A string formatted JSON for the read request
        """

        # Create a read result list to store all the read result
        read_result_list = []

        # Create the request URL
        if id is not None:
            request_url = f'{self.root_url}/{self.label}({id})'
        else:
            request_url = f'{self.root_url}/{self.label}'

        # Send the request for a response
        r = requests.get(url=request_url,
                         headers=self.header)

        # Check the failure status code
        if r.status_code != 200:
            return None

        # Check the success status code
        if r.status_code == 200:
            # Parse the read result
            read_result = json.loads(r.text)

            # Add the read result to list
            if 'value' in read_result:
                # Use extend for multiple result
                read_result_list.extend(read_result['value'])
            else:
                # Use append for single result
                read_result_list.append(read_result)

        # Check if there are more result
        while '@odata.nextLink' in read_result:
            # If there are more result
            # Parse the URL for the next set of result
            request_url = read_result['@odata.nextLink']
            # Send the request for a response
            r = requests.get(url=request_url,
                             headers=self.header)

            # Check the status code
            if r.status_code == 200:
                # Parse the read result
                read_result = json.loads(r.text)

                # Add the read result to list
                if 'value' in read_result:
                    # Use extend for multiple result
                    read_result_list.extend(read_result['value'])
                else:
                    # Use append for single result
                    read_result_list.append(read_result)

        # Return all the read result
        return read_result_list


    def update(self, id, payload):
        """Update Entity.

        Args:
            id (str): The unique identifier (ID) of the entity.
            payload (dict): The payload (message body) passed in.

        Returns:
            An integer for the status code of the update request.
        """

        # Create the request URL
        request_url = f'{self.root_url}/{self.label}({id})'

        # Send the request for a response
        r = requests.patch(url=request_url,
                           headers=self.header,
                           data=payload)

        # Check the status code
        if r.status_code == 204:
            # Return the status code
            return r.status_code

        # There was an error
        return None


    def delete(self, id):
        """Delete Entity.

        Args:
            id (str): The unique identifier (ID) of the entity.

        Returns:
            An integer for the status code of the delete request.
        """

        # Create the request URL
        request_url = f'{self.root_url}/{self.label}({id})'

        # Send the request for a response
        r = requests.delete(url=request_url,
                            headers=self.header)

        # Check the status code
        if r.status_code == 204:
            # Return the status code
            return r.status_code

        # There was an error
        return None


    def associate(self, src, dest):
        """Associate Entity.

        Args:
            src (str): The source unique identifier (ID) of the entity.
            dest (str): The destination unique identifier (ID) of the
                entity.
        """
        pass


    def query(self, **kwargs):
        """Query Entity.

        .. _Query Data using the Web API:
        https://docs.microsoft.com/en-us/powerapps/developer/common-data-service/webapi/query-data-web-api

        .. _Web API Query Data Sample:
        https://docs.microsoft.com/en-us/powerapps/developer/common-data-service/webapi/web-api-query-data-sample

        Args:
            kwargs (dict): The keyword arguments for the query.

        Returns:
            A string formatted JSON for the result of the query.
        """

        # Initialize query
        query = ''

        # If the `select` system query option is specified
        if 'select' in kwargs:
            # Build the query
            query = f"$select={kwargs['select']}"
        # If the `top` system query option is specified
        if 'top' in kwargs:
            # Build the query
            query = f"$top={kwargs['top']}"

        # Create the request URL
        request_url = f'{self.root_url}/{self.label}?{query}'

        # Send the request for a response
        r = requests.get(url=request_url,
                         headers=self.header)

        # Check the status code
        if r.status_code == 200:
            # Return the response text (message body)
            return r.text

        # There was an error
        return None