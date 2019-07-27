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
#  \___/_\_\___\__|\_,_|\__\___/_|           _
#  | _ \ _ \/ __|___ _____ ____ _ _ __  _ __| |___
#  |   /  _/ (_ |___/ -_) \ / _` | '  \| '_ \ / -_)
#  |_|_\_|  \___|   \___/_\_\__,_|_|_|_| .__/_\___|
#                                      |_|

# author: Konstantin Kovar
# email: mail@vomkonstant.in

# This file is by no means meant to be an example on how
# to code an RPG, in fact it is messy code that could be organised
# much better.
# This script's purpose however is to showcase uses for
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
)


print("Hello brave warrior!")

# Now asking all the initial questions
# For more complex projects it would make sense to organise them differently like
# grouping them in a module or in a class, but here we are creating them
# as we need them

# These are the functions that will be used to choose the role
def choose_assassin():
    """Assassin"""
    return "Assassin"


def choose_mage():
    """Mage"""
    return "Mage"


def choose_berserker():
    """Berserker"""
    return "Berserker"


# These functions will be used to choose a starting weapon
def choose_ax():
    """Ax"""
    return "Ax"


def choose_sword():
    """Sword"""
    return "Sword"


def choose_mace():
    """Mace"""
    return "Mace"


# our hero is being initialized by prompting the player
class Hero:
    def __init__(self, hp=100, atk=11):
        self.name = prompt([Text("name", message="How may I address you?")])["name"]
        # The prompt_and_execute() method directly returns
        # the return value of the chosen option.
        self.role = InqExList(
            "In what martial art style have you been educated?",
            [choose_assassin, choose_berserker, choose_mage],
        ).prompt_and_execute()
        self.weapon = InqExList(
            "What is your weapon of choice?", [choose_ax, choose_sword, choose_mace]
        ).prompt_and_execute()
        self.hp = hp
        self.atk = atk


hero = Hero()

print(
    "You, {}, are our hero and you are being sent on a quest to retrieve the mystical flower of Choc'blath from the dangerous valleys of Phem'trr. Take your {} and off you go.".format(
        hero.name, hero.weapon
    )
)

# These functions will be used to paxk the players backpack.
def choose_lockpicking_set():
    """A set for picking locks, could come in handy."""
    return "lockpicking set"


def choose_map():
    """A map, reduces your chances of getting lost."""
    return "map"


def choose_oil_lamp():
    """An oil lamp, increases you abilities during the night."""
    return "oil lamp"


def choose_healing_potion():
    """A healing potion, works as advertised."""
    return "healing potion"


print(
    """What items do you want to take with you on your journey?
    Keep in mind that every additional item will make you less powerful in a fight."""
)

# This is a mutliple choice question because the player is free to
# choose any, all or none of the options.
# Again, the prompt_and_execute() method directly returns
# the return value of the chosen option.
# I put this in a set type for faster membership checks.
backpack = set(
    InqExCheckbox(
        """Available items:""",
        [choose_lockpicking_set, choose_map, choose_oil_lamp, choose_healing_potion],
    ).prompt_and_execute()
)

print(
    "You are now being sent on your way and would you believe it, right outside the cities gate a monster already blocks your way."
)

print(
    "You have {} items in your backback that are wearing you down, so you have {} attack points.".format(
        len(backpack), hero.atk - len(backpack)
    )
)

# For our purposes, monsters a fine just being dicts
monster1 = dict(hp=20, atk=5, name="the spider-like creature")

# Here we define our combat functions
# we can actually reuse them in every fight
# This is very simplified since we know the player can't actually
# die in this game.
def attack(monster):
    """Attack the monster"""
    monster["hp"] -= hero.atk - len(backpack)
    if not monster["hp"] > 0:
        print("The monster died. You won the fight like only a true hero could.")
        return False
    else:
        print(
            "You attack {} with your {} and apply {} damage. It has {} HP left.".format(
                monster["name"], hero.weapon, (hero.atk - len(backpack)), monster["hp"]
            )
        )
        hero.hp -= monster["atk"]
        print(
            "The monster attacks you and applies {} damage. You have {} HP left.".format(
                monster["atk"], hero.hp
            )
        )
        return True


