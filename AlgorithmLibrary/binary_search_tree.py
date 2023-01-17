from typing import TypeVar, Generic

T = TypeVar('T')


def typeCheck(gen_class, value):
    if gen_class.__name__ != type(value).__name__:
        raise TypeError("Invalid datatype. Expected: "+
                        gen_class.__name__+
                        ", but got: "+
                        type(value).__name__)


class Node(Generic[T]):
    """

    Attributes
    ----------
    __key : TypeVar
        key value of T datatype
    __left_child : Node | None
        left child of the node
    __right_child : Node | None
        right child of the node
    __parent : Node | None
        parent of the node
    """

    def __init__(self, value: T) -> None:
        self.__key: T = value
        self.__left_child: Node | None = None
        self.__right_child: Node | None = None
        self.__parent: Node | None = None

    @property
    def key(self) -> T:
        return self.__key

    @key.setter
    def key(self, value: T) -> None:
        self.__key = value

    @property
    def left_child(self):
        return self.__left_child

    @left_child.setter
    def left_child(self, child) -> None:
        self.__left_child = child

    @property
    def right_child(self):
        return self.__right_child

    @right_child.setter
    def right_child(self, child) -> None:
        self.__right_child = child

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, child) -> None:
        self.__parent = child


class BinarySearchTree(Generic[T]):

    def __init__(self) -> None:
        self.size: int = 0
        self.__root: Node[T] | None = None

    def insert(self, key: T) -> bool:
        typeCheck(self.__orig_class__.__args__[0], key)

        if self.contains(key):
            return False

        self.size += 1

        node = Node(key)

        if self.__root is None:
            self.__root = node
            return True

        y = None
        x = self.__root

        while x is not None:
            y = x
            if node.key == x.key:
                break
            elif node.key < x.key:
                x = x.left_child
            else:
                x = x.right_child

        node.parent = y
        if y is None:
            self.__root = node
        elif node.key < y.key:
            y.left_child = node
        else:
            y.right_child = node
        return True

    def remove(self, key: T) -> None:

        typeCheck(self.__orig_class__.__args__[0], key)

        x = self.__find(self.__root, key)

        if x == self.__root:
            to_find = self.__root
        else:
            to_find = x.parent

        if x is None:
            return

        # If node has not any child
        if x.right_child is None and x.left_child is None:
            if to_find.left_child is x:
                to_find.left_child = None
            else:
                to_find.right_child = None
        # else if node has only right child
        elif x.right_child is None and x.left_child is not None:
            if to_find.left_child is x:
                to_find.left_child = x.left_child
            else:
                to_find.right_child = x.left_child
        # else if node has only left child
        elif x.right_child is not None and x.left_child is None:
            if to_find.left_child is x:
                to_find.left_child = x.right_child
            else:
                to_find.right_child = x.right_child
        # else if node has no children
        else:
            right_minimum = self.__minimum(x.right_child)
            self.remove(right_minimum.key)
            x.key = right_minimum.key
        self.size -= 1

    def contains(self, key: T) -> bool:
        return self.__find(self.__root, key) is not None

    def __find(self, x: Node, key: T) -> Node | None:
        while x is not None and key != x.key:
            if key < x.key:
                x = x.left_child
            else:
                x = x.right_child
        return x

    def __minimum(self, node: Node) -> Node:
        while node.left_child is not None:
            node = node.left_child
        return node
