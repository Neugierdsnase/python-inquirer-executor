import os
import sys
import unittest

sys.path.append(os.path.realpath("."))

from inquirer_executor import InquirerExecutorList as InqExList


def print_one():
    """One."""
    print("one")


def print_two():
    """Two."""
    print("two")


def print_three():
    """Three."""
    print("three")


question = InqExList(
    "Of the given choices, how many puppies is best?",
    [print_one, print_two, print_three],
)

if sys.argv[1] == "slow":
    returnvalue = question.prompt_user()
    print(question.answer)
    if isinstance(returnvalue, InqExList):
        print("True")
    else:
        print("False")
elif sys.argv[1] == "fast":
    question.prompt_and_execute()

