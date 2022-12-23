from unittest import TestCase
import random
from AlgorithmLibrary.RedBlackTree import RedBlackTree


class TestRedBlackTree(TestCase):
    def test_insert(self):
        test_set: set[int] = set()
        rbt = RedBlackTree[int]()

        [test_set.add(i) for i in range(1, 20)]
        [rbt.insert(i) for i in range(1, 20)]

        test_list = list(test_set)
        random.shuffle(test_list)

        for num in test_list:
            self.assertTrue(rbt.contains(num))
            rbt.remove(num)
            self.assertFalse(rbt.contains(num))
            rbt.insert(num)
            self.assertTrue(rbt.contains(num))
            rbt.remove(num)
            self.assertFalse(rbt.contains(num))
