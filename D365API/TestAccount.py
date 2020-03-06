"""
D365API.TestAccount
~~~~~~~~~~~~~~~~~~~
"""

import json
import os
import random
import unittest

from D365API.Access import Access
from D365API.Entity import Entity

class TestAccount(unittest.TestCase):
    """Test the Entity module with Account."""

    @classmethod
    def setUpClass(cls):
        """Prepare test class.

        Get the data from JSON (JavaScript Object Notation) file and login.
        """

        # Get the current directory of the file
        cls._current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the test data file
        cls._test_data_file = os.path.join(cls._current_directory, "TestData.json")

        # Open the file for reading
        with open(cls._test_data_file, "r") as f:
            cls._data = json.load(f)

        # Get the hostname
        cls._hostname = cls._data["organizations"]["name"]

        # Get the user data for success login
        user_rest_v1_success = cls._data["systemusers"]["user_rest_v1_success"]

        # Create an instance of Access object and login
        cls._access = Access(hostname=cls._hostname,
                             client_id=user_rest_v1_success["client_id"],
                             client_secret=user_rest_v1_success["client_secret"],
                             tenant_id=user_rest_v1_success["tenant_id"]).login()


    def test_create_account_success(self):
        """Test a success of create Account.

        Get the hostname from the Test Data and the generated Account Name to
        make a request. Should result in response with status code 204 No Content.
        """

        # Create the payload
        payload = {
            # Generate a random Account Name
            "name": "Account-{}".format(random.randrange(10000, 99999))
        }

        # Create an instance of Entity object
        entity = Entity(self._access, self._hostname)

        # Make a request to create the Account
        # Get the return unique identifier (ID)
        # The payload need to be serialized to JSON formatted str (json.dumps)
        account_id = entity.accounts.create(json.dumps(payload))

        # Test to ensure Account ID is a string
        self.assertEqual(type(account_id), str)

        # Create or update the Account ID in the test data
        self._data["accounts"]["read_account_success"]["id"] = account_id

        # Write the new test data to file
        with open(self._test_data_file, "w") as f:
            json.dump(self._data, f)


    def test_read_account_success(self):
        """Test a success of read Account.

        Get the hostname from the Test Data to make a request. Should result in
        reponse with status code 200 OK.
        """

        # Create an instance of Entity object
        entity = Entity(self._access, self._hostname)

        # Make a request to read the Account
        account = entity.accounts.read()

        # Test to ensure Account information is a string
        self.assertEqual(type(account), str)


    def test_read_account_failure(self):
        """Test a failure of read Account.

        Get the hostname from the Test Data to make a request. Should result in
        reponse with None.
        """

        # Create an instance of Entity object
        entity = Entity(self._access, self._hostname)

        # Get the read Account failure data
        read_account_failure = self._data["accounts"]["read_account_failure"]

        # Make a request to read the Account with unique identifier (ID)
        account = entity.accounts.read(read_account_failure["id"])

        # Test to ensure Account information is None
        self.assertEqual(account, None)


if __name__ == "__main__":
    unittest.main()