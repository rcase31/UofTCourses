"""CSC148 Exercise 6: Binary Search Trees Practice

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for Exercise 6.

You are responsible for completing three BinarySearchTree methods in this file.

Note: there's only one Task for this exercise.
"""
from typing import List, Optional, Tuple


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every node, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[object]
    # The left subtree, or None if the tree is empty
    _left: Optional['BinarySearchTree']
    # The right subtree, or None if the tree is empty
    _right: Optional['BinarySearchTree']

    # === Representation Invariants ===
    #  - If _root is None, then so are _left and _right.
    #    This represents an empty BST.
    #  - If _root is not None, then _left and _right are BinarySearchTrees.
    #  - (BST Property) All items in _left are <= _root,
    #    and all items in _right are >= _root.

    def __init__(self, root: Optional[object]) -> None:
        """Initialize a new BST with the given root value and no children.

        If <root> is None, make an empty tree, with subtrees that are None.
        If <root> is not None, make a tree with subtrees are empty trees.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def __contains__(self, item: object) -> bool:
        """Return True if <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left   # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    def height(self) -> int:
        """Return the height of this BST.

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        if self.is_empty():
            return 0
        else:
            return max(self._left.height(), self._right.height()) + 1

    def insert(self, item: object) -> None:
        """Insert <item> into this BST, maintaining the BST property.

        Do not change positions of any other nodes.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        if self.is_empty():
            # Make new leaf node.
            # Note that self._left and self._right cannot be None if the
            # tree is non-empty! (This is one of our invariants.)
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item <= self._root:
            self._left.insert(item)
        else:
            self._right.insert(item)


##############################################################################
# Task 1: More BST practice
##############################################################################
    # TODO: Implement this method!
    def num_less_than(self, item: object) -> int:
        """Return the number of items in this BST that are less than <item>.
        """
        counter = 0
        if self.is_empty():
            return 0
        else:
            if self._root < item:
                counter += 1
            counter += self._right.num_less_than(item)
            counter += self._left.num_less_than(item)
        return counter

    # TODO: Implement this method!
    def items_at_depth(self, d: int) -> list:
        """Return a sorted list of all items in this BST at depth <d>.

        Precondition: d >= 1.

        Reminder: you should not have to use the built-in 'sort' method
        or do any sorting yourself.
        """
        temp_list = []
        if self._root is None:
            return temp_list
        if d == 1:
            temp_list.append(self._root)
        else:
            temp_list.extend(self._right.items_at_depth(d))
            temp_list.extend(self._left.items_at_depth(d))
        return temp_list
    # TODO: Implement this method!
    def levels(self) -> List[Tuple[int, list]]:
        """Return a list of items in the tree, separated by level.

        You may wish to use 'items_at_depth' as a helper method,
        but this also makes your code less efficient. Try doing
        this method twice, once with 'items_at_depth', and once
        without it!
        >>> bst = BinarySearchTree(10)
        >>> bst.insert(1)
        >>> bst.insert(2)
        >>> bst.insert(3)
        >>> bst.insert(6)
        >>> bst.insert(2)
        >>> bst.levels()
        """
        # levels_list = []
        # for depth in range(1,self.height()+1):
        #     levels_list.append((depth, self.items_at_depth(depth)))
        # return levels_list

        # if self._root is None:
        #     return []
        # else:
        #     levels_list = self.helper_levels()

        # return levels_list

        if self.is_empty():
            return []
        else:
            output_list = [(1, [self._root])]

            left_output = self._left.levels()
            right_output = self._right.levels()


            # On this case we strip the output of the tuples and get only the lists
            left_list = []
            for item in left_output:
                left_list.append(item[1])

            right_list = []
            for item in right_output:
                right_list.append(item[1])

            # Now we must merge the two lists
            i = 0
            merged = []
            left_size = len(left_list)
            right_size = len(right_list)
            while i < left_size and i < right_size:
                merged.append(left_list[i] + right_list[i])
                i += 1
            # we add up the remaining part of the bigger list
            if right_size > left_size:
                merged += right_list[i:]
            elif left_size != 0: # just one check to avoid indexing on and empty list
                merged += left_list[i:]

            i = 2
            for level in merged:
                output_list.append((i, level))
                i += 1

            return output_list


            # i = 0
            # while i < len(left):
            #     temp = left[i]
            #     temp = temp[1]
            #     output_list.append((i+2, temp))
            #     i += 1
            #
            # i = 0
            # while i < len(right):
            #     temp = right[i]
            #     temp = temp[1]
            #     # Pensar no caso em que a outpulist tem tamanho 1, e eu preciso
            #     #  inserir no lugar um, (porque i eh 0),  entao len precisa na
            #     # verdade ser 2 ne?
            #     if i < (len(output_list) - 1):
            #         temp2 = output_list[i + 1][1]
            #         output_list[i + 1] = ((i + 2, temp + temp2))
            #     else:
            #         output_list.append((i+2, temp))
            #     i += 1
            #
            # return output_list



    def helper_levels(self, d: int) -> list:

        temp_list = []
        if self._root is None:
            return temp_list
        if d == 1:
            temp_list.append(self._root)
        else:
            temp_list.extend(self._right.items_at_depth(d))
            temp_list.extend(self._left.items_at_depth(d))
        return temp_list


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
