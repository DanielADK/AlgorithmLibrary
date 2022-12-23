from enum import Enum
from typing import TypeVar, Generic


class Color(Enum):
    RED = 1
    BLACK = 0


T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, value: T) -> None:
        self.__color: Color = Color.RED
        self.__key: T = value
        self.__left_child: Node | None = None
        self.__right_child: Node | None = None
        self.__parent: Node | None = None

    @property
    def color(self) -> Color:
        return self.__key

    @color.setter
    def color(self, color: Color) -> None:
        self.__color = color

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


class RedBlackTree(Generic[T]):
    def __init__(self) -> None:
        self.__root: Node[T] | None = None

    def insert(self, value: T) -> None:
        node = Node(value)

        y = None
        x = self.__root

        while x is not None:
            y = x
            if node.key < x.key:
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

        if node.parent is None:
            node.color = Color.BLACK
            return

        if node.parent.parent is None:
            return

        self.__insert_balance(node)

    def __insert_balance(self, x: Node) -> None:
        while x.parent.color is Color.RED:
            if x.parent is x.parent.parent.right_child:
                y = x.parent.parent.left_child
                if y.color is Color.RED:
                    y.color = Color.BLACK
                    x.parent.color = Color.BLACK
                    x.parent.parent.color = Color.RED
                    x = x.parent.parent
                else:
                    if x is x.parent.left_child:
                        x = x.parent
                        self.__right_rotation(x)
                    x.parent.color = Color.BLACK
                    x.parent.parent.color = Color.RED
                    self.__left_rotation(x.parent.parent)
            else:
                y = x.parent.parent.right_child
                if y.color is Color.RED:
                    y.color = Color.BLACK
                    x.parent.color = Color.BLACK
                    x.parent.parent.color = Color.RED
                    x = x.parent.parent
                else:
                    if x is x.parent.right_child:
                        x = x.parent
                        self.__left_rotation(x)
                    x.parent.color = Color.BLACK
                    x.parent.parent.color = Color.RED
                    self.__right_rotation(x.parent.parent)
            if x is self.__root:
                break
        self.__root.color = Color.BLACK

    def __left_rotation(self, x: Node) -> None:
        y = x.right_child
        x.right_child = y.left_child
        if y.left_child is not None:
            y.left_child.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.__root = y
        elif x is x.parent.left_child:
            x.parent.left_child = y
        else:
            x.parent.right_child = y
        y.left_child = x
        x.parent = y

    def __right_rotation(self, x: Node) -> None:
        y = x.left_child
        x.left_child = y.right_child
        if y.right_child is not None:
            y.right_child.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.__root = y
        elif x is x.parent.right_child:
            x.parent.right_child = y
        else:
            x.parent.left_child = y
        y.right_child = x
        x.parent = y

