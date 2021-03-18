"""
Test
~~~~
"""

import unittest
from D365API.Test.TestAccess import TestAccess

def load_tests(loader, tests, pattern):
    """
    Customize how modules or packages load tests during normal test
    runs or test discovery. This `load_tests` function loads all the
    tests in specific order of execution.

    Args:
        loader (TestLoader): Used to create test suites from classes
            and modules.
        tests (TestCase): The tests loaded by default from the module.
        pattern (str): 

    Returns:
        A TestSuite with the individual test cases.
    """

    # Define the test classes
    test_classes = (
        TestAccess,
    )

    # Create the Unit Test Suite
    suite = unittest.TestSuite()

    # Loop through each of the test classes
    for test_class in test_classes:
        # Load the tests from the test class
        tests = loader.loadTestsFromTestCase(test_class)
        # Add the tests to the test suite
        suite.addTests(tests)

    return suite