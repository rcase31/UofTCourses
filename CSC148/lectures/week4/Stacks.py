class SStack:

    # ==== Private Attributes ====
    # The items in stack
    # _items: List
    _items: 'List'
    def __init__(self):
        self._items = []

    def push(self, item: object):
        self._items.append(item)

    def pop(self) -> object:
        return self.pop()
