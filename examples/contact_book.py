# -*- coding: utf-8 -*-

#             _   _
#   _ __ _  _| |_| |_  ___ _ _ ___
#  | '_ \ || |  _| ' \/ _ \ ' \___|
#  | .__/\_, |\__|_||_\___/_||_|
#  |_|   |__/        _
#  (_)_ _  __ _ _  _(_)_ _ ___ _ _ ___
#  | | ' \/ _` | || | | '_/ -_) '_|___|
#  |_|_||_\__, |\_,_|_|_| \___|_|
#   _____ ___|_|__ _  _| |_ ___ _ _
#  / -_) \ / -_) _| || |  _/ _ \ '_|
#  \___/_\_\___\__|\_,_|\__\___/_|
#   __ ___ _ _| |_ __ _ __| |_ ___
#  / _/ _ \ ' \  _/ _` / _|  _|___|
#  \__\___/_||_\__\__,_\__|\__|
#  | |__  ___  ___| |_____
#  | '_ \/ _ \/ _ \ / /___|
#  |_.__/\___/\___/_\_\     _
#   _____ ____ _ _ __  _ __| |___
#  / -_) \ / _` | '  \| '_ \ / -_)
#  \___/_\_\__,_|_|_|_| .__/_\___|
#                     |_|

# author: Konstantin Kovar
# email: mail@vomkonstant.in

# This file is by no means meant to be an example on how
# to code a contact book application.
# This script's purpose is merely to showcase uses for
# python-inquirer-executor rather than to produce high-quality code.
# It is therefore written in a way that you can examine it top to
# bottom and have a good idea of what's happening to familiarize
# yourself with this package.
# The code is also heavily commented for this very reason.


import os
import sys
from inquirer import Text, List, prompt

sys.path.append(os.path.realpath("."))
from inquirer_executor import (
    InquirerExecutorList as InqExList,
    InquirerExecutorCheckbox as InqExCheckbox,
    QuestionsCatalogue,
    dynamic_docstring_decorator,
)

# You will be able to do three things with this contact book:
# 1) List all contacts (and then edit them a bit)
# 2) Add a new contact
# 3) Delete contacts

# First things first, lets start with some mock data:

data = [
    {
        "first_name": "Guido",
        "last_name": "van Rossum",
        "known_for": "Python",
        "phone": "+123456789",
        "email": "bdfl@python.org",
    },
    {
        "first_name": "Linus",
        "last_name": "Torvalds",
        "known_for": "Linux",
        "phone": "+12567891",
        "email": "dontdisturbme@ever.com",
    },
    {
        "first_name": "Chris",
        "last_name": "Lattner",
        "known_for": "Swift",
        "phone": "+35476588",
        "email": "guido@dropbox.com",
    },
    {
        "first_name": "Rasmus",
        "last_name": "Lerdorf",
        "known_for": "PHP",
        "phone": "+25436478",
        "email": "guido@dropbox.com",
    },
    {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "known_for": "Note G",
        "phone": None,
        "email": None,
    },
]

# This data could of course also be imported from
# a database, a csv, tsv, a shelve or whatever.
#
# Now that we have our data, let's define a class
# representing the entries.


class Entry:
    def __init__(self, first_name, last_name, known_for, phone=None, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.known_for = known_for
        self.phone = phone
        self.email = email

        # It might seem strange to define this in the __init__ method
        # and in fact you don't have to, but we need a place where the
        # decorator is in scope to access the first_name and last_name
        # OR self.first_name and self.last_name values.
        # The __init__ method has one of these scopes.
        @dynamic_docstring_decorator("{} {}".format(first_name, last_name))
        def show_options():
            InqExList(
                "What do you want to do with this contact?",
                [self.add_to_favourites, self.change_number, self.change_email],
            ).prompt_and_execute()

        self.show_options = show_options

    def add_to_favourites(self):
        """Add this contact to your favourite list."""
        pass

    def change_number(self):
        """Change the number for this contact."""
        pass

    def change_email(self):
        """Change the email for this contact."""
        pass


# Lets a list containing objects representing all our data
entries = [
    Entry(
        entry["first_name"],
        entry["last_name"],
        entry["known_for"],
        entry["phone"],
        entry["email"],
    )
    for entry in data
]


def list_all_constacts():
    """List all the contacts"""
    InqExList(
        "Here are all your contacts:", [entry.show_options for entry in entries]
    ).prompt_and_execute()


def close():
    """Close the contact book."""
    quit()


def main_menu():
    InqExList(
        "What do you want to do?", [list_all_constacts, close]
    ).prompt_and_execute()


if __name__ == "__main__":
    print("Welcome to your contact book.")
    while True:
        main_menu()

