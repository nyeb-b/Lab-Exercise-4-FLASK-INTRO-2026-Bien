"""Small data-structure examples used by the Flask app."""


class Node:
    """One item in a singly linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None

#Linkedlist
class LinkedList:
    """A singly linked list with the operations used in the lab."""

    def __init__(self, values=None):
        self.head = None
        self.length = 0
        for value in values or []:
            self.append(value)

    def append(self, value):
        """Add a value to the end of the list."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self.length += 1

    def prepend(self, value):
        """Add a value to the beginning of the list."""
        node = Node(value)
        node.next = self.head
        self.head = node
        self.length += 1

    def remove(self, value):
        """Remove the first matching value and report whether it was found."""
        previous = None
        current = self.head
        while current is not None:
            if current.value == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                self.length -= 1
                return True
            previous, current = current, current.next
        return False

    def pop_front(self):
        """Remove and return the first value, or None when the list is empty."""
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        self.length -= 1
        return value

    def find(self, value):
        """Return a value's position, or None when it is not in the list."""
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return None

    def clear(self):
        """Remove every value from the list."""
        self.head = None
        self.length = 0

    def to_list(self):
        """Return the linked-list values in order."""
        values = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values


#Stack
class Stack:
    """A last-in, first-out (LIFO) stack backed by a Python list."""

    def __init__(self, values=None):
        self._items = list(values or [])

    @property
    def length(self):
        """Return the number of values in the stack."""
        return len(self._items)

    def is_empty(self):
        """Return True when the stack has no values."""
        return not self._items

    def push(self, value):
        """Place a value on top of the stack."""
        self._items.append(value)

    def pop(self):
        """Remove and return the top value, or None when the stack is empty."""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        """Return the top value without removing it."""
        if self.is_empty():
            return None
        return self._items[-1]

    def to_list(self):
        """Return a copy of the stack from bottom to top."""
        return list(self._items)
