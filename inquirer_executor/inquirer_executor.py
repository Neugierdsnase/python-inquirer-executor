# -*- coding: utf-8 -*-

from functools import wraps
from inspect import getfullargspec
from inquirer import List, Checkbox, prompt, Path, Editor, Text


class InquirerExecutorBase:
    def __init__(self, message, functions, carousel=False, inquirerInstance=None):
        if not inquirerInstance:
            raise ValueError(
                "You are not meant to use the base class directly, please use InquirerExecutorList or InquirerExecutorCheckbox instead."
            )
        self.message = message
        self.carousel = carousel
        self._inquirerInstance = inquirerInstance
        self._options = functions
        self._update_question()
        self._options_argspecs = None
        self.answer = None
        for function in self._options:
            self._check_arg_consistency(function)

    def _update_question(self):
        kwargs = dict(
            message=self.message,
            choices=[function.__doc__ for function in self._options],
        )
        if self.carousel:
            kwargs.update(carousel=self.carousel)
        self._question = [self._inquirerInstance("omittet", **kwargs)]

    # In the interest of failing fast, checking for consistent args and kwargs at creation time
    def _check_arg_consistency(self, func):
        argspec = getfullargspec(func).args
        if self._options_argspecs or isinstance(self._options_argspecs, list):
            if not self._options_argspecs == argspec:
                raise AssertionError(
                    """
                All functions passed to an InquirerExecutor instance need to accept the same arguments and keywords.
                See README under "Passing arguments and keyword arguments" for more information.
                """
                )
        else:
            self._options_argspecs = argspec

    @classmethod
    def from_iterable(cls, message, functions, carousel=False):
        return cls(message, functions, carousel)

    def __iter__(self):
        yield from self._options

    def __add__(self, options):
        """
        Adds a callable type to the list of options.
        Checks for the right types and parameter consistency
        at execution time.
        """
        # If an iterable has already been provided, use it, if not, create one with single item
        options = options if hasattr(options, "__iter__") else [options]
        for item in options:
            if not callable(item):
                raise TypeError(
                    "Only function types (or iterables of them) can be added to an InquirerExecutor instance."
                )
            self._check_arg_consistency(item)
        self._options.extend(options)
        self._update_question()
        return self

    def __getitem__(self, index):
        return self._options[index]

    def __setitem__(self, index, value):
        if not callable(value):
            raise TypeError(
                "Only function types (or methods) can be part of an InquirerExecutor instance."
            )
        self._check_arg_consistency(value)
        self._options[index] = value
        self._update_question()

    def insert(self, index, value):
        """
        Inserts a callable type (the value parameter) 
        to the list of options at index.
        Checks for the right types and parameter consistency
        at execution time.
        """
        self._options.insert(index, value)
        self._check_arg_consistency(value)
        self._update_question()
        return self

    def reorder(self, indices):
        """
        Reorders the options according to the indices parameter,
        which is a list of numbers, defining the new indices of
        the corresponting options.
        """
        self._options = [self._options[i] for i in indices]
        self._update_question()
        return self

    def reverse(self):
        """
        Reverses the order of the options.
        """
        self._options.reverse()
        self._update_question()
        return self

    def remove(self, function_name_or_index):
        """
        Removes an option either by index if the passed in
        argument is an int or by function name, if the passed
        in argument is a string.
        """
        if isinstance(function_name_or_index, str):
            self._options = [
                option
                for option in self._options
                if option.__name__ != function_name_or_index
            ]
            self._update_question()
        elif isinstance(function_name_or_index, int):
            del self._options[function_name_or_index]
            self._update_question()
        else:
            raise ValueError("You can only remove functions by index or function name.")

    def prompt_user(self, **kwargs):
        """
        Prompts the user and presents them with the available
        options. Sets the instances answer value and returns the
        instance itself.
        """
        self.answer = prompt(self._question, **kwargs)["omittet"]
        return self


