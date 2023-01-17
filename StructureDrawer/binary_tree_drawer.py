import AlgorithmLibrary.binary_search_tree
from AlgorithmLibrary.binary_search_tree import BinarySearchTree, Node, T
import math
from Utilities.Config import Config
from PIL import Image, ImageDraw, ImageFont


class ChartNode(Node):
    def __init__(self, value: T, x: int, y: int):
        super().__init__(value)
        self.x: int = x
        self.y: int = y


class Drawing:
    def __init__(self, x_size: int, y_size: int, config: str):
        self.__cfg: Config = Config(config)
        self.__image: Image = Image.new("RGB", (x_size, y_size), (255, 255, 255))
        self.__im_draw: ImageDraw = ImageDraw.Draw(self.__image)

    def drawGrid(self, step: int) -> None:
        x_size, y_size = self.__im_draw.im.size
        for x_pos in range(0, x_size, step):
            self.__im_draw.line([(x_pos, 0), (x_pos, y_size)], fill=(169, 169, 169), width=1)
        for y_pos in range(0, y_size, step):
            self.__im_draw.line([(0, y_pos), (x_size, y_pos)], fill=(169, 169, 169), width=1)

    def drawNodeAt(self, node: Node, x: int, y: int) -> None:
        node_radius = self.__cfg.get("node_radius")
        node_line_width = self.__cfg.get("node_line_width")
        x_min, y_min = x-node_radius / 2, y-node_radius / 2
        # fontsize = 2/3 * node_radius
        font: ImageFont = ImageFont.truetype("Roboto-Medium.ttf", int(2 / 3 * node_radius))

        self.__im_draw.ellipse((x_min, y_min, x_min+node_radius, y_min+node_radius),
                               outline=(0, 0, 0),
                               fill=(255, 255, 255),
                               width=node_line_width)
        self.__im_draw.text((x, y), str(node.key),
                            align="center",
                            anchor="mm",
                            fill=(0, 0, 0),
                            font=font)

    def drawNode(self, node: ChartNode) -> None:
        self.drawNodeAt(node, node.x, node.y)

    def connectNode(self, a: ChartNode, b: ChartNode):
        self.__im_draw.line([(a.x, a.y), (b.x, b.y)],
                            fill=(0, 0, 0),
                            width=self.__cfg.get("line_width"))

    def draw(self, tree: BinarySearchTree) -> None:
        self.drawGrid(40)
        self.drawNodeAt(Node(1), 40, 40)

        a = ChartNode(2, 180, 180)
        b = ChartNode(3, 140, 140)
        self.connectNode(a, b)
        self.drawNode(a)
        self.drawNode(b)

        # write to stdout
        self.__image.show()


drawing = Drawing(500, 300, "params.cfg")

bst = BinarySearchTree[int]()

bst.insert(5)
bst.insert(3)
bst.insert(8)
bst.insert(9)
bst.insert(1)
bst.insert(4)
bst.insert(2)

drawing.draw(bst)