"""
Doctests ought not to have more than 80 lines
They also may mark for doctests exemples

Inheritance ====================
Used for some hierarquy in classes.
Then we make slight changes from its parent class.
The default does not inherite methods, but it can be done.

raise NotImplementederror   #cria um erro na sua rotina

from datetime import date

In the exemple she created an abstract (mother) class, which should not be
implemented
-This means we can only call child classes

Reflexion: code that looks upon its code

Abstract class:
It defines something that all types of employees must have (name, age, emp. id, etc)

SalariedEmployee is-a Employee

This must be defined as this:

class SalariedEmployee(Employee)

One very important thing: both share the same id (mother and child)
________________________________
| id76 |            | Employee |
--------            -----------|
|                              |
--------------------------------
|            |SalariedEmployee |
|             -----------------|
|                              |
--------------------------------

All classes are a descendent of the class Object.

"""
from typing import Dict, Tuple


class Mother_Brain:
    """
    A terrible creature whose telepatic abilities enable itself to control space
    pirates
    """
    _mental_controlled_creatures: Dict[str id, 'Alien']
    size: int
    weigth: int

    def __init__(self) -> None:
        """
        She initializes as a baby, wieghing only 4 pounds and with a height of
        3 feet
        """
        self._mental_controlled_creatures = {}

class Alien:
    """
    Usually dark lesser creatures susceptable to Mother Brain's mind control

    """
    size: int
    height: int

    def __init__(self) -> None:



