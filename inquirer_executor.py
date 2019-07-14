# -*- coding: utf-8 -*-

from functools import wraps
from inspect import getargspec
from inquirer import List, Checkbox, prompt

class InquirerExecutorBase:
    def __init__(self, message, functions, carousel=False, inquirerInstance=None):
        if not inquirerInstance:
            raise ValueError("You are not meant to use the base class directly, please use InquirerExecutorList or InquirerExecutorCheckbox instead.")
        self.message = message
        self.carousel = carousel
        self.inquirerInstance = inquirerInstance
        self._options = [self._allow_kwargs(f) for f in functions]
        self._update_question()
        self.answer = None

    def _update_question(self):
        kwargs = dict(message=self.message,  choices=[function.__doc__ for function in self._options])
        if self.carousel:
            kwargs.update(("carousel", self.carousel))
        self._question = [
            self.inquirerInstance("omittet", **kwargs)
        ]

    @classmethod
    def from_iterable(cls, message, functions, carousel=False):
        return cls(message, functions, carousel)

    # This is a decorator to avoid TypeErrors for functions that do not expect certain kwargs.
    @staticmethod
    def _allow_kwargs(func):
        argspec = getargspec(func)
        @wraps(func)
        def newfunc(*args, **kwargs):
            if args:
                raise TypeError("You can't use positional arguments with functions that are being used as options.")
            some_args = dict((keyword, kwargs[keyword]) for keyword in argspec.args if keyword in kwargs)
            return func(**some_args)
        return newfunc

    def __iter__(self):
        yield from self._options

    def __add__(self, options):
        # If an iterable has already been provided, use it, if not, create one with single item
        options = options if hasattr(options, '__iter__') else [options]
        for item in options:
            if not callable(item):
                raise TypeError("Only function types (or iterables of them) can be added to an InquirerExecutor instance.")
        self._options.extend(self._allow_kwargs(options))
        self._update_question()
        return self

    def __getitem__(self, index):
        return self._options[index]

    def __setitem__(self, index, value):
        if not callable(value):
            raise TypeError("Only function types (or methods) can be part of an InquirerExecutor instance.")
        self._options[index] = self._allow_kwargs(value)
        self._update_question()
    
    def prompt_user(self, **kwargs):
        self.answer = prompt(self._question, **kwargs)["omittet"]
        return self

    def insert(self, index, value):
        self._options.insert(index, value)
        self._update_question()
        return self

    def reorder(self, indices):
        self._options = [self._options[i] for i in indices]
        self._update_question()
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
        return self.prompt_user(**kwargs).find_function()(*args, **kwargs)


class InquirerExecutorCheckbox(InquirerExecutorBase):
    def __init__(self, message, functions, carousel=False):
        super().__init__(message, functions, carousel=carousel, inquirerInstance=Checkbox)
        self.execution_stack = []

    def find_functions(self):
        self.execution_stack = [function for function in self._options if function.__doc__ in self.answer]
        return self.execution_stack

    def execute(self, *args, **kwargs):
        if not self.execution_stack:
            raise ValueError("Execution not possible since no answer was provided.")
        for function in self.execution_stack:
            function(*args, **kwargs)

    def prompt_and_execute(self, *args, **kwargs):
        self.prompt_user(**kwargs).find_functions()
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