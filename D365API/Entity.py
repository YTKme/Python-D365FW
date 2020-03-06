"""
D365API.Entity
~~~~~~~~~~~~~~
"""

from D365API.Rest import Rest
from D365API.Constant import HTTP_GET
from D365API.Constant import HTTP_POST
from D365API.Constant import HTTP_PATCH

class Entity(Rest):
    """Entity.
    """

    def __getattr__(self, label):
        """Get Attribute Passed In.

        Args:
            label (str): The attribute passed in.

        Returns:
            A instance of the Entity class.
        """
        # Set the name / label
        self._label = label

        # Return the self instance
        return self


    def create(self, payload):
        """Create Entity.

        Args:
            payload (dict): The payload (message body) passed in.

        Returns:
            A string for the unique identifier (ID) of the Entity.
        """

        # Create the relative (request) URL
        relative_url = "/{name}".format(name=self._label)

        # Send the request
        r = self.send(HTTP_POST, relative_url, payload)

        # Check the status code
        if r.status_code == 204:
            # Parse the unique identifier (ID) of the entity
            entity_url = r.headers["OData-EntityId"]
            begin_id = entity_url.find("(") + 1
            end_id = entity_url.find(")")
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
            A
        """

        # Create the relative (request) URL
        if id is not None:
            relative_url = "/{name}({id})".format(name=self._label, id=id)
        else:
            relative_url = "/{name}".format(name=self._label)

        # Send the request
        r = self.send(HTTP_GET, relative_url, None)

        # Check the status code
        if r.status_code == 200:
            # Return the response text (message body)
            return r.text

        # There was an error
        return None


    def update(self, id, payload):
        """Update Entity.

        Args:
            id (str): The unique identifier (ID) of the entity.
            payload (dict): The payload (message body) passed in.
        """

        # Create the relative (request) URL
        relative_url = "/{name}({id})".format(name=self._label, id=id)

        # Send the request
        r = self.send(HTTP_PATCH, relative_url, payload)

        # Check the status code
        if r.status_code == 204:
            # Return the status code
            return r.status_code

        # There was an error
        return None


    def delete(self):
        """Delete Entity.
        """

        print("Delete " + self._label)