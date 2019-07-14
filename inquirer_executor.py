from inquirer import List, Checkbox, prompt

class InquirerExecutorBase:
    def __init__(self, message, functions, carousel=False, inquirerInstance=None):
        if not inquirerInstance:
            raise ValueError("You are not meant to use the base class directly, please use InquirerExecutorList or InquirerExecutorCheckbox instead.")
        self.message = message
        self.carousel = carousel
        self.inquirerInstance = inquirerInstance
        self._options = functions
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

    def __iter__(self):
        yield from self._options

    def __add__(self, options):
        # If an iterable has already been provided use it, if not, create one with single item
        options = options if hasattr(options, '__iter__') else [options]
        for item in options:
            if not callable(item):
                raise TypeError("Only function types (or iterables of them) can be added to an InquirerExecutor instance.")
        self._options.extend(options)
        self._update_question()
        return self

    def __getitem__(self, index):
        return self._options[index]

    def __setitem__(self, index, value):
        self._options[index] = value
        self._update_question() 

    def insert(self, index, value):
        self._options.insert(index, value)
        self._update_question()
        return self


class InquirerExecutorList(InquirerExecutorBase):
    def __init__(self, message, functions, carousel=False):
        super().__init__(message, functions, carousel=carousel, inquirerInstance=List)

    def find_function(self):
        for function in self._options:
            if function.__doc__ == self.answer:
                return function

    def prompt_user(self):
        self.answer = prompt(self._question)["omittet"]
        return self
    
    def execute(self, *args, **kwargs):
        if not self.answer:
            raise ValueError("Execution not possible since no answer was provided.")
        self.find_function()(*args, **kwargs)

    def prompt_and_execute(self, *args, **kwargs):
        return self.prompt_user().find_function()(*args, **kwargs)


class InquirerExecutorCheckbox(InquirerExecutorBase):
    def __init__(self, message, functions, carousel=False):
        super().__init__(message, functions, carousel=carousel, inquirerInstance=Checkbox)
        self.execution_stack = []

    def find_functions(self):
        self.execution_stack = [function for function in self._options if function.__doc__ in self.answer]
        return self.execution_stack

    def prompt_user(self):
        self.answer = prompt(self._question)["omittet"]
        return self

    def execute(self, *args, **kwargs):
        if not self.execution_stack:
            raise ValueError("Execution not possible since no answer was provided.")
        for function in self.execution_stack:
            function(*args, **kwargs)

    def prompt_and_execute(self, *args, **kwargs):
        self.prompt_user().find_functions()
        for function in self.execution_stack:
            function(*args, **kwargs)
        return self.execution_stack

class QuestionsCatalogue:
    """
    This class holds multiple instances of the InquirerExecutor class
    or any inquirer classes to be able to prompt for more than one 
    question before starting to execute the users choices.
    """
    pass 