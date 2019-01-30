from typing import List, Generic

class PriorityQueue(object):
    _queue: List[int]
    _list_elements_address: List[int]
    def __init__(self):
        # We need to initialize any property of this class, independently of
        # whether is going to be or not used.
        self._queue = []
        self._list_elements_address = []
    def insert(self, element: object):
        _counter = 0
        for _item in self._queue[::]:
            if element < _item:
                self._queue.insert(_counter, element)
                return
            _counter += 1
        self._queue.insert(_counter, element)

    def remove(self)-> object:
        return self._queue.pop()

    def gen_address_list(self)-> None:
        self._list_elements_address = []
        for element in self._queue:
            self._list_elements_address.append(id(element))


class Normal_Queue(object):
    _queue: List[int]
    def __init__(self):
        self._queue = []
    def enqueue(self, elementIn: object):
        self._queue.insert(0,elementIn)
    def dequeue(self)->object:
        return self._queue.pop()
    def is_empty(self)->bool:
        return len(self._queue) == 0
    def __len__(self)->int:
        re_queue = Normal_Queue()
        counter = 0
        while not self.is_empty():
            re_queue.enqueue(self.dequeue())
            counter += 1
        while not re_queue.is_empty():
            self.enqueue(re_queue.dequeue())
        return counter

class DoubleQueue(Normal_Queue):
    def __init__(self, is_special):
        Normal_Queue.__init__(self)
        self.is_special = is_special

    def enqueue(self, elementIn: object):
        Normal_Queue.enqueue(self, elementIn)
        if self.is_special(elementIn):
            Normal_Queue.enqueue(self, elementIn)

def is_special(word: str)->bool:
    list_of_words =  ['boo', 'cow', 'bull']
    return word in list_of_words

class Stack(object):
    _stack_list: List[object]
    def __init__(self):
        self._stack_list = []
    def insert(self, item: object):
        self._stack_list.append(item)
    def pop(self)-> object:
        return self._stack_list.pop()
    def is_empty(self)-> bool:
        return len(self._stack_list) == 0
    def __len__(self)->int:
        aux_stack = Stack()
        counter = 0
        while not self.is_empty():
            aux_stack.insert(self._stack_list.pop())
            counter += 1
        while not aux_stack.is_empty():
            self.insert(aux_stack.pop())
        return counter

class Node(object):

    def __init__(self, item: object):
        self.cargo = item
        self.next = None
    def __str__(self)->object:
        return self.cargo

class Linked_List(object):
    _first: Node
    def __init__(self, item: Node):
        self._first = Node(item)
    def insert(self, item: Node):
        prev = None
        curr = self._first
        while curr is not None:
            prev = curr
            curr = curr.next
        prev.next = Node(item)

    def insert_at(self, position: int, item: Node):
        prev = None
        curr = self._first
        counter = 0
        while curr is not None and position != counter:
            prev = curr
            curr = curr.next
        if position == counter:
            item.next = curr
            prev.next = item
            return
        if curr is None:
            raise IndexError

    def __len__(self)->int:
        counter = 0
        curr = self._first
        while curr is not None:
            counter += 1
            curr = curr.next
        return counter

    def __str__(self)-> str:
        str_temp = " -> "
        lst_temp = []
        curr = self._first
        while curr is not None:
            lst_temp.append(str(curr))
            curr = curr.next
        str_temp.join(lst_temp)
        str_temp = "[" + str_temp + "]"
        return str_temp

    def __getitem__(self, key) -> Node:
        curr = self._first
        counter = 0
        while curr is not None and counter != key:
            curr = curr.next
            counter += 1
        if curr is not None:
            return curr
        else:
            raise IndexError

def deplete(s: Stack):

    new_stack = Stack()
    while not s.is_empty():
        new_stack.insert(s.pop())
    s = new_stack


def second(entrada: int):

    entrada = 19

def prima():

    cuidado = 10
    second(cuidado)
    print(cuidado)


