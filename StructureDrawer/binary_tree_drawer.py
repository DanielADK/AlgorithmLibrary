import random
from AlgorithmLibrary.binary_search_tree import BinarySearchTree, Node, T
import matplotlib.pyplot as plt
from Utilities.Config import Config
from PIL import Image, ImageDraw, ImageFont


class ChartNode(Node):
    def __init__(self, value: T, x: int, y: int):
        super().__init__(value)
        self.x: int = x
        self.y: int = y


def getTreeDepth(node: Node, depth: int) -> int:
    ldepth: int = 0
    rdepth: int = 0
    if node.left_child is not None:
        ldepth = getTreeDepth(node.left_child, depth+1)
    if node.right_child is not None:
        rdepth = getTreeDepth(node.right_child, depth+1)
    if ldepth+rdepth != 0:
        depth = ldepth if ldepth > rdepth else rdepth
    return depth


class Drawing:
    class Layer:
        def __init__(self, x_size: int, y_size: int, color: tuple[int, int, int, int]):
            self.image: Image = Image.new("RGBA", (x_size, y_size), color)
            self.draw: ImageDraw = ImageDraw.Draw(self.image)

    def __init__(self, x_size: int, y_size: int, config: str):
        self.__cfg_file: str = config
        self.__cfg: Config = Config(config)
        self.__x_size = x_size
        self.__y_size = y_size
        self.__background: Drawing.Layer = self.Layer(x_size, y_size, (255, 255, 255, 255))
        self.__layout: Drawing.Layer = self.Layer(x_size, y_size, (255, 255, 255, 0))
        self.__layout: Drawing.Layer = self.Layer(x_size, y_size, (255, 255, 255, 0))

    def drawGrid(self, step: int) -> None:
        for x_pos in range(0, self.__x_size, step):
            self.__background.draw.line([(x_pos, 0), (x_pos, self.__y_size)],
                                        fill=(169, 169, 169),
                                        width=1)
        for y_pos in range(0, self.__y_size, step):
            self.__background.draw.line([(0, y_pos), (self.__x_size, y_pos)],
                                        fill=(169, 169, 169),
                                        width=1)

    def drawNodeAt(self, node: Node, x: int, y: int) -> None:
        node_radius = self.__cfg.get("node_radius")
        node_line_width = self.__cfg.get("node_line_width")
        x_min, y_min = x-(node_radius / 2), y-(node_radius / 2)
        text_height: int = node_radius
        font: ImageFont = ImageFont.truetype("Roboto-Medium.ttf", text_height)
        text_width: float = self.__layout.draw.textlength(str(node.key), font)
        text_ratio: float = (node_radius * (1 / 2)) / text_width

        font = ImageFont.truetype("Roboto-Medium.ttf", int(text_height * text_ratio))

        self.__layout.draw.ellipse((x_min, y_min, x_min+node_radius, y_min+node_radius),
                                   outline=(0, 0, 0),
                                   fill=(255, 255, 255),
                                   width=node_line_width)
        self.__layout.draw.text((x, y), str(node.key),
                                align="center",
                                anchor="mm",
                                fill=(0, 0, 0),
                                font=font)

    def drawNode(self, node: ChartNode) -> None:
        self.drawNodeAt(node, node.x, node.y)

    def drawNodeConnection(self, a: ChartNode, b: ChartNode):
        self.__layout.draw.line([(a.x, a.y), (b.x, b.y)],
                                fill=(0, 0, 0),
                                width=self.__cfg.get("line_width"))

    def drawNodeTree(self, node: Node, x_pos: int, y_depth: int) -> None:
        y_step: int = self.__cfg.get("node_radius")
        new_depth: int = int(y_depth+y_step * 1.5)
        height: int = int(new_depth / y_step)
        x_step: int = int(self.__x_size / (2 ** height))
        x_left: int = int(x_pos-x_step)
        x_right: int = int(x_pos+x_step)
        if node.left_child is not None:
            self.drawNodeConnection(
                    ChartNode(node.key, x_pos, y_depth),
                    ChartNode(node.left_child, x_left, new_depth))
            self.drawNodeTree(node.left_child, x_left, new_depth)
        if node.right_child is not None:
            self.drawNodeConnection(
                    ChartNode(node.key, x_pos, y_depth),
                    ChartNode(node.right_child, x_right, new_depth))
            self.drawNodeTree(node.right_child, x_right, new_depth)
        self.drawNodeAt(node, x_pos, y_depth)

    def drawTree(self, tree: BinarySearchTree) -> None:
        self.drawGrid(25)

        height: int = getTreeDepth(tree.root, 0)
        max_size: int = 2 ** (height+1)
        x_size: int = self.__cfg.get("node_radius") * (max_size-8)
        y_size: int = self.__cfg.get("node_radius") * int(height*2)
        self.__init__(x_size, y_size, self.__cfg_file)

        canvas_center: int = int(x_size / 2)

        y_depth = self.__cfg.get("node_radius")
        self.drawNodeTree(tree.root, canvas_center, y_depth)
        print()

    def show(self):
        self.__layout.image.show()

    def print_to_plot(self):
        plt.imshow(self.__image)
        plt.show()


drawing = Drawing(500, 300, "params.cfg")

bst = BinarySearchTree[int]()

size = 1024
for i in range(1, 5):

    print(2**(i+1))

count = 10
#for i in [-3, -5, 6, -9, 5, 8, 2, 7, 9, -1]:
for i in [60, 50, 70, 40, 55, 65, 80, 30, 45, 53, 58, 63, 68, 75, 90, 20, 35, 42, 255]:
    bst.insert(i)

drawing.drawTree(bst)
drawing.show()
