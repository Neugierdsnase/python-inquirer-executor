# python-inquirer-executor
This is a wrapper around [python-inquirer](https://github.com/magmax/python-inquirer). From that project's README:

> So, **Inquirer** should ease the process of asking end user **questions**, **parsing**, **validating** answers, managing **hierarchical prompts** and providing **error feedback**.

This package extends this thought by building classes on top of it to create prompts that will automatically call one or more functions corresponding to the user's choice, while keeping your code nice, tidy and readable. This is achieved by facilitating the docstring of your functions as user-facing representaion of these functions. 

## How to use
### Installation

```
pip install inquirer-executor
```

As the whole code is contained in a single file and has only one dependecy (the built-upon [inquirer](https://github.com/magmax/python-inquirer) package), you can also manually copy/paste this (or parts of it) into your project, if that is how you roll.

### Creating a single-choice question (List)
```python
from inquirer_executor import InquirerExecutorList 

question = InquirerExecutorList("Question you want to ask the user?", list_of_functions)
```
The `list_of_functions` can be any iterable that is exlusively composed of function types. The class will generate the question from the string you provided as the first argument and a list of functions that will be presented to the user as selectable options. These options will be represented by the given function's corresponding **docstring**. 

#### Example

```python
from inquirer_executor import InquirerExecutorList 

def print_one():
    """One."""
    print("one")

def print_two():
    """Two."""
    print("two")

def print_three():
    """Three."""
    print("three")

question = InquirerExecutorList("Of the given choices, how many puppies is best?", [print_one, print_two, print_three])    
```
This will create the instance of the question. You now have `prompt_user()` and `prompt_and_execute()` methods at your disposal. Once you have used the `prompt_user()` method, and the user has provided an answer, you can also:
- use the `find_function()` method to return the corresponding function to the user's answer
- access the instances `answer` value to read the user's answer (the docstring they have selected *as* string)
- use the `execute()` method to execute the users choice at a later point (the function returns the return value of the function called)

For now though, we are just going to use `prompt_and_execute()` to see the results right away:
```python
question.prompt_and_execute()
```
Which gives us this output:
```
[?] Of the given choices, how many puppies is best?: Three.
   One.
   Two.
 > Three.

three
```
The user has chosen from the docstrings representing the functions and the function got executed, printing 'three'. Neat.

### Creating a multiple-choice question (Checkbox)
```python
from inquirer_executor import InquirerExecutorCheckbox

question = InquirerExecutorCheckbox("Question you want to ask the user?", list_of_functions)
```
Initializing this works exactly like it does for the `InquirerExecutorList` class. The difference is the existence of the `execution_stack` value, which is a list that contains all the options the user has checked. So this class will never return a single function, always a list of functions.


#### Example
```python
from inquirer_executor import InquirerExecutorCheckbox

def print_puppies():
    """Puppies."""
    print("puppies")

def print_rocks():
    """Rocks."""
    print("rocks")

def print_kittens():
    """Kittens."""
    print("kittens")

question2 = InquirerExecutorCheckbox("Of the given choices, which ones are furry and cuddly?", [print_puppies, print_rocks, print_kittens])
```
This will create the instance of the question. Again, you now have `prompt_user()` and `prompt_and_execute()` methods at your disposal. Once you have generated an answer with the `prompt_user()` method, you can:
- use the `find_functions()` *(mind the plural 's')* method to return the corresponding list of functions to the users answer
- access the instances `answer` value to read the user's answers (a list of the docstrings they have selected)
- use the `execute()` method to execute the users choices at a later point (the function itself returns a list of the functions return values)

For now though, we are again just going to use `prompt_and_execute()` to get this result:
```
[?] Of the given choices, which one's are furry and cuddly?: 
   X Puppies.
   o Rocks.
 > X Kittens.

puppies
kittens
```
The user has checked options one and three and the corresponing functions got called.

*Keep in mind that in this case `prompt_and_execute()` always returns **a list**.*

### Mutating the question after instantiation

#### Adding

There are two ways to add functions to InquirerExecutor instances after they have been created. The first one is the `+` operator, that will append the added function to the end of the choices associated with the question.

The second one is the `insert(index, value)` method, that will insert a `value` (which in this case has to be a function type) at `index`. Use it like you are used to from the `list` type.

#### Setting

You can also set new values as you are used to like 
```python
instance[0] = new_value
```
where again, `new_value` needs to be a function type.

#### Reordering

InquirerExecutor provides a `reorder(indices)` method where indices is a list of numbers that represent the new order, so when given `[2, 0, 1]`, the original index 0 would be moved to index 2, original index 1 moved to 0 and 2 to 1.

You can also use the `reverse()` method, which also works like you are used to from `list` types.

#### Removing

InquirerExecutor provides a `remove(value)` method, that excepts **either** a **function name** as string **or an index** as number as it's `value` argument. In both cases, the matching function is removed from the choices presented to the user.

### Passing arguments

You can of course pass whatever arguments you like to your functions. Just keep in mind, that potentially any and every function in the list will be called, so all of your functions *must* accept the **same** parameters. To prevent possible errors down the road, InquirerExecuter **enforces this** at creation time and will throw an `AssertionError` if the accepted parameters of your functions don't match.

### Theming

You can use [python-inquirer's built-in theming options](https://magmax.org/python-inquirer/usage.html#themes) with the key difference that you have to **instantiate** the theme **before using it**. You then pass the **instance** to the `prompt_user()` or `prompt_and_execute()` methods using the `theme` keyword, **not** the theme class.

### Dynamically setting docstrings

This package makes it sometimes necessary - or at least preferable - to generate docstrings dynamically. This could be achieved by defining the docstring after you define the function like so:

```python
name = input("What is your name?")

def some_function():
    """Can't display the name variable here."""
    return name

some_function.__doc__ = "Returns your name: {}".format(name)
```
This is possible and valid as long as you are dealing with *normal* functions. As soon as you are trying to do this with methods inside a class, Python will raise an error telling you that the `__doc__` attribute of methods is not writable.

For this reason InquirerExecutor provides a decorator named `dynamic_docstring_decorator` that can be used to set dynamic docstrings. The above code rewritten with the decorator would look like this:

```python
from inquirer_executor import dynamic_docstring_decorator

name = input("What is your name?")

@dynamic_docstring_decorator("Returns your name: {}".format(name))
def some_function():
    """Can't display the name variable here.""" # This docstring gets overwritten
    return name
```

Much nicer and cleaner!

### Using this as part of a whole catalogue of questions

Depending on what you are trying to achieve you might want to organize the questions yourself in a manner that fits your use case best. For simple applications, InquirerExecutor provides a `QuestionsCatalogue` class, that can be instantiated with a n iterable type that consists of either `inquirer` or `inquirer_executor` objects. 

The `QuestionsCatalogue` handles these objects so they feel just like a list of functions and equips you with it's `prompt_all()` method. This method returns a tuple of two items: 1) A dictionairy of all the answers given to the Text, Path, etc. prompts that you may have used directly from `inquirer` and 2) a list of functions the user has chosen from single- and multiple-choice questions in the `QuestionsCatalogue`. In order to keep everything human-readable and easy to reason about, this class provides no way of directly calling all functions, you need to call them yourself however and whenever you see fit.

#### Example

```python
from inquirer import Text
from inquirer_executor import (
    InquirerExecutorList as InqExList,
    InquirerExecutorCheckbox as InqExCheckbox,
    QuestionsCatalogue,
)

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


inqex_checkbox = InqExCheckbox.from_iterable(
    "What do you want to return?", [return_one, return_two]
)

inqex_list = InqExList.from_iterable(
    "What do you want to return?", [return_three, return_four, return_five]
)

text_question_first_name = Text("first_name", message="What's your first name")

text_question_last_name = Text("last_name", message="What's your last name")

questions_catalogue = QuestionsCatalogue(
    [inqex_checkbox, inqex_list, text_question_first_name, text_question_last_name]
)

print(questions_catalogue.prompt_all())

```
Assuming the user checked both options at the checkbox and chose "Return 4" at the single choice question and he is a billionaire from Gotham City the above code would produce something like this:

```
[?] What do you want to return?: 
   X Return 1
 > X Return 2

[?] What do you want to return?: Return 4
   Return 3
 > Return 4
   Return 5

[?] What's your first name: Bruce
[?] What's your last name: Wayne
({'first_name': 'Bruce', 'last_name': 'Wayne'}, [<function return_one at 0x7f516964de18>, <function return_two at 0x7f51663a4d90>, <function return_four at 0x7f516611bd08>])
```
## Examples

If you would like to see this package applied in a bit more complex examples, please do consult the [examples folder](https://github.com/Neugierdsnase/python-inquirer-executor/tree/master/examples) of the repository. These small projects are structured with human-readability in mind and are heavily commented to guide you through the code to get you working with this package in no time.

## Raison D'être

I needed this myself.

## Contributing

Contributions and improvements are very welcome. Please write a test for your code contribution and use the [Black code formatter](https://pypi.org/project/black/) when editing the code in this project.

If you have played around with the package and you think what you have created would make a good example project, I would absolutely love to merge it into the examples folder, please make sure to comment your code so others can understand what you are doing.

## License

Copyright (c) 2019 [Konstantin Kovar](https://blog.vomkonstant.in), based on [python-inquirer](https://github.com/magmax/python-inquirer), by Miguel Ángel García ([@magmax9](https://twitter.com/magmax9)).

Licensed under the [MIT license](https://github.com/Neugierdsnase/python-inquirer-executor/blob/master/LICENSE).
