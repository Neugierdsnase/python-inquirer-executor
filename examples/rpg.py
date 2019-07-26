# -*- coding: utf-8 -*-

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
# grouping them in a module or in a class

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


# These functions will be used to choose a weapon
def choose_ax():
    """Ax"""
    return "Ax"


def choose_sword():
    """Sword"""
    return "Sword"


def choose_mace():
    """Mace"""
    return "Mace"


class Hero:
    def __init__(self, hp=100, atk=11):
        self.name = prompt([Text("name", message="How may I address you?")])
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

backpack = InqExCheckbox(
    """Available items:""",
    [choose_lockpicking_set, choose_map, choose_oil_lamp, choose_healing_potion],
).prompt_and_execute()

print(
    "You are now being sent on your way and would you believe it, right outside the cities gate a monster already blocks your way."
)

print(
    "You have {} items in your backback that are wearing you down, so you have {} attack points.".format(
        len(backpack), hero.atk - len(backpack)
    )
)

monster1 = dict(hp=20, atk=5, name="the spider-like creature")


def attack(monster):
    """Attack the monster"""
    monster["hp"] -= hero.atk
    if not monster["hp"] > 0:
        print("The monster died. You won the fight like only a true hero could.")
        return False
    else:
        print(
            "You attack {} with your {} and apply {} damage. It has {} HP left.".format(
                monster["name"], hero.weapon, hero.atk, monster["hp"]
            )
        )
        hero.hp -= monster["atk"]
        print(
            "The monster attacks you and applies {} damage. You have {} HP left.".format(
                monster["atk"], hero.hp
            )
        )
        return True


def flee(monster):
    """Flee"""
    print("You ran away like a coward.")
    return False


while True:
    choice = InqExList("What do you do?", [attack, flee]).prompt_and_execute(monster1)
    if not choice:
        break
