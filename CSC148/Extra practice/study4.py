def quicksort(lst) -> list:

    if len(lst) < 2:
        return lst[:]

    pivot = lst[0]

    smaller, bigger = _partition(pivot, lst[1:])

    smaller = quicksort(smaller)
    bigger = quicksort(bigger)

    return smaller + [pivot] + bigger

def _partition(pivot: int, lst: list)->(list, list):

    smaller = []
    bigger = []

    for item in lst:
        if item < pivot:
            smaller.append(item)
        else:
            bigger.append(item)

    return smaller, bigger

def mergesort(lst) -> list:

    if len(lst) < 2:
        return lst[:]

    mid = len(lst)//2

    chunk1 = lst[:mid]
    chunk2 = lst[mid:]

    chunk1 = mergesort(chunk1)
    chunk2 = mergesort(chunk2)

    return _merged(chunk1, chunk2)


def _merged(lst1, lst2)-> list:
    index1 = 0
    index2 = 0

    merged = []
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] > lst2[index2]:
            merged.append(lst2[index2])
            index2 += 1
        else:
            merged.append(lst1[index1])
            index1 += 1

    return merged + lst1[index1:] + lst2[index2:]
