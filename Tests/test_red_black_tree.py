import string
from unittest import TestCase
import random
from AlgorithmLibrary.red_black_tree import RedBlackTree


class TestRedBlackTree(TestCase):
    def test_int_insert(self):
        test_list: list[int] = []
        rbt = RedBlackTree[int]()

        count: int = 2_000
        test_list = random.sample(range(-count, count), count)

        for num in test_list:
            rbt.insert(num)
            self.assertTrue(rbt.contains(num))

    def test_str_insert(self):
        test_list: list[str] = []
        rbt = RedBlackTree[str]()

        # Generate random strings
        letters: str = string.ascii_letters + string.digits + string.punctuation
        for _ in range(2_000):
            length = random.randint(5, 200)
            result: str = ''.join(random.choice(letters) for _ in range(length))
            test_list.append(result)
            rbt.insert(result)

        # check if everything is inside the tree
        for sentence in test_list:
            self.assertTrue(rbt.contains(sentence))

        # check if non-added is not inside
        for _ in range(20):
            length = random.randint(5, 20)
            result: str
            while True:
                result = ''.join(random.choice(letters) for j in range(length))
                if result not in test_list:
                    break
            self.assertFalse(rbt.contains(result))



