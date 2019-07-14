# python-inquirer-executor
This is a wrapper around [python-inquirer](https://github.com/magmax/python-inquirer) that allows you to use it's `List` and `Checkbox` classes to create prompts that will automatically call a function corresponding to the user's choice. While keeping you code nice and tidy.
## How to use
### As a single-choice list
```python
from inquirer_executor import InquirerExecutorList 

question = InquirerExecutorList("Question you want to ask the user?", list_of_functions)
```
The list of functions can be any literal that is exlusively composed of function types. The class will generate the question fron the strin you privided as the first argument and give the user the option of choosing a functions. These options will be represented the function's corresponding **docstring**. 

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
This will create the instance of the question. You now have `prompt_user()` and `prompt_and_execute()` methods at your disposal. Once you have used the `prompt_user()` method, you can also:
- use the `find_function()` method to return the corresponding function to the users answer
- access the instances `answer` value to read the user's answer (the docstring they have selected)
- use the `execute()` method to execute the users choice at later point (the function returns the return value of the function called)

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
The user has chosen from the docstrings representing the functions and the function got executed. Neat.

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

question2 = InquirerExecutorCheckbox("Of the given choices, which one's are furry and cuddly?", [print_puppies, print_rocks, print_kittens])
```
This will create the instance of the question. Again, you now have `prompt_user()` and `prompt_and_execute()` methods at your disposal. Once you have used the `prompt_user()` method, you can also:
- use the `find_functions()` *(mind the plural 's')* method to return the corresponding list of functions to the users answer
- access the instances `answer` value to read the user's answers (a list of the docstrings they have selected)
- use the `execute()` method to execute the users choices at later point (the function itself always returns `None`)

For now though, we are again just going to use `prompt_and_execute()` to see the results right away:
```
[?] Of the given choices, which one's are furry and cuddly?: 
   X Puppies.
   o Rocks.
 > X Kittens.

puppies
kittens
```
*Keep in mind that in this case `prompt_and_execute()` always returns `None`.*
### Using this as part of a whole catalogue of questions

#### Example

### Notes
#### Adding options later
- using the `+` operator
- using the `.insert()` method
#### Passing arguments and keyword arguments

## Raison D'être

I needed it myself.