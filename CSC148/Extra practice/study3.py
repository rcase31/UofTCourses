import random
from typing import List

class Spreadsheet:
    """"""

    _values: List[List[int]]
    _headers: List[str]

    def __init__(self, headers: List[str]):
        self._headers = [header for header in headers]
        self._values = []

    def insert_row(self, row: List[int]):

        temp = []
        for i in range(len(self._headers)):
            temp.append(row[i])

        self._values.append(temp)

    def average(self, column)-> float:

        column -= 1
        sum = 0
        count = 0
        for row in self._values:
            sum += row[column]
            count += 1
        return sum/count
    def set_cell(self, cell: (int, int), value):
        row = cell[0] - 1
        column = cell[1] - 1
        self._values[row][column] = value

    def get_cell(self, cell: (int, int))-> float:
        row = cell[0] - 1
        column = cell[1] - 1
        return self._values[row][column]
    def defectus(self):
        self = Spreadsheet(['b'])


def mergesort(lst: list)->list:
    # This is a recursive method, so it must also have a base case
    if len(lst)< 2:
        return lst[:]
    else:
        mid = len(lst)//2
        left = mergesort(lst[:mid])
        right = mergesort(lst[mid:])

        return _merged(left, right)

def _merged(lst1, lst2)->list:
    # the rough work happens here!
    index1 = 0
    index2 = 0
    merged = []
    # iterar enquanto ambos estiverem dentro do limite... se um deles sair
    # desse limite, ja para de iterar!

    while index1<len(lst1) and index2<len(lst2):
        if lst1[index1]<=lst2[index2]:
            merged.append(lst1[index1])
            index1 += 1
        else:
            merged.append(lst2[index2])
            index2 += 1
    return merged + lst1[index1:] + lst2[index2:]

def quicksort(lst: list) -> list:
    """
    >>> quicksort([1,2,2,52,32,32,32,32,45,465,232,32,246,1,1,24,5])
    [1, 1, 1, 2, 2, 5, 24, 32, 32, 32, 32, 32, 45, 52, 232, 246, 465]

    """

    tamanho = len(lst)

    # if tamanho < 2:
    #     #this is the base case
    #     return lst[:]
    # else:
    #     pivot = lst[0]
    #     smaller, bigger = _partition(lst[1:], pivot)
    #
    #     smaller = quicksort(smaller)
    #     bigger = quicksort(bigger)
    #
    #     return smaller + [pivot] + bigger

    if tamanho < 2:
        #this is the base case
        return lst[:]
    else:
        pivot = lst[0]
        smaller, bigger = _partition(lst, pivot)

        smaller = quicksort(smaller)
        bigger = quicksort(bigger)

        return smaller + bigger



def _partition(lst: list, pivot: int):
    smaller = []
    bigger = []
    for element in lst:
        if element <= pivot:
            smaller.append(element)
        else:
            bigger.append(element)
    return smaller, bigger


def recursos(a: int):
    print(id(a))
    a += 1
    print(id(a))
    return a

def nested_sum(obj):

    sum = 0

    if isinstance(obj, int):
        sum += obj
    else:
        for lst_i in obj:
            nested_sum(lst_i)
        return sum


from typing import Union, List
def flatten_2000(lst)-> list:

    output = []
    if isinstance(lst, int):
        return [lst]
    else:
        for item in lst:
            output += flatten_2000(item)

    return output
