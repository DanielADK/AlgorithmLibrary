import string
from unittest import TestCase
import random
from AlgorithmLibrary.red_black_tree import RedBlackTree


class TestRedBlackTree(TestCase):
    def test_int_insert(self):
        rbt = RedBlackTree[int]()

        count: int = 20_000
        test_list: list[int] = random.sample(range(-count, count), count)

        for num in test_list:
            rbt.insert(num)
            self.assertTrue(rbt.contains(num))

    def test_str_insert(self):
        test_list: list[str] = []
        rbt = RedBlackTree[str]()

        # Generate random strings
        letters: str = string.ascii_letters+string.digits+string.punctuation
        for _ in range(20_000):
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

    def test_deny_multitype(self):
        rbt = RedBlackTree[str]()
        with self.assertRaises(TypeError):
            rbt.insert(1)
            rbt.insert(list("1"))
            rbt.insert(tuple("1"))
            rbt.insert(tuple(1))
            rbt.insert(dict({"a": 1}))
            rbt.insert(True)
        rbt.insert("apple")
        self.assertTrue(rbt.contains("apple"))

    def test_to_list(self):
        test_int_list: list[int] = []
        rbt = RedBlackTree[int]()

        count: int = 20_000
        test_int_list = random.sample(range(-count, count), count)

        for i in test_int_list:
            rbt.insert(i)

        self.assertEqual(rbt.to_list(), sorted(test_int_list))

        test_str_list: list[str] = []
        rbts = RedBlackTree[str]()
        letters: str = string.ascii_letters+string.digits+string.punctuation
        for _ in range(2_000):
            length = random.randint(5, 200)
            result: str = ''.join(random.choice(letters) for _ in range(length))
            test_str_list.append(result)
            rbts.insert(result)

        self.assertEqual(rbts.to_list(), sorted(test_str_list))

    def test_size(self):
        rbt = RedBlackTree[int]()
        self.assertTrue(rbt.size == 0)

        count: int = 1_000
        test_list: list[int] = random.sample(range(-count, count), count)

        count = 0
        for i in test_list:
            rbt.insert(i)
            count += 1

            self.assertTrue(rbt.size == count)

        for i in test_list:
            if random.randint(0, 3) == 1:
                rbt.remove(i)
                self.assertFalse(rbt.size == count)
                count -= 1
                self.assertTrue(rbt.size == count)