# This function doesn't actually *need* the monster argument,
# but InquirerExecutor forces us to have only functions that expect
# the same arguments (and keyword arguments) in one question.
# It does so to avoid hard-to-debug errors down the road.
# So in this case, because the `attack` function takes a monster
# argument, the `flee` function too, has to take a monster argument.
#
# For more information on this consult the
# "Passing arguments"-section of the README.
def flee(monster):
    """Flee"""
    print("You ran away like a coward.")
    return False


# Combat loop will break if player flees or monster dies
while True:
    choice = InqExList("What do you do?", [attack, flee]).prompt_and_execute(monster1)
    if not choice:
        break

print("You encounter an abandoned castle. All the doors are locked.")

monster2 = dict(hp=30, atk=7, name="the armored bear")

# This function will only be called if the player actually makes it inside the castle.
def inside_castle():
    """This is what happens when the player manages to get inside the castle."""
    print("Inside the castle you find a treasure, but it's guarded by an armored bear.")
    # We use the same combat loop and the same functions as before.
    while True:
        choice = InqExList("What do you do?", [attack, flee]).prompt_and_execute(
            monster2
        )
        if not choice:
            break
    print(
        "You approach the treasure chest and it is a chest full of items. Choose the one's you want to pick up:"
    )

    # This function showcases a rather uncomfortable edge case:
    # Upon defining the function you cannot dynamically format
    # the docstring.
    # So the function gets defined without a docstring and below...
    def choose_magic_sword():
        old_weapon = hero.weapon
        hero.weapon = "magic sword"
        hero.atk += 3
        print(
            "You are leaving your {} behind and pick up the magic sword. Your attack increases by 3 points an is now {}.".format(
                old_weapon, hero.atk
            )
        )

    # ... we set the docstring to include the weapon the player originally chose.
    choose_magic_sword.__doc__ = "Drop your {} and pick up a magic sword instead for increased attack.".format(
        hero.weapon
    )

    def choose_jewels():
        """Jewels you might be able to sell or trade in for something else."""
        backpack.add("jewels")

    # The player gets prompted to choose his loot, the functions themselves
    # take care of the rest, so we don't need to store the actual return values
    # in a variable
    InqExCheckbox(
        "Items in treasure chest:", [choose_magic_sword, choose_jewels]
    ).prompt_and_execute()


# These functions right here are the options the player has to try
# and get over the wall into the castle
def dont_bother():
    """Not even trying, just moving on."""
    return False


def try_climbing_wall():
    """Try climbing the wall"""
    if len(backpack) > 2:
        print(
            "You are trying to climb the wall, but your backback is too heavy, you can't do it, you fail, you give up. Moving on... "
        )
    else:
        print("You did it! You successfully climbed the wall into the castle.")
        inside_castle()


def try_digging_a_tunnel():
    """Try digging a tunnel under the wall."""
    print(
        "After a couple of hours of digging you realise that's kind of a dumb idea, you're not making relevant progress here. You are too exhausted now to try anyting else."
    )
    return False


# Remember not all players may have chosen the lockpicking set,
# see below how I manage this.
def try_picking_lock():
    """Try picking the lock with your lockpicking set."""
    print(
        "You did it! You successfully pick the lock and casually stroll into the castle."
    )
    inside_castle()


# I initialize the prompt here only with the options I want to
# display for *ALL* players, but I don't call any prompting methods
# on it (yet).
how_to_get_in_castle = InqExList(
    "How will you attempt to get into the castle?",
    [try_climbing_wall, try_digging_a_tunnel, dont_bother],
)

# Here the membership check on the backpack determines whether or not
# the `try_picking_lock` function should be given as an option.
if "lockpicking set" in backpack:
    # Since I find it logically to keep the `dont_bother` function
    # as the last option, I don't just add (+) the function, but
    # rather use the `insert` method to insert the option at the
    # second-to-last place.
    how_to_get_in_castle.insert(2, try_picking_lock)

# After this is done I prompt the player and fate
# decides if they get into the castle.
# (What happens in the castle we have already defined above.)
how_to_get_in_castle.prompt_and_execute()
