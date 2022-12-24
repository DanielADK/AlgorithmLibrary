from enum import Enum
from typing import TypeVar, Generic


class Color(Enum):
    """
    An Enum which represents 2 possible colors of node

    ...
    """
    RED = 1
    BLACK = 0


T = TypeVar('T')


# > A node in a binary tree that can hold any type of data
class Node(Generic[T]):
    """
    A class to represent a node of tree.

    ...

    Attributes
    ----------
    __color : Color
        color of the node
    __key : TypeVar
        key value of T datatype
    __left_child : Node | None
        left child of the node
    __right_child : Node | None
        right child of the node
    __parent : Node | None
        parent of the node
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, value: T) -> None:
        self.__color: Color = Color.RED
        self.__key: T = value
        self.__left_child: Node | None = None
        self.__right_child: Node | None = None
        self.__parent: Node | None = None

    @property
    def color(self) -> Color:
        return self.__color

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
    """
    A class that represent type of binary search tree - Red-black tree

    ...

    Attributes
    ----------
    __nil : Node
        Node which represents NULL node
    __root : Node[T]
        Root of the tree

    Methods
    -------
    insert(value: T)
        Inserts value of datatype T into the tree
    remove(value: T)
        Removes value of datatype T from the tree
    search(value: T)
        Search for value of datatype T in the tree
    minimum()
        Returns minimum value in the tree
    maximum()
        Return maximum value in the tree
    """

    def __init__(self) -> None:
        """
        It initializes the tree.
        """
        self.__nil = Node(0)
        self.__nil.color = Color.BLACK
        self.__nil.left_child = None
        self.__nil.right_child = None
        self.__root: Node[T] = self.__nil

    def insert(self, value: T) -> None:
        """
        We start at the root and traverse down the tree until we find the correct place to insert
        the new node.

        The first thing we do is create a new node with the value we want to insert.
        We then set the parent of the new node to None, and the left and right children
        to the NIL node. We also set the color of the new node to red.

        Next, we set the y_node variable to None and the x_node variable to the root of the tree.
        We then enter a while loop that will continue until we reach the NIL node.

        Inside the while loop, we set y_node to x_node and then check if the key of
        the new node is less than the key of the current node. If it is, we set x_node
        to the left child of the current node. Otherwise, we set x_node to the
        right child of the current node.

        Once we reach the NIL node, we set the parent

        :param value: The value to be inserted into the tree
        :type value: T
        :return: The node that is being returned is the node that is being inserted.
        """
        node = Node(value)
        node.parent = None
        node.left_child = self.__nil
        node.right_child = self.__nil
        node.color = Color.RED

        y_node = None
        x_node = self.__root

        while x_node != self.__nil:
            y_node = x_node
            if node.key < x_node.key:
                x_node = x_node.left_child
            else:
                x_node = x_node.right_child

        node.parent = y_node
        if y_node is None:
            self.__root = node
        elif node.key < y_node.key:
            y_node.left_child = node
        else:
            y_node.right_child = node

        if node.parent is None:
            node.color = Color.BLACK
            return

        if node.parent.parent is None:
            return

        self.__insert_balance(node)

    def remove(self, value: T) -> None:
        """
        If the value is in the tree, remove it

        :param value: The value to remove from the tree
        :type value: T
        """
        self.__remove_from_tree(self.__root, value)

    def contains(self, key: T) -> bool:
        """
        If the key is in the tree, return True, otherwise return False

        :param key: The key to search for
        :type key: T
        :return: The value of the key.
        """
        return self.__find_value(self.__root, key) is not self.__nil

    def minimum(self, node: Node) -> Node:
        """
        It returns the minimum value in the tree.

        :param node: The node to start the search from
        :type node: Node
        :return: The minimum value in the tree.
        """
        while node.left_child != self.__nil:
            node = node.left_child
        return node

    def maximum(self, node: Node) -> Node:
        """
        It returns the maximum node in the tree.

        :param node: The node to start the search from
        :type node: Node
        :return: The maximum value in the tree.
        """
        while node.right_node != self.__nil:
            node = node.right_node
        return node

    def __find_value(self, node: Node, key: T) -> Node:
        """
        If the key is not found, return the node that would be the parent
        of the key if it were inserted into the tree

        :param node: The node to start searching from
        :type node: Node
        :param key: The key to search for
        :type key: T
        :return: The node that contains the key.
        """
        if node is self.__nil or key is node.key:
            return node

        if key < node.key:
            return self.__find_value(node.left_child, key)
        return self.__find_value(node.right_child, key)

    def __remove_from_tree(self, node: Node, key: T) -> None:
        """
        We find the node to be removed, then we find its successor, and then
        we replace the node to be removed with its successor

        :param node: The node to start searching from
        :type node: Node
        :param key: The key to be removed from the tree
        :type key: T
        :return: The node with the minimum key in the tree.
        """
        z_node = self.__nil
        while node is not self.__nil:
            if node.key is key:
                z_node = node

            if node.key <= key:
                node = node.right_child
            else:
                node = node.left_child

        if z_node is self.__nil:
            # Value is not in the tree
            return

        y_node = z_node
        y_color = y_node.color
        if z_node.left_child is self.__nil:
            x_node = z_node.right_child
            self.__rb_transplant(z_node, z_node.right_child)
        elif z_node.right_child is self.__nil:
            x_node = z_node.left_child
            self.__rb_transplant(z_node, z_node.left_child)
        else:
            y_node = self.minimum(z_node.right_child)
            y_color = y_node.color
            x_node = y_node.right_child
            if y_node.parent is z_node:
                x_node.parent = y_node
            else:
                self.__rb_transplant(y_node, y_node.right_child)
                y_node.right_child = z_node.right_child
                y_node.right_child.parent = y_node

            self.__rb_transplant(z_node, y_node)
            y_node.left_child = z_node.left_child
            y_node.left_child.parent = y_node
            y_node.color = z_node.color
        if y_color is Color.BLACK:
            self.__remove_balance(x_node)

    def __remove_balance(self, x_node: Node) -> None:
        """
        If the node to be removed is black, then we need to rebalance the tree

        :param x_node: The node to be removed
        :type x_node: Node
        """
        while x_node is not self.__root and x_node.color is Color.BLACK:
            if x_node is x_node.parent.left_child:
                s_node = x_node.parent.right_child
                if s_node.color is Color.RED:
                    s_node.color = Color.BLACK
                    x_node.parent.color = Color.RED
                    self.__left_rotation(x_node.parent)
                    s_node = x_node.parent.right_child

                if s_node.left_child.color is Color.BLACK \
                        and s_node.right_child.color is Color.BLACK:
                    s_node.color = Color.RED
                    x_node = x_node.parent
                else:
                    if s_node.right_child.color is Color.BLACK:
                        s_node.left_child.color = Color.BLACK
                        s_node.color = Color.RED
                        self.__right_rotation(s_node)
                        s_node = x_node.parent.right_child

                    s_node.color = x_node.parent.color
                    x_node.parent.color = Color.BLACK
                    s_node.right_child.color = Color.BLACK
                    self.__left_rotation(x_node.parent)
                    x_node = self.__root
            else:
                s_node = x_node.parent.left_child
                if s_node.color is Color.RED:
                    s_node.color = Color.BLACK
                    x_node.parent.color = Color.RED
                    self.__right_rotation(x_node.parent)
                    s_node = x_node.parent.left_child

                if s_node.right_child.color is Color.BLACK \
                        and s_node.right_child.color is Color.BLACK:
                    s_node.color = Color.RED
                    x_node = x_node.parent
                else:
                    if s_node.left_child.color is Color.BLACK:
                        s_node.right_child.color = Color.BLACK
                        s_node.color = Color.RED
                        self.__left_rotation(s_node)
                        s_node = x_node.parent.left_child
                    s_node.color = x_node.parent.color
                    x_node.parent.color = Color.BLACK
                    s_node.left_child.color = Color.BLACK
                    self.__right_rotation(x_node.parent)
                    x_node = self.__root
        x_node.color = Color.BLACK

    def __rb_transplant(self, x_node: Node, y_node: Node) -> None:
        """
        If the node to be replaced is the root, then the replacement node becomes the root.
        Otherwise, the replacement node takes the place of the node to be replaced

        :param x_node: The node to be removed
        :type x_node: Node
        :param y_node: the node that will replace x
        :type y_node: Node
        """
        if x_node.parent is None:
            self.__root = y_node
        elif x_node is x_node.parent.left_child:
            x_node.parent.left_child = y_node
        else:
            x_node.parent.right_child = y_node
        y_node.parent = x_node.parent

    def print(self):
        """
        The function takes in a node, a string, and a boolean. It then prints the node's value,
        and then calls itself on the left and right children of the node,
        passing in the string and boolean
        """
        self.__print_tree(self.__root, "", True)

    def __print_tree(self, node: Node, indent, last: bool) -> None:
        """
        If the node is not the NIL node, print the node's key and color,
        then recursively print the left and right subtrees

        :param node: The node to print
        :type node: Node
        :param indent: This is the indentation string that is used to print the tree
        :param last: A boolean value that indicates whether the current node
        is the last child of its parent
        :type last: bool
        """
        if node != self.__nil:
            print(indent, end=' ')
            if last:
                print("└─(R)────", end=' ')
                indent += "     "
            else:
                print("├─(L)────", end=' ')
                indent += " │ "

            print(str(node.key) + " (" + ("RED" if node.color == Color.RED else "BLACK") + ")")
            self.__print_tree(node.left_child, indent, False)
            self.__print_tree(node.right_child, indent, True)

    def __insert_balance(self, x_node: Node) -> None:
        """
        It inserts a node into the tree and then balances the tree

        :param x_node: Node
        :type x_node: Node
        """
        while x_node.parent.color is Color.RED:
            if x_node.parent is x_node.parent.parent.right_child:
                y_node = x_node.parent.parent.left_child
                if y_node.color is Color.RED:
                    y_node.color = Color.BLACK
                    x_node.parent.color = Color.BLACK
                    x_node.parent.parent.color = Color.RED
                    x_node = x_node.parent.parent
                else:
                    if x_node is x_node.parent.left_child:
                        x_node = x_node.parent
                        self.__right_rotation(x_node)
                    x_node.parent.color = Color.BLACK
                    x_node.parent.parent.color = Color.RED
                    self.__left_rotation(x_node.parent.parent)
            else:
                y_node = x_node.parent.parent.right_child
                if y_node.color is Color.RED:
                    y_node.color = Color.BLACK
                    x_node.parent.color = Color.BLACK
                    x_node.parent.parent.color = Color.RED
                    x_node = x_node.parent.parent
                else:
                    if x_node is x_node.parent.right_child:
                        x_node = x_node.parent
                        self.__left_rotation(x_node)
                    x_node.parent.color = Color.BLACK
                    x_node.parent.parent.color = Color.RED
                    self.__right_rotation(x_node.parent.parent)
            if x_node is self.__root:
                break
        self.__root.color = Color.BLACK

    def __left_rotation(self, x_node: Node) -> None:
        """
        "Rotate the subtree rooted at `x` to the left."

        The first line of the function is a docstring. This is a special type of comment
        that is used to document the function. It is a good idea to include a docstring
        for every function you write

        :param x_node: Node
        :type x_node: Node
        """
        y_node = x_node.right_child
        x_node.right_child = y_node.left_child
        if y_node.left_child is not self.__nil:
            y_node.left_child.parent = x_node

        y_node.parent = x_node.parent
        if x_node.parent is None:
            self.__root = y_node
        elif x_node is x_node.parent.left_child:
            x_node.parent.left_child = y_node
        else:
            x_node.parent.right_child = y_node
        y_node.left_child = x_node
        x_node.parent = y_node

    def __right_rotation(self, x_node: Node) -> None:
        """
        "Rotate the subtree rooted at `x` to the right."

        The function is a bit long, but it's not too hard to understand.
        The first thing it does is to save the left child of `x` in a variable called `y`.
        Then it sets the left child of `x` to be the right child of `y`. Finally, it sets
        the right child of `y` to be `x`

        :param x_node: Node
        :type x_node: Node
        """
        y_node = x_node.left_child
        x_node.left_child = y_node.right_child
        if y_node.right_child is not self.__nil:
            y_node.right_child.parent = x_node

        y_node.parent = x_node.parent
        if x_node.parent is None:
            self.__root = y_node
        elif x_node is x_node.parent.right_child:
            x_node.parent.right_child = y_node
        else:
            x_node.parent.left_child = y_node
        y_node.right_child = x_node
        x_node.parent = y_node
