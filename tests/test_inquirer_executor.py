import unittest
import unittest
from inquirer import List
from inquirer_executor import (
    InquirerExecutorList as InqExList,
    InquirerExecutorCheckbox as InqExCheckbox,
)


class TestInquirerExecutorList(unittest.TestCase):
    """
    These tests test for properties and functionality of 
    the List class as much as of the Base class.
    Since they are tested here, Base class methods will not be tested again in the Checkbox tests.
    """ 
    def setUp(self):
        def return_one():
            """Return 1"""
            return 1

        def return_a_string():
            """Return "a string" """
            return "a string"

        def return_True():
            """Return boolean value True"""
            return True

        self.fs = [return_one, return_a_string, return_True]
        self.inqex = InqExCheckbox.from_iterable("What do you want to return?", self.fs)

    def test_existance_attributes(self):
        self.assertEqual(self.inqex.message, "What do you want to return?")
        self.assertEqual(self.inqex.carousel, False)
        self.assertEqual(self.inqex._inquirerInstance, Checkbox)
        self.assertIs(self.inqex._options, self.fs)
        self.assertIsInstance(self._question, List)

    def test_arg_consistency(self):
        pass

    def test_iterating(self):
        pass
        
    def test_adding(self):
        # Don't forget to test if answer got updated in _options as well!
        pass

    def test_inserting(self):
        pass 

    def test_getting(self):
        pass

    def test_setting(self):
        pass
        
    def test_prompting(self):
        # Here is where pexpect might come in handy

    def test_finding_function(self):
        pass
        
    def test_executing_found_function(self):
        pass

    def test_prompting_and_executing(self):
        pass 

    def tearDown(self):
        pass


class TestInquirerExecutorCheckbox(unittest.TestCase):
    """
    These tests test for properties and functionality of 
    the Checkbox class.
    The Base class methods are being tested in the tests
    for the List class.
    """
    def setUp(self):
        def return_one():
            """Return 1"""
            return 1

        def return_a_string():
            """Return "a string" """
            return "a string"

        def return_True():
            """Return boolean value True"""
            return True

        fs = [return_one, return_a_string, return_True]
        self.inqex = InqExCheckbox.from_iterable("What do you want to return?", fs)

    def test_finding_function(self):
        pass
        
    def test_executing_found_function(self):
        pass

    def test_prompting_and_executing(self):
        pass 

    def tearDown(self):
        pass

    def tearDown(self):
        pass
