"""
Class notes

She is talking about the two types of employees and about the superclasses and
subclasses.

Ticking-time-bomb method: something that must be substituted.
-Remember that the ticking-time-bomb method has that "raise NotImplementedError"

We can also use the abstract class as an input!! This is very important

4 cases of inheritance
-Complete
-Inherit (no changes)
-Replace
-Extend

Use long names
    "hours_per_name"

Important detail:subclasses don't always have an __init__ method
    It is important to have though.
    And this can be done for both parent and child classes

About the __init__ method
    If we are to call the parents init
        Employee.__init__(self, id, name)
    By default only the child __init__ is called
        but we may call the parents __init__ class


"""
"""Inheritance Example: Companies and Employees

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains an illustration of *inheritance* through an abstract
Employee class that defined a common interface for all of its subclasses.

We illustrate the benefit of inheritance in the simple Company class,
which stores different types of employees.

NOTE: This is an incomplete version of this week's code.
We'll update this code after Wednesday's lecture.



"""
from datetime import date


class Employee:
    """An employee of a company.

    This is an abstract class. Only child classes should be instantiated.

    === Public attributes ===
    id_:
    name:
    pay_history:
    === Representation invariants ===

    """
    id_: int
    name: str
    pay_history: Dict[date, int]

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.
        """
        raise NotImplementedError

    def pay(self, pay_date: date) -> None:
        """Pay this Employee on the given date and record the payment.

        (Assume this is called once per month.)
        """
        payment = self.get_monthly_payment()
        print(f'An employee was paid {payment} on {pay_date}.')


class SalariedEmployee(Employee):
    """An employee whose pay is computed based on an annual salary.
    === Public Attributes ===
    salary:
        the amount this employee earns in a year

    """
    salary: float
    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.
        """
        return self.salary / 12

    def pay(self, pay_date: date) -> None:
        """(Illustrate method overriding.)"""
        print('Payment rejected! Mwahahahaha.')


class HourlyEmployee(Employee):
    """An employee whose pay is computed based on an hourly rate.
    === Public attributes ===
    hours_per_month:
        the number of hours this employee works in a month
    hourly_wage:
        the amount this employee earns in an hour

    === Representation invariants ===
    - hourly_wage > 0
    - hours_per_month >0
    """
    hours_per_hour: float
    hourly_wage:  float

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.
        """
        return self.hours_per_hour * self.hourly_wage

    def pay(self, pay_date: date) -> None:
        """(Illustrate method overriding.)"""
        Employee.pay(self, pay_date)
        print('Payment accepted! Have a nice day. :)')


if __name__ == '__main__':
    employees = [
        SalariedEmployee(),
        HourlyEmployee(),
        SalariedEmployee()
    ]

    for employee in employees:
        employee.pay(date(2017, 9, 30))
