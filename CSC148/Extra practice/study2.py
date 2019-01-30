from typing import Union, List

def flaten(lst: Union[List, int])->List:
    """
    This function flattens a list using recursive calls
    """
    if isinstance(lst, int):
        # This is our base case
        return [lst]
    else:
        new_list = []
        for element in lst:
            new_list.extend(flaten(element))
        return new_list
def xgcd(n, m):
    s1, s0, t1, t0, r1, r0 = 0, 1, 1, 0, m, n
    while r1 != 0:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        s0, s1 = s1, s0 - quotient * s1
        t0, t1 = t1, t0 - quotient * t1
    return(r0, s0, t0)

if __name__ == '__main__':
    xgcd(3, 2)
    xgcd(26, 4)
    xgcd(4, 26)
