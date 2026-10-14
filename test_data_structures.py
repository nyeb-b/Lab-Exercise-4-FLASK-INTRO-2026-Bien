import unittest

from data_structures import LinkedList, Stack


class LinkedListTests(unittest.TestCase):
    def test_list_actions_keep_values_in_order(self):
        linked_list = LinkedList(["Flask"])

        linked_list.prepend("HTML")
        linked_list.append("CSS")

        self.assertEqual(linked_list.to_list(), ["HTML", "Flask", "CSS"])
        self.assertEqual(linked_list.find("Flask"), 1)
        self.assertTrue(linked_list.remove("Flask"))
        self.assertEqual(linked_list.pop_front(), "HTML")


class StackTests(unittest.TestCase):
    def test_stack_returns_the_latest_value_first(self):
        stack = Stack()
        stack.push("first")
        stack.push("last")

        self.assertEqual(stack.peek(), "last")
        self.assertEqual(stack.pop(), "last")
        self.assertEqual(stack.to_list(), ["first"])

    def test_empty_stack_pop_and_peek_return_none(self):
        stack = Stack()

        self.assertIsNone(stack.pop())
        self.assertIsNone(stack.peek())
        self.assertTrue(stack.is_empty())


if __name__ == "__main__":
    unittest.main()
