import os
import sys
import unittest
from readchar import key
from copy import deepcopy
from inquirer import List, Checkbox, Text

sys.path.append(os.path.realpath("."))
from inquirer_executor import (
    InquirerExecutorBase as Base,
    InquirerExecutorList as InqExList,
    InquirerExecutorCheckbox as InqExCheckbox,
    QuestionsCatalogue,
    dynamic_docstring_decorator,
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
        self.inqex = InqExList.from_iterable("What do you want to return?", self.fs)

    def test_existance_attributes(self):
        self.assertEqual(self.inqex.message, "What do you want to return?")
        self.assertEqual(self.inqex.carousel, False)
        self.assertEqual(self.inqex._inquirerInstance, List)
        self.assertIs(self.inqex._options, self.fs)
        # self.inqex._question is a list, because this is what
        # inquirer uses to prompt questions
        self.assertIsInstance(self.inqex._question, list)
        self.assertIsInstance(*self.inqex._question, List)

    def test_instantiation_of_base_class(self):
        with self.assertRaises(ValueError):
            Base("What do you want to return?", self.fs)

    def test_carousel_if_true(self):
        new_inqex = InqExList("What?", [], carousel=True)
        self.assertTrue(new_inqex.carousel)

    def test_arg_consistency(self):
        def one_arg(anything):
            return anything

        def same_arg(anything):
            return True

        def two_args(anything, anything_else):
            return [anything, anything_else]

        new_inqex = InqExList("Anything?", [one_arg, same_arg])

        self.assertIsInstance(new_inqex, InqExList)

        with self.assertRaises(AssertionError):
            failing_inqex = InqExList.from_iterable("Anything?", [one_arg, two_args])

    def test_iterating(self):
        l = []
        for f in self.inqex:
            l.append(f)
        self.assertListEqual(l, self.fs)

    def test_adding(self):
        def later_function():
            return "Whatever"

        def failing_due_to_unwanted_argument(argument):
            return argument

        inqex_copy = deepcopy(self.inqex)

        inqex_copy += later_function
        self.assertIn(later_function, inqex_copy._options)
        # check to see if choices of the _question got updated as well
        self.assertIn(later_function.__doc__, inqex_copy._question[0].choices)

        with self.assertRaises(AssertionError):
            inqex_copy += failing_due_to_unwanted_argument

        with self.assertRaises(TypeError):
            inqex_copy += "something that isn't a callable type"

    def test_inserting(self):
        inqex_copy = deepcopy(self.inqex)

        def returns_two():
            return 2

        inqex_copy.insert(1, returns_two)
        self.assertEqual(inqex_copy[1](), 2)

        def failing_due_to_unwanted_argument(argument):
            return argument

        with self.assertRaises(AssertionError):
            inqex_copy.insert(0, failing_due_to_unwanted_argument)

        with self.assertRaises(TypeError):
            inqex_copy.insert(2, "something that isn't a callable type")

    def test_getting(self):
        returns_one = self.inqex[0]
        returns_a_string = self.inqex[1]
        returns_True = self.inqex[2]
        self.assertEqual(returns_one(), 1)
        self.assertEqual(returns_a_string(), "a string")
        self.assertTrue(returns_True())

    def test_setting(self):
        inqex_copy = deepcopy(self.inqex)

        def returns_two():
            return 2

        inqex_copy[0] = returns_two
        self.assertEqual(inqex_copy[0](), 2)

        def failing_due_to_unwanted_argument(argument):
            return argument

        with self.assertRaises(AssertionError):
            inqex_copy[1] = failing_due_to_unwanted_argument

        with self.assertRaises(TypeError):
            inqex_copy[2] = "something that isn't a callable type"

    def test_reordering(self):
        inqex_copy = deepcopy(self.inqex)
        inqex_copy.reorder([2, 0, 1])
        self.assertEqual(self.inqex[0], inqex_copy[1])
        self.assertEqual(self.inqex[1], inqex_copy[2])
        self.assertEqual(self.inqex[2], inqex_copy[0])

    def test_reversing(self):
        inqex_copy = deepcopy(self.inqex)
        inqex_copy.reverse()
        self.assertListEqual(inqex_copy._options, self.inqex[::-1])
        self.assertListEqual(
            inqex_copy._question[0].choices, self.inqex._question[0].choices[::-1]
        )

    def test_removing(self):
        inqex_copy = deepcopy(self.inqex)

        with self.assertRaises(ValueError):
            inqex_copy.remove(["this", "and", "that"])

        # removing by function name
        inqex_copy.remove("return_one")
        self.assertListEqual(inqex_copy._options, [self.inqex[1], self.inqex[2]])
        self.assertEqual(len(inqex_copy._question[0].choices), 2)

        # removing by index
        inqex_copy.remove(0)
        self.assertListEqual(inqex_copy._options, [self.inqex[2]])
        self.assertEqual(len(inqex_copy._question[0].choices), 1)

    def test_prompting(self):
        """
        Prompting is already being sufficiently tested in
        the original python-inquirer library. It is a valid
        assumption that if this class can produce a valid
        instance of a python-inquirer List class, prompting
        works as expected.
        """
        pass

    def test_finding_functions(self):
        inqex_copy = deepcopy(self.inqex)
        inqex_copy.answer = 'Return "a string" '
        self.assertEqual(inqex_copy.find_function(), self.inqex[1])

    def test_executing(self):
        inqex_copy = deepcopy(self.inqex)

        with self.assertRaises(ValueError):
            inqex_copy.execute()

        inqex_copy.answer = 'Return "a string" '
        self.assertEqual(inqex_copy.execute(), "a string")


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

    def test_existance_execution_stack(self):
        self.assertEqual(self.inqex.execution_stack, [])

    def test_prompting(self):
        """
        Prompting is already being sufficiently tested in
        the original python-inquirer library. It is a valid
        assumption that if this class can produce a valid
        instance of a python-inquirer Checkbox class, prompting
        works as expected. 
        """
        pass

    def test_finding_functions(self):
        inqex_copy = deepcopy(self.inqex)
        inqex_copy.answer = ['Return "a string" ', "Return boolean value True"]
        self.assertEqual(inqex_copy.find_functions(), [self.inqex[1], self.inqex[2]])

    def test_executing(self):
        inqex_copy = deepcopy(self.inqex)

        with self.assertRaises(ValueError):
            inqex_copy.execute()

        inqex_copy.answer = ['Return "a string" ', "Return boolean value True"]
        inqex_copy.find_functions()
        for result in inqex_copy.execute():
            self.assertIn(result, ["a string", True])


class TestQuestionsCatalogue(unittest.TestCase):
    def setUp(self):
        def return_one():
            """Return 1"""
            return 1

        def return_two():
            """Return 2"""
            return 2

        def return_three():
            """Return 3"""
            return 3

        def return_four():
            """Return 4"""
            return 4

        def return_five():
            """Return 5"""
            return 5

        self.inqex_checkbox = InqExCheckbox.from_iterable(
            "What do you want to return?", [return_one, return_two]
        )
        self.inqex_list = InqExList.from_iterable(
            "What do you want to return?", [return_three, return_four, return_five]
        )
        self.text_question_first_name = Text(
            "first_name", message="What's your first name"
        )
        self.text_question_last_name = Text(
            "last_name", message="What's your last name"
        )

        self.questions_catalogue = QuestionsCatalogue(
            [
                self.inqex_checkbox,
                self.inqex_list,
                self.text_question_first_name,
                self.text_question_last_name,
            ]
        )

    def test_existance_attributes(self):
        self.assertIsInstance(self.questions_catalogue.execution_stack, list)
        self.assertIsInstance(self.questions_catalogue.answer_dict, dict)

    def test_error_on_invalid_arguments(self):
        with self.assertRaises(TypeError):
            QuestionsCatalogue("an ordinairy string")

        with self.assertRaises(TypeError):
            QuestionsCatalogue(
                [
                    self.inqex_list,
                    self.text_question_last_name,
                    "an ordinairy string as list item",
                ]
            )

        # While the above two should fail, the following is allowed and should pass
        self.assertIsInstance(
            QuestionsCatalogue(
                [
                    self.inqex_list,
                    self.text_question_last_name,
                    self.text_question_first_name,
                ]
            ),
            QuestionsCatalogue,
        )

    def test_prompting(self):
        """
        Prompting is hard to test.
        In this case, prompting itself is already being 
        sufficiently tested in the original python-inquirer 
        library. 
        Whether or not the QuestionsCatalogue's prompt_all()
        method calls the right prompts on the individual 
        questions has extensively been tested manually, 
        but an automated unittest for this matter is not yet
        implemented. TODO HELP PLEASE: If you read this and have a sensible idea on how to implement this, please do tell.
        """
        pass


class TestDocstringDecorator(unittest.TestCase):
    def test_decorator(self):
        @dynamic_docstring_decorator("Overwritten docstring")
        def some_function():
            """Some docstring."""
            return True

        self.assertEqual(some_function.__name__, "some_function")
        self.assertEqual(some_function.__doc__, "Overwritten docstring")
        self.assertTrue(some_function())
