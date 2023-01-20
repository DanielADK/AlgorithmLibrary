from typing import TypeVar, Generic

T = TypeVar('T')


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
