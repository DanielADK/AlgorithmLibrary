from Structures import Node


class Edge:
    def __init__(self, a: Node, b: Node) -> None:
        self.__first: Node = a
        self.__second: Node = b

    @property
    def first(self) -> Node:
        return self.__first

    @first.setter
    def first(self, node: Node) -> None:
        self.__first = node

    @property
    def second(self) -> Node:
        return self.__second

    @second.setter
    def second(self, node: Node) -> None:
        self.__second = node
