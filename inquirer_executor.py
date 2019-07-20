# -*- coding: utf-8 -*-

from functools import wraps
from inspect import getfullargspec
from inquirer import List, Checkbox, prompt


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
            kwargs.update(("carousel", self.carousel))
        self._question = [self._inquirerInstance("omittet", **kwargs)]

    # In the interest of failing fast, checking for consistent args and kwargs at creation time
    def _check_arg_consistency(self, func):
        argspec = getfullargspec(func).args
        print(argspec, self._options_argspecs)
        if self._options_argspecs:
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
        # If an iterable has already been provided, use it, if not, create one with single item
        options = options if hasattr(options, "__iter__") else [options]
        for item in options:
            if not callable(item):
                raise TypeError(
                    "Only function types (or iterables of them) can be added to an InquirerExecutor instance."
                )
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
        self._options[index] = value
        self._update_question()

    def insert(self, index, value):
        self._options.insert(index, value)
        self._update_question()
        return self

    def reorder(self, indices):
        self._options = [self._options[i] for i in indices]
        self._update_question()
        return self

    def prompt_user(self, **kwargs):
        self.answer = prompt(self._question, **kwargs)["omittet"]
        return self


class InquirerExecutorList(InquirerExecutorBase):
    def __init__(self, message, functions, carousel=False):
        super().__init__(message, functions, carousel=carousel, inquirerInstance=List)

    def find_function(self):
        for function in self._options:
            if function.__doc__ == self.answer:
                return function

    def execute(self, *args, **kwargs):
        if not self.answer:
            raise ValueError("Execution not possible since no answer was provided.")
        self.find_function()(*args, **kwargs)

    def prompt_and_execute(self, *args, **kwargs):
        theme = kwargs.pop("theme", None)
        return self.prompt_user(theme=theme).find_function()(*args, **kwargs)


class InquirerExecutorCheckbox(InquirerExecutorBase):
    def __init__(self, message, functions, carousel=False):
        super().__init__(
            message, functions, carousel=carousel, inquirerInstance=Checkbox
        )
        self.execution_stack = []

    def find_functions(self):
        self.execution_stack = [
            function for function in self._options if function.__doc__ in self.answer
        ]
        return self.execution_stack

    def execute(self, *args, **kwargs):
        if not self.execution_stack:
            raise ValueError("Execution not possible since no answer was provided.")
        for function in self.execution_stack:
            function(*args, **kwargs)

    def prompt_and_execute(self, *args, **kwargs):
        theme = kwargs.pop("theme", None)
        self.prompt_user(theme=theme).find_functions()
        for function in self.execution_stack:
            function(*args, **kwargs)
        return self.execution_stack


class QuestionsCatalogue(list):
    """
    This class holds multiple instances of the InquirerExecutor class
    or any inquirer classes to be able to prompt for more than one 
    question before starting to execute the users choices.
    """

    def __init__(self):
        super().__init__()
        self.execution_stack = []

    pass

