"""
D365API.TestD365API
~~~~~~~~~~~~~~~~~~~
"""

import json
import os
import unittest

from D365API.D365API import D365API
from D365API.Constant import TEST_FILE


def setUpModule():
    """Set Up Module"""
    pass


def tearDownModule():
    """Tear Down Module"""
    pass


class TestD365APIGeneral(unittest.TestCase):
    """Test."""

    def test_general(self):
        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(test_data_file, 'r') as f:
            data = json.load(f)

        # Get the hostname from the Test Data
        hostname = data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = data['systemusers']['oauth_1_0_user_success']

        # Get the read Account failure unique identifier (ID)
        read_account_id = 'af2e07f6-fa17-ec11-b6e6-000d3a9b2012'

        # Create an instance of D365API object and login
        d365api = D365API(hostname=hostname,
                          client_id=oauth_1_0_user_success['client_id'],
                          client_secret=oauth_1_0_user_success['client_secret'],
                          tenant_id=oauth_1_0_user_success['tenant_id'])

        print(f'Label: {d365api.accounts.label}')

        print(f'Account: {d365api.accounts.read(id=read_account_id)}')


if __name__ == '__main__':
    unittest.main()