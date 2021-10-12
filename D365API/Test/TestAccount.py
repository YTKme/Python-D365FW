"""
D365API.TestAccount
~~~~~~~~~~~~~~~~~~~
"""

import json
import os
import uuid
import random
import unittest
import requests

from D365API.Access import Access
from D365API.Entity import Entity
from D365API.Constant import TEST_FILE


def setUpModule():
    """Set Up Module"""
    pass


def tearDownModule():
    """Tear Down Module"""
    pass


class TestAccountCreate(unittest.TestCase):
    """Test the Entity module with Create Account."""
    
    @classmethod
    def setUpClass(cls):
        """Prepare test set up class.

        Get the data from JSON (JavaScript Object Notation) file and
        login. Initialize any prerequisite.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        cls.test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(cls.test_data_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname from the Test Data
        cls.hostname = cls.data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = cls.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        cls.access = Access(hostname=cls.hostname,
                            client_id=oauth_1_0_user_success['client_id'],
                            client_secret=oauth_1_0_user_success['client_secret'],
                            tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Create an instance of Entity
        cls.entity = Entity(cls.access, cls.hostname)


    def test_create_account_random_failure(self):
        """Test a random failure for create Account.

        Get the hostname from the Test Data and the generated a random
        Account field to make a request for create. Should result in
        response with status code 400 Bad Request.
        """
        
        # Create payload
        payload = {
            # Generate a random Account field
            'random': f'Random-{random.randrange(10000, 99999)}'
        }

        # Make a request to create the Account with random field
        # Create the Account with the newly generated Account field
        create_account_id = self.entity.accounts.create(json.dumps(payload))

        # Test to ensure Account information is None
        self.assertIsNone(create_account_id)


    @unittest.expectedFailure
    def test_create_account_description_failure(self):
        """Test a description failure for create Account.

        Get the hostname from the Test Data and the generated a random
        Account Description to make a request for create. Should result
        in response with status code 400 Bad Request.
        """
        
        # Create payload
        payload = {
            # Generate a random Account description
            'description': f'Description-{random.randrange(10000, 99999)}'
        }

        # Make a request to create the Account with random description
        # Create the Account with the newly generated Account description
        create_account_id = self.entity.accounts.create(json.dumps(payload))

        # Test to ensure Account information is None
        self.assertIsNone(create_account_id)


    def test_create_account_success(self):
        """Test a success for create Account.

        Get the hostname from the Test Data and the generated Account
        Name to make a request for create. Should result in response
        with status code 204 No Content.
        """

        # Create payload
        payload = {
            # Generate a random Account Name
            'name': f'Account-{random.randrange(10000, 99999)}'
        }

        # Make a request to create the Account
        # Get the return unique identifier (ID)
        # The payload need to be serialized to JSON formatted str (json.dumps)
        create_account_id = self.entity.accounts.create(json.dumps(payload))

        # Create the dictionary for Account data
        self.data['accounts'] = {}
        self.data['accounts']['create_account_success'] = {}
        # Create or update the Account ID in the Test Data
        self.data['accounts']['create_account_success']['id'] = create_account_id

        # Write the new Test Data to file
        with open(self.test_data_file, 'w') as f:
            json.dump(self.data, f)

        # Test to ensure Account ID is a string
        self.assertEqual(type(create_account_id), str)


    @classmethod
    def tearDownClass(cls):
        """Prepare test tear down class.

        Clean up Test Data.
        """

        # Check if Account data exist
        if 'accounts' in cls.data:
            # Get the create Account success unique identifier (ID)
            create_account_id = cls.data['accounts']['create_account_success']['id']
            # Make a request to delete the Account
            create_account = cls.entity.accounts.delete(create_account_id)
            # Check if the delete was successful
            if create_account == 204:
                # Delete the Account entry from the Test Data
                del cls.data['accounts']

            # Write the new Test Data to file
            with open(cls.test_data_file, 'w') as f:
                json.dump(cls.data, f)


class TestAccountRead(unittest.TestCase):
    """Test the Entity module with Read Account."""
    
    @classmethod
    def setUpClass(cls):
        """Prepare test set up class.

        Get the data from JSON (JavaScript Object Notation) file and
        login. Initialize any prerequisite.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        cls.test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(cls.test_data_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname from the Test Data
        cls.hostname = cls.data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = cls.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        cls.access = Access(hostname=cls.hostname,
                            client_id=oauth_1_0_user_success['client_id'],
                            client_secret=oauth_1_0_user_success['client_secret'],
                            tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Create an instance of Entity
        cls.entity = Entity(cls.access, cls.hostname)

        # Create payload
        payload = {
            # Generate a random Account Name
            'name': f'Account-{random.randrange(10000, 99999)}'
        }

        # Make a request to create the Account
        # Get the return unique identifier (ID)
        # The payload need to be serialized to JSON formatted str (json.dumps)
        cls.account_id = cls.entity.accounts.create(json.dumps(payload))


    def test_read_account_failure(self):
        """Test a failure of read Account.

        Generate a random Universally Unique IDentifier (UUID) to make a
        request for read. Should result in response with None.
        """

        # Generate a random UUID
        read_account_id = uuid.uuid4()

        # Make a request to read the Account with unique identifier (ID)
        account = self.entity.accounts.read(read_account_id)

        # Test to ensure read Account information is None
        self.assertIsNone(account)


    def test_read_account_success(self):
        """Test a success for read Account.

        Get the hostname from the Test Data to make a request for read.
        Should result in response with status code 200 OK and a list
        formatted JSON for the result of the read.
        """

        # Make a request to read the Account
        read_account = self.entity.accounts.read(self.account_id)

        # Test to ensure Account information is a string
        self.assertEqual(type(read_account), list)

    @unittest.expectedFailure
    def test_read_account_count_success(self):
        """Test a success for read count Account.

        Get the hostname from the Test Data to make a request for read.
        Should result in response with a list, the count Account result
        is +1 more than the read Account result from  the
        `RetrieveTotalRecordCount` function due to `setUpClass`
        function.
        """

        # Get the Account count using the `RetrieveTotalRecordCount` function
        request_url = f"{self.entity.accounts.root_url}/RetrieveTotalRecordCount(EntityNames=['account'])"

        # Create header
        header = {
            'Authorization': f'Bearer {self.access}',
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'OData-Version': '4.0',
            'OData-MaxVersion': '4.0'
        }

        # Make a request to count the total Account
        count_account_result = requests.get(url=request_url,
                                            headers=header)

        # Parse the Account count result
        count_account = json.loads(count_account_result.text)['EntityRecordCountCollection']['Values'][0]

        # Make a request to read the Account
        read_account = self.entity.accounts.read()

        # Test to ensure count Account (+1) is the same as read Account
        self.assertEqual((count_account + 1), len(read_account))


    @classmethod
    def tearDownClass(cls):
        """Prepare test tear down class.

        Clean up Test Data.
        """

        # Make a request to delete the Account
        _ = cls.entity.accounts.delete(cls.account_id)


class TestAccountUpdate(unittest.TestCase):
    """Test the Entity module with Update Account."""
    
    @classmethod
    def setUpClass(cls):
        """Prepare test set up class.

        Get the data from JSON (JavaScript Object Notation) file and
        login.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        cls.test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(cls.test_data_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname from the Test Data
        cls.hostname = cls.data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = cls.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        cls.access = Access(hostname=cls.hostname,
                            client_id=oauth_1_0_user_success['client_id'],
                            client_secret=oauth_1_0_user_success['client_secret'],
                            tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Create an instance of Entity
        cls.entity = Entity(cls.access, cls.hostname)

        # Create payload
        payload = {
            # Generate a random Account Name
            'name': f'Account-{random.randrange(10000, 99999)}'
        }

        # Make a request to create the Account
        # Get the return unique identifier (ID)
        # The payload need to be serialized to JSON formatted str (json.dumps)
        cls.account_id = cls.entity.accounts.create(json.dumps(payload))


    def test_update_account_failure(self):
        """Test a failure for Account update.

        Generate a random Universally Unique IDentifier (UUID) and an
        incorrect Account Name to make a request for update. Should
        result in response with None.
        """

        # Generate a random UUID
        update_account_id = uuid.uuid4()

        # Create payload
        payload = {
            # Generate a random Account Name
            'name': f'Account-{random.randrange(10000, 99999)}'
        }

        # Make a request to update the Account with the incorrect unique identifier (ID)
        # Update the Account Name with the newly generated Account Name
        update_account = self.entity.accounts.update(update_account_id, json.dumps(payload))

        # Test to ensure update Account information is None
        self.assertIsNone(update_account)


    def test_update_account_success(self):
        """Test a success for Account update.

        Get the hostname from the Test Data and the generated a new
        Account Name to make a request for update. Should result in
        response with status code 204 No Content.
        """

        # Create payload
        payload = {
            # Generate a random Account Name
            'name': f'Account-{random.randrange(10000, 99999)}'
        }

        # Make a request to update the Account with unique identifier (ID)
        # Update the Account Name with the newly generated Account Name
        update_account = self.entity.accounts.update(self.account_id, json.dumps(payload))

        # Test to ensure HTTP status code is 204 No Content
        self.assertEqual(update_account, 204)


    @classmethod
    def tearDownClass(cls):
        """Prepare test tear down class.

        Clean up Test Data.
        """

        # Make a request to delete the Account
        _ = cls.entity.accounts.delete(cls.account_id)


class TestAccountDelete(unittest.TestCase):
    """Test the Entity module with Delete Account."""
    
    @classmethod
    def setUpClass(cls):
        """Prepare test set up class.

        Get the data from JSON (JavaScript Object Notation) file and
        login.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        cls.test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(cls.test_data_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname from the Test Data
        cls.hostname = cls.data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = cls.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        cls.access = Access(hostname=cls.hostname,
                            client_id=oauth_1_0_user_success['client_id'],
                            client_secret=oauth_1_0_user_success['client_secret'],
                            tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Create an instance of Entity
        cls.entity = Entity(cls.access, cls.hostname)

        # Create payload
        payload = {
            # Generate a random Account Name
            'name': f'Account-{random.randrange(10000, 99999)}'
        }

        # Make a request to create the Account
        # Get the return unique identifier (ID)
        # The payload need to be serialized to JSON formatted str (json.dumps)
        cls.account_id = cls.entity.accounts.create(json.dumps(payload))


    def test_delete_account_failure(self):
        """Test a failure for Account delete.

        Generate a random Universally Unique IDentifier (UUID) to make a
        request for delete. Should result in response with None.
        """

        # Generate a random UUID
        delete_account_id = uuid.uuid4()

        # Make a request to delete the Account with unique identifier (ID)
        # Delete the Account
        delete_account = self.entity.accounts.delete(delete_account_id)

        # Test to ensure delete Account information is None
        self.assertIsNone(delete_account)


    def test_delete_account_success(self):
        """Test a success for Account delete.

        Get the hostname and the unique identifier (ID) from the Test
        Data to make a request for delete. Should result in response
        with status code 204 No Content.
        """

        # Make a request to delete the Account with unique identifier (ID)
        delete_account = self.entity.accounts.delete(self.account_id)

        # Test to ensure HTTP status code is 204 No Content
        self.assertEqual(delete_account, 204)


    @classmethod
    def tearDownClass(cls):
        """Prepare test tear down class.

        Clean up Test Data.
        """

        # Make a request to delete the Account
        _ = cls.entity.accounts.delete(cls.account_id)


class TestAccountAssociate(unittest.TestCase):
    """Test the Entity module with Associate Account."""

    @classmethod
    def setUpClass(cls):
        """Prepare test set up class.

        Get the data from JSON (JavaScript Object Notation) file and
        login.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        cls.test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(cls.test_data_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname from the Test Data
        cls.hostname = cls.data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = cls.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        cls.access = Access(hostname=cls.hostname,
                            client_id=oauth_1_0_user_success['client_id'],
                            client_secret=oauth_1_0_user_success['client_secret'],
                            tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Create an instance of Entity
        cls.entity = Entity(cls.access, cls.hostname)

        # Generate a random number
        random_number = random.randrange(10000, 99999)

        # Create Account using payload
        payload = {
            'name': f'Account-{random_number}'
        }

        # Make a request to create the Account
        # Get the return unique identifier (ID)
        # The payload need to be serialized to JSON formatted str (json.dumps)
        cls.account_id = cls.entity.accounts.create(json.dumps(payload))

        # Create Opportunity using payload
        payload = {
            'name': f'Opportunity-{random_number}'
        }

        # Make a request to create the Opportunity
        cls.opportunity_id = cls.entity.opportunities.create(json.dumps(payload))


    def test_associate_account_opportunity_failure(self):
        """Test a failure for associate Account to Opportunity.

        Generate random Universally Unique IDentifier (UUID) for Account
        and Opportunity to make a request to associate the two entity.
        Should result in a response with None.
        """

        # Generate a random UUID for Account
        random_account_id = uuid.uuid4()
        # Generate a random UUID for Opportunity
        random_opportunity_id = uuid.uuid4()

        # Make a request to associate Account and Opportunity
        associate_account = self.entity.accounts.associate(primary_id=random_account_id,
                                                           collection='opportunity_customer_accounts',
                                                           secondary='opportunities',
                                                           secondary_id=random_opportunity_id)

        # Test to ensure associate Account information is None
        self.assertIsNone(associate_account)


    def test_associate_account_opportunity_success(self):
        """Test a success for associate Account to Opportunity.

        Get the unique identifier (ID) for Account and Opportunity to
        make a request to associate the two entity. Should result in a
        response with status code 204 No Content.
        """

        # Make a request to associate Account and Opportunity
        associate_account = self.entity.accounts.associate(primary_id=self.account_id,
                                                           collection='opportunity_customer_accounts',
                                                           secondary='opportunities',
                                                           secondary_id=self.opportunity_id)

        # Test to ensure HTTP status code is 204 No Content
        self.assertEqual(associate_account, 204)


    @classmethod
    def tearDownClass(cls):
        """Prepare test tear down class.

        Clean up Test Data.
        """

        # Make a request to disassociate Account and Opportunity
        _ = cls.entity.accounts.disassociate(primary_id=cls.account_id,
                                             collection='opportunity_customer_accounts',
                                             secondary='opportunities',
                                             secondary_id=cls.opportunity_id)

        # Make a request to delete the Account
        _ = cls.entity.accounts.delete(cls.account_id)
        # Make a request to delete the Opportunity
        _ = cls.entity.opportunities.delete(cls.opportunity_id)


class TestAccountDisassociate(unittest.TestCase):
    """Test the Entity module with Disassociate Account."""

    @classmethod
    def setUpClass(cls):
        """Prepare test set up class.

        Get the data from JSON (JavaScript Object Notation) file and
        login.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        cls.test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(cls.test_data_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname from the Test Data
        cls.hostname = cls.data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = cls.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        cls.access = Access(hostname=cls.hostname,
                            client_id=oauth_1_0_user_success['client_id'],
                            client_secret=oauth_1_0_user_success['client_secret'],
                            tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Create an instance of Entity
        cls.entity = Entity(cls.access, cls.hostname)

        # Generate a random number
        random_number = random.randrange(10000, 99999)

        # Create Account using payload
        payload = {
            'name': f'Account-{random_number}'
        }

        # Make a request to create the Account
        # Get the return unique identifier (ID)
        # The payload need to be serialized to JSON formatted str (json.dumps)
        cls.account_id = cls.entity.accounts.create(json.dumps(payload))

        # Create Opportunity using payload
        payload = {
            'name': f'Opportunity-{random_number}'
        }

        # Make a request to create the Opportunity
        cls.opportunity_id = cls.entity.opportunities.create(json.dumps(payload))

        # Make a request to associate Account and Opportunity
        cls.entity.accounts.associate(primary_id=cls.account_id,
                                      collection='opportunity_customer_accounts',
                                      secondary='opportunities',
                                      secondary_id=cls.opportunity_id)


    def test_disassociate_account_opportunity_failure(self):
        """Test a failure for disassociate Account to Opportunity.

        Generate random Universally Unique IDentifier (UUID) for Account
        and Opportunity to make a request to disassociate the two
        entity. Should result in a response with None.
        """

        # Generate a random UUID for Account
        random_account_id = uuid.uuid4()
        # Generate a random UUID for Opportunity
        random_opportunity_id = uuid.uuid4()

        # Make a request to disassociate Account and Opportunity
        disassociate_account = self.entity.accounts.disassociate(primary_id=random_account_id,
                                                                 collection='opportunity_customer_accounts',
                                                                 secondary='opportunities',
                                                                 secondary_id=random_opportunity_id)

        # Test to ensure disassociate Account information is None
        self.assertIsNone(disassociate_account)


    def test_disassociate_account_opportunity_success(self):
        """Test a success for disassociate Account to Opportunity.

        Get the unique identifier (ID) for Account and Opportunity to
        make a request to disassociate the two entity. Should result in
        a response with status code 204 No Content.
        """

        # Make a request to disassociate Account and Opportunity
        disassociate_account = self.entity.accounts.disassociate(primary_id=self.account_id,
                                                                 collection='opportunity_customer_accounts',
                                                                 secondary='opportunities',
                                                                 secondary_id=self.opportunity_id)

        # Test to ensure HTTP status code is 204 No Content
        self.assertEqual(disassociate_account, 204)


    @classmethod
    def tearDownClass(cls):
        """Prepare test tear down class.

        Clean up Test Data.
        """

        # Make a request to disassociate Account and Opportunity
        _ = cls.entity.accounts.disassociate(primary_id=cls.account_id,
                                             collection='opportunity_customer_accounts',
                                             secondary='opportunities',
                                             secondary_id=cls.opportunity_id)

        # Make a request to delete the Account
        _ = cls.entity.accounts.delete(cls.account_id)
        # Make a request to delete the Opportunity
        _ = cls.entity.opportunities.delete(cls.opportunity_id)


class TestAccountQuery(unittest.TestCase):
    """Test the Entity module with Query Account."""

    @classmethod
    def setUpClass(cls):
        """Prepare test set up class.

        Get the data from JSON (JavaScript Object Notation) file and
        login.
        """

        # Get the current directory of the file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the path of the Test Data file
        cls.test_data_file = os.path.join(current_directory, TEST_FILE)

        # Open the file for reading
        with open(cls.test_data_file, 'r') as f:
            cls.data = json.load(f)

        # Get the hostname from the Test Data
        cls.hostname = cls.data['organizations']['name']

        # Get the user data for success login
        oauth_1_0_user_success = cls.data['systemusers']['oauth_1_0_user_success']

        # Create an instance of Access object and login
        cls.access = Access(hostname=cls.hostname,
                            client_id=oauth_1_0_user_success['client_id'],
                            client_secret=oauth_1_0_user_success['client_secret'],
                            tenant_id=oauth_1_0_user_success['tenant_id']).login()

        # Create an instance of Entity
        cls.entity = Entity(cls.access, cls.hostname)


    def test_query_select_account_success(self):
        """Test a success for Account query `select`.

        Get the hostname from the Test Data to make a request for query.
        Test for the `select` system query option. Should result in
        response with status code 200 OK and a string formatted JSON for
        the result of the query.
        """

        # Define query property
        query = {
            'select': 'accountid,name'
        }

        # Make a request to query the Account
        query_account = self.entity.accounts.query(**query)

        # Test to ensure Account information is a string
        self.assertEqual(type(query_account), str)


    def test_query_top_account_success(self):
        """Test a success for Account query `top`.

        Get the hostname from the Test Data to make a request for query.
        Test for the `top` system query option. Should result in
        response with status code 200 OK and a string formatted JSON for
        the result of the query.
        """

        # Set the `top` system query option count
        top_count = 3
        
        # Define query property
        query = {
            'top': top_count
        }

        # Make a request to query the Account
        query_account = self.entity.accounts.query(**query)

        # Count the number of result
        query_account_count = len(json.loads(query_account)['value'])

        # Test to ensure the Account query count is same as `top` count
        self.assertLessEqual(query_account_count, top_count)


    @classmethod
    def tearDownClass(cls):
        """Prepare test tear down class.

        Clean up Test Data.
        """

        # No need clean up
        pass


def suite():
    """Test Suite"""

    # Create the Unit Test Suite
    suite = unittest.TestSuite()

    # Add the Unit Test
    suite.addTest(TestAccountCreate())
    suite.addTest(TestAccountRead())
    suite.addTest(TestAccountUpdate())
    suite.addTest(TestAccountDelete())
    suite.addTest(TestAccountAssociate())
    suite.addTest(TestAccountQuery())

    # Return the Test Suite
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())