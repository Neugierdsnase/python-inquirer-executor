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
from inquirer import Text, prompt

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
        "email": "chris@apple.com",
    },
    {
        "first_name": "Rasmus",
        "last_name": "Lerdorf",
        "known_for": "PHP",
        "phone": "+25436478",
        "email": "rasmus@lerdorf.ca",
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

favourites = []


class Entry:
    def __init__(self, first_name, last_name, known_for, phone=None, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.known_for = known_for
        self.phone = phone
        self.email = email

    @classmethod
    def create(cls, first_name, last_name, known_for, *args, **kwargs):
        return cls(first_name, last_name, known_for, *args, **kwargs).prepare()

    def prepare(self):
        @dynamic_docstring_decorator("{} {}".format(self.first_name, self.last_name))
        def show_options():
            options = InqExList(
                "What do you want to do with {} {}?".format(
                    self.first_name, self.last_name
                ),
                [self.inspect, self.do_nothing, self.change_number, self.change_email],
            )
            if self in favourites:
                options += self.remove_from_favourites
            else:
                options += self.add_to_favourites

            options.prompt_and_execute()

        self.show_options = show_options

        @dynamic_docstring_decorator(
            "Delete {} {}".format(self.first_name, self.last_name)
        )
        def delete_entry():
            global entries
            entries = [entry for entry in entries if entry.last_name != self.last_name]
            print("Deleted {} {}".format(self.first_name, self.last_name))

        self.delete_entry = delete_entry

        return self

    def __repr__(self):
        return "<Entry object for {} {}>".format(self.first_name, self.last_name)

    def __str__(self):
        """Show contact info."""
        return "Name: {0} {1}\nphone: {2}\nemail: {3}\nknown for: {4}\n".format(
            self.first_name, self.last_name, self.phone, self.email, self.known_for
        )

    def inspect(self):
        """See this person's contact info."""
        print(str(self))

    def add_to_favourites(self):
        """Add this contact to your favourite list."""
        favourites.append(self)

    def remove_from_favourites(self):
        """Remove this contact from your favourite list."""
        global favourites
        favourites = [entry for entry in favourites if entry != self]

    def change_number(self):
        """Change the phone number for this contact."""
        self.phone = prompt(
            [Text("new_number", message="Please enter the new phone number")]
        )["new_number"]

    def change_email(self):
        """Change the email for this contact."""
        self.email = prompt(
            [Text("new_email", message="Please enter the new email adress")]
        )["new_email"]

    def do_nothing(self):
        """Go back."""
        pass


# Lets a list containing objects representing all our data
entries = [
    Entry.create(
        entry["first_name"],
        entry["last_name"],
        entry["known_for"],
        entry["phone"],
        entry["email"],
    )
    for entry in data
]


# The following four functions represent the main menu options
def list_all_constacts():
    """List all the contacts"""
    if not entries:
        print("Your cantact book is empty.")
    else:
        InqExList(
            "Here are all your contacts", [entry.show_options for entry in entries]
        ).prompt_and_execute()


def list_favourites():
    """List favourite contacts"""
    if not favourites:
        print("Your favourites list is empty.")
    else:
        InqExList(
            "Here are your favourite contacts",
            [entry.show_options for entry in favourites],
        ).prompt_and_execute()


def add_new_contact():
    """Add a new contact to the contact book."""

    def save_new_contact(new_contact):
        """Save new contact."""
        entries.append(new_contact)
        print("New contact saved.")

    def add_new_contact_to_favourites(new_contact):
        """Add new contact to favourites."""
        favourites.append(new_contact)
        print("New contact successfully added to favourites.")

    answers_and_functions = QuestionsCatalogue(
        [
            Text("first_name", message="First name"),
            Text("last_name", message="Last name"),
            Text("phone", message="phone number"),
            Text("email", message="email address"),
            Text("known_for", message="known for"),
            InqExCheckbox(
                "What do you want to do with this contact?",
                [save_new_contact, add_new_contact_to_favourites],
            ),
        ]
    ).prompt_all()

    answers = answers_and_functions[0]
    list_of_function = answers_and_functions[1]

    new_contact = Entry.create(
        answers["first_name"],
        answers["last_name"],
        answers["known_for"],
        email=answers["email"],
        phone=answers["phone"],
    )

    for function in list_of_function:
        function(new_contact)


def delete_contacts():
    """Delete contacts."""
    InqExCheckbox(
        "Which contacts do you want to delete?",
        [entry.delete_entry for entry in entries],
    ).prompt_and_execute()


def close():
    """Close the contact book."""
    quit()


def main_menu():
    InqExList(
        "What do you want to do?",
        [list_all_constacts, list_favourites, add_new_contact, delete_contacts, close],
    ).prompt_and_execute()


if __name__ == "__main__":
    print("Welcome to your contact book.")
    while True:
        main_menu()
