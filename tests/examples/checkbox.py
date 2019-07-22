import os
import sys

sys.path.append(os.path.realpath("."))

from inquirer_executor import InquirerExecutorCheckbox as InqExCheckbox


def print_puppies():
    """Puppies."""
    print("puppies")


def print_stones():
    """Stones."""
    print("stones")


def print_kittens():
    """Kittens."""
    print("kittens")


question = InqExCheckbox(
    "What is fluffy and cuddly?", [print_puppies, print_stones, print_kittens]
)

if sys.argv[1] == "slow":
    returnvalue = question.prompt_user()
    for f in question.execution_stack:
        print(f.__doc__)
    if isinstance(returnvalue, InqExCheckbox):
        print("True")
    else:
        print("False")
elif sys.argv[1] == "fast":
    question.prompt_and_execute()
