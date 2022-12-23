from enum import Enum
from typing import TypeVar, Generic


class Color(Enum):
    RED = 1
    BLACK = 0


T = TypeVar('T')


# > A node in a binary tree that can hold any type of data
class Node(Generic[T]):
    def __init__(self, value: T) -> None:
        """
        This function creates a new node with the given value, and sets the color to red, the left and right children to
        None, and the parent to None

        :param value: The value of the node
        :type value: T
        """
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
    def __init__(self) -> None:
        """
        It initializes the tree.
        """
        self.__NIL = Node(0)
        self.__NIL.color = Color.BLACK
        self.__NIL.left_child = None
        self.__NIL.right_child = None
        self.__root: Node[T] = self.__NIL

    def insert(self, value: T) -> None:
        """
        We start at the root and traverse down the tree until we find the correct place to insert the new node.

        The first thing we do is create a new node with the value we want to insert. We then set the parent of the new node
        to None, and the left and right children to the NIL node. We also set the color of the new node to red.

        Next, we set the y variable to None and the x variable to the root of the tree. We then enter a while loop that will
        continue until we reach the NIL node.

        Inside the while loop, we set y to x and then check if the key of the new node is less than the key of the current
        node. If it is, we set x to the left child of the current node. Otherwise, we set x to the right child of the
        current node.

        Once we reach the NIL node, we set the parent

        :param value: The value to be inserted into the tree
        :type value: T
        :return: The node that is being returned is the node that is being inserted.
        """
        node = Node(value)
        node.parent = None
        node.left_child = self.__NIL
        node.right_child = self.__NIL
        node.color = Color.RED

        y = None
        x = self.__root

        while x != self.__NIL:
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

    def remove(self, value: T) -> None:
        """
        If the value is in the tree, remove it

        :param value: The value to remove from the tree
        :type value: T
        """
        self.__remove_from_tree(self.__root, value)

    def minimum(self, node: Node) -> Node:
        """
        It returns the minimum value in the tree.

        :param node: The node to start the search from
        :type node: Node
        :return: The minimum value in the tree.
        """
        while node.left_child != self.__NIL:
            node = node.left_child
        return node

    def maximum(self, node: Node) -> Node:
        """
        It returns the maximum node in the tree.

        :param node: The node to start the search from
        :type node: Node
        :return: The maximum value in the tree.
        """
        while node.right_node != self.__NIL:
            node = node.right_node
        return node

    def __remove_from_tree(self, node: Node, key: T) -> None:
        """
        We find the node to be removed, then we find its successor, and then we replace the node to be removed with its
        successor

        :param node: The node to start searching from
        :type node: Node
        :param key: The key to be removed from the tree
        :type key: T
        :return: The node with the minimum key in the tree.
        """
        z = self.__NIL
        while node is not self.__NIL:
            if node.key is key:
                z = node

            if node.key <= key:
                node = node.right_child
            else:
                node = node.left_child

        if z is self.__NIL:
            # Value is not in the tree
            return

        y = z
        y_color = y.color
        if z.left_child is self.__NIL:
            x = z.right_child
            self.__rb_transplant(z, z.right_child)
        elif z.right_child is self.__NIL:
            x = z.left_child
            self.__rb_transplant(z, z.left_child)
        else:
            y = self.minimum(z.right_child)
            y_color = y.color
            x = y.right_child
            if y.parent is z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right_child)
                y.right_child = z.right_child
                y.right_child.parent = y

            self.__rb_transplant(z, y)
            y.left_child = z.left_child
            y.left_child.parent = y
            y.color = z.color
        if y_color is Color.BLACK:
            self.__remove_balance(x)

    def __remove_balance(self, x: Node) -> None:
        """
        If the node to be removed is black, then we need to rebalance the tree

        :param x: The node to be removed
        :type x: Node
        """
        while x is not self.__root and x.color is Color.BLACK:
            if x is x.parent.left_child:
                s = x.parent.right_child
                if s.color is Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.__left_rotation(x.parent)
                    s = x.parent.right_child

                if s.left_child.color is Color.BLACK and s.right_child.color is Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.right_child.color is Color.BLACK:
                        s.left_child.color = Color.BLACK
                        s.color = Color.RED
                        self.__right_rotation(s)
                        s = x.parent.right_child

                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.right_child.color = Color.BLACK
                    self.__left_rotation(x.parent)
                    x = self.__root
            else:
                s = x.parent.left_child
                if s.color is Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.__right_rotation(x.parent)
                    s = x.parent.left_child

                if s.right_child.color is Color.BLACK and s.right_child.color is Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.left_child.color is Color.BLACK:
                        s.right_child.color = Color.BLACK
                        s.color = Color.RED
                        self.__left_rotation(s)
                        s = x.parent.left_child
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.left_child.color = Color.BLACK
                    self.__right_rotation(x.parent)
                    x = self.__root
        x.color = Color.BLACK

    def __rb_transplant(self, x: Node, y: Node) -> None:
        """
        If the node to be replaced is the root, then the replacement node becomes the root. Otherwise, the replacement node
        takes the place of the node to be replaced

        :param x: The node to be removed
        :type x: Node
        :param y: the node that will replace x
        :type y: Node
        """
        if x.parent is None:
            self.__root = y
        elif x is x.parent.left_child:
            x.parent.left_child = y
        else:
            x.parent.right_child = y
        y.parent = x.parent

    def print(self):
        """
        The function takes in a node, a string, and a boolean. It then prints the node's value, and then calls itself on the
        left and right children of the node, passing in the string and boolean
        """
        self.__print_tree(self.__root, "", True)

    def __print_tree(self, node: Node, indent, last: bool) -> None:
        """
        If the node is not the NIL node, print the node's key and color, then recursively print the left and right subtrees

        :param node: The node to print
        :type node: Node
        :param indent: This is the indentation string that is used to print the tree
        :param last: A boolean value that indicates whether the current node is the last child of its parent
        :type last: bool
        """
        if node != self.__NIL:
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

    def __insert_balance(self, x: Node) -> None:
        """
        It inserts a node into the tree and then balances the tree

        :param x: Node
        :type x: Node
        """
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
        """
        "Rotate the subtree rooted at `x` to the left."

        The first line of the function is a docstring. This is a special type of comment that is used to document the
        function. It is a good idea to include a docstring for every function you write

        :param x: Node
        :type x: Node
        """
        y = x.right_child
        x.right_child = y.left_child
        if y.left_child is not self.__NIL:
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
        """
        "Rotate the subtree rooted at `x` to the right."

        The function is a bit long, but it's not too hard to understand. The first thing it does is to save the left child
        of `x` in a variable called `y`. Then it sets the left child of `x` to be the right child of `y`. Finally, it sets
        the right child of `y` to be `x`

        :param x: Node
        :type x: Node
        """
        y = x.left_child
        x.left_child = y.right_child
        if y.right_child is not self.__NIL:
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


if __name__ == "__main__":
    bst = RedBlackTree[int]()
    bst.insert(10)
    bst.insert(20)
    bst.insert(25)
    bst.insert(30)
    bst.insert(7)
    bst.insert(5)
    bst.insert(4)
    bst.insert(3)
    bst.insert(1)
    bst.print()
