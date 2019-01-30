from typing import List

def uniques(obj)-> List[int]:
    """
    >>> uniques([13,[12, 13], 4])
    [13, 2, 4]
    >>> uniques([13,[13,13],13])
    [13]
    """
    if isinstance(obj, int):
        return [obj]
    else:
        answer = []
        for element in obj:
            for item in uniques(obj):
                if item not in answer:
                    answer.append(item)
        return answer


