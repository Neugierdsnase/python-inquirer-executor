# python-inquirer-executor
This is a wrapper around [python-inquirer](https://github.com/magmax/python-inquirer). From this project's README:

> So, **Inquirer** should ease the process of asking end user **questions**, **parsing**, **validating** answers, managing **hierarchical prompts** and providing **error feedback**.

This package extends this thought by building classes on top of it to create prompts that will automatically call one or more functions corresponding to user's choice, while keeping you code nice, tidy and readable. This is achieved by facilitating the docstring of your functions as user-facing representaion of themselves (which is what docstrings (kinda) are intended to be anyways). 

## How to use
### Installation
As of right now, the only way to use this is to download it from this GitHub repository.
### As a single-choice list
```python
from inquirer_executor import InquirerExecutorList 

question = InquirerExecutorList("Question you want to ask the user?", list_of_functions)
```
The list of functions can be any iterable that is exlusively composed of function types. The class will generate the question from the string you privided as the first argument and give the user the option of choosing a function. These options will be represented by the function's corresponding **docstring**. 

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
- access the instances `answer` value to read the user's answer (the docstring they have selected)
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

### As a multiple-choice checkbox
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
- use the `execute()` method to execute the users choices at a later point (the function itself always returns `None`)

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

*Keep in mind that in this case `prompt_and_execute()` always returns `None`.*

### Using this as part of a whole catalogue of questions

#### Example

### Theming

You can use [python-inquirer's built-in theming options](https://magmax.org/python-inquirer/usage.html#themes) with the key difference that you have **instantiate** the theme **before using it**. You then pass the **instance** to the `prompt_user()` or `prompt_and_execute()` methods using the `theme` keyword, **not** the theme class.

### Additional notes on usage
- Adding options later
  - using the `+` operator
    
    You can just ...

  - using the `insert()` method

    You can also ...

- Mutating options
  - setting an item

    You can ...
  - using the `reorder()` method

    Or you could...

- Passing arguments and keyword arguments

  - You can of course pass whatever arguments you like to your functions. Just keep in mind, that potentially any and every function will be called, so all of your functions *must* accept the **same** arguments and keyword arguments. To prevent possible errors down the road, InquirerExecuter checks for this at creation time and will throw an `AssertionError` if the arguments and keyword arguments of your functions don't match.


## Raison D'être

I needed this myself.

## License

Copyright (c) 2019 [Konstantin Kovar](https://blog.vomkonstant.in), based on [python-inquirer](https://github.com/magmax/python-inquirer), by Miguel Ángel García ([@magmax9](https://twitter.com/magmax9)).

Licensed under the [MIT license](./LICENSE).
