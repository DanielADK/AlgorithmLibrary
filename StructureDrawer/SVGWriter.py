from Structures import Node, Edge
from Utilities.Config import Config


def nodeToSVG(node: (Node, (int, int))) -> str:
    return '<g class="point" transform="translate({x},{y})">' \
            '<circle></circle>' \
            '<text class="pointIndex" text-anchor="middle" y="5">' \
            '{key}' \
            '</text>' \
            '</g>' \
            .format(key=str(node[0].key), x=node[1], y=node[2])


class SVGWriter:
    def __init__(self, x_size: int, y_size: int, file_path: str, config: str):
        self.__cfg_file: str = config
        self.__cfg: Config = Config(config)
        self.__file: str = file_path
        self.__x_size: int = x_size
        self.__y_size: int = y_size
        self.__nodes: list[(Node, (int, int))] = list()
        self.__edges: list[Edge] = list()

    def addNode(self, node: Node, x: int, y: int) -> None:
        self.__nodes.append((node, x, y))

    def save(self):
        with open(self.__file, "w", encoding="utf-8") as file:
            # Write header SVG tag
            file.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" '
                       'width="{x}" height="{y}">\n'.format(x=self.__x_size, y=self.__y_size))

            # Write styles
            file.write(self.__cfg.get("styles")+"\n")

            # Write lines

            # Write edges
            for node in self.__nodes:
                file.write(nodeToSVG(node))
                print(nodeToSVG(node))

            # Write footer SVG tag
            file.write("</svg>")