class InquirerExecutorList(InquirerExecutorBase):
    """
    This class creates single-choice questions where the
    options are docstrings related to functions (or methods).
    """

    def __init__(self, message, functions, carousel=False):
        super().__init__(message, functions, carousel=carousel, inquirerInstance=List)

    def find_function(self):
        """
        Finds the function in the options that corresponds
        with the instances answer value.
        Then returns that function.
        """
        for function in self._options:
            if function.__doc__ == self.answer:
                return function

    def execute(self, *args, **kwargs):
        """
        Executes the function in the options that corresponds
        with the instances answer value with the passed in args
        and kwargs.
        Returns the return value of the called function.
        """
        if not self.answer:
            raise ValueError("Execution not possible since no answer was provided.")
        return self.find_function()(*args, **kwargs)

    def prompt_and_execute(self, *args, **kwargs):
        """
        Prompts the user and presents them with the available
        options.
        Executes the function in the options that corresponds
        with the users answer with the passed in args
        and kwargs.
        Returns the return value of the called function.
        """
        theme = kwargs.pop("theme", None)
        return self.prompt_user(theme=theme).find_function()(*args, **kwargs)


class InquirerExecutorCheckbox(InquirerExecutorBase):
    """
    This class creates multiple-choice questions where the
    options are docstrings related to functions (or methods).
    """

    def __init__(self, message, functions, carousel=False):
        super().__init__(
            message, functions, carousel=carousel, inquirerInstance=Checkbox
        )
        self.execution_stack = []

    def find_functions(self):
        """
        Finds the functions in the options that corresponds
        with the instances answer value.
        Then returns a list of matching functions.
        """
        self.execution_stack = [
            function for function in self._options if function.__doc__ in self.answer
        ]
        return self.execution_stack

    def execute(self, *args, **kwargs):
        """
        Executes the functions in the options that corresponds
        with the instances execution_stack value with the passed in args
        and kwargs.
        Returns the a list of the called functions return values.
        """
        r = []
        if not self.execution_stack:
            raise ValueError("Execution not possible since no answer was provided.")
        for function in self.execution_stack:
            r.append(function(*args, **kwargs))
        return r

    def prompt_and_execute(self, *args, **kwargs):
        """
        Prompts the user and presents them with the available
        options.
        Executes the functions in the options that corresponds
        with the users answer with the passed in args
        and kwargs.
        Returns the a list of the called functions return values.
        """
        r = []
        theme = kwargs.pop("theme", None)
        self.prompt_user(theme=theme).find_functions()
        for function in self.execution_stack:
            r.append(function(*args, **kwargs))
        return r


class QuestionsCatalogue(list):
    """
    This class inherits from list, so it can be used like a list,
    the only two things is sets itself apart from the built-in list
    is that fact that it type-checks it's members and offers the 
    prompt_all() method. (Request help() for this method for more
    information.)
    All members of the list must either be instances of question
    types offered by the inquirer package, or instances of 
    InquirerExecutorCheckbox or InquirerExecutorList.
    """

    def __init__(self, list_of_questions):
        if not isinstance(list_of_questions, (list, tuple, set, frozenset)):
            raise TypeError("You need to instantiate this class with an iterable type.")
        l = []
        for question in list_of_questions:
            l.append(self._check_item_type(question))
        super().__init__(l)
        self.execution_stack = []
        self.answer_dict = {}

    @staticmethod
    def _check_item_type(question):
        if not isinstance(
            question,
            (
                List,
                Checkbox,
                Path,
                Editor,
                Text,
                InquirerExecutorCheckbox,
                InquirerExecutorList,
            ),
        ):
            raise TypeError(
                "Every item in the iterable must be an instance of an Inquirer or InquirerExecutor class."
            )
        return question

    def prompt_all(self):
        """
        Prompts the user for all questions in the list.
        The method returns a tuple made up of a dict of answers
        to the questions that have been constructed using the "inquirer"-
        package (of the kind the package would return itself) 
        and a list of functions that have been selected by
        the user during the course of answering all of the questions.
        """
        for question in self:
            if isinstance(question, InquirerExecutorList):
                question.prompt_user()
                self.execution_stack.append(question.find_function())
            elif isinstance(question, InquirerExecutorCheckbox):
                question.prompt_user()
                self.execution_stack.extend(question.find_functions())
            else:
                self.answer_dict.update(prompt([question]))
        return (self.answer_dict, self.execution_stack)


def dynamic_docstring_decorator(docstring):
    """
    A decorator that allows for dynamic creation of docstrings.
    """

    def dynamic_docstring_decorator_wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__doc__ = docstring
        return wrapper

    return dynamic_docstring_decorator_wrap
