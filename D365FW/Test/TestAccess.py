"""
D365FW.TestAccess
~~~~~~~~~~~~~~~~~
"""

import json
import os
import unittest
from D365FW.Access import Access
from D365FW.Constant import TEST_FILE

class TestAccess(unittest.TestCase):
    """Test the Access module."""

    @classmethod
    def setUpClass(cls):
        """Prepare test class.

        Get the Test Data from JSON (JavaScript Object Notation) file.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the test data file
        test_access_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(test_access_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname
        cls._hostname = cls.data['organizations']['name']


    def test_login_rest_v1_success(self):
        """Test a success of REST (REpresentational State Transfer) login method.

        Get the success username and password (oauth_1_0_user_success)
        from the Test Data file and login. Should result in login method
        returning an access token.
        """

        # Get the user data for success login
        oauth_1_0_user_success = self.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        access = Access(hostname=self._hostname,
                        client_id=oauth_1_0_user_success['client_id'],
                        client_secret=oauth_1_0_user_success['client_secret'],
                        tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Test to ensure access is a string
        self.assertEqual(type(access), str)


    def test_login_rest_v1_failure(self):
        """Test a failure of REST (REpresentational State Transfer) login method.

        Get the failure username and password (oauth_1_0_user_failure)
        from the Test Data file and login. Should result in login method
        returning None value.
        """

        # Get the user data for success login
        oauth_1_0_user_failure = self.data['systemusers']['oauth_1_0_user_failure']

        # Create an instance of Access object and login
        access = Access(hostname=self._hostname,
                        client_id=oauth_1_0_user_failure['client_id'],
                        client_secret=oauth_1_0_user_failure['client_secret'],
                        tenant_id=oauth_1_0_user_failure['tenant_id']).login()

        # Test to ensure access is not a string
        self.assertNotEqual(type(access), str)


if __name__ == '__main__':
    unittest.main()