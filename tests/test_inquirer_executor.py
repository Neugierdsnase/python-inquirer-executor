import unittest
from inquirer_executor import InquirerExecutor as InqEx

class TestInquirerExecutor(unittest.TestCase):
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
        self.inqex = InqEx.from_iterable("What do you want to return?", fs)

    def tearDown(self):
        pass 
