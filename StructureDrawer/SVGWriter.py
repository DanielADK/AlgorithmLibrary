from Structures.Node import Node
from Structures.Edge import Edge
from Utilities.Config import Config
import json


def nodeToSVG(node: (Node, (int, int))) -> str:
    return '<g class="point" transform="translate({x},{y})">' \
           '<circle></circle>' \
           '<text class="pointIndex" text-anchor="middle" y="5">' \
           '{key}' \
           '</text>' \
           '</g>' \
        .format(key=str(node[0].key), x=node[1][0], y=node[1][1])


class SVGWriter:
    def __init__(self, x_size: int, y_size: int, config: str):
        self.__cfg_file: str = config
        self.__cfg: Config = Config(config)
        self.__x_size: int = x_size
        self.__y_size: int = y_size
        self.__nodes: list[(Node, (int, int))] = list()
        self.__edges: list[Edge] = list()

    def addNode(self, node: Node, x: int, y: int) -> None:
        self.__nodes.append((node, (x, y)))

    def addEdge(self, a: Node, b: Node) -> None:
        self.__edges.append(Edge(a, b))

    def edgeToSVG(self, edge: Edge) -> str:
        # find coords of nodes
        first: (int, int) = [x for x in self.__nodes if x[0] == edge.first][0][1]
        second: (int, int) = [x for x in self.__nodes if x[0] == edge.second][0][1]
        return '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black"/>' \
            .format(x1=first[0], y1=first[1], x2=second[0], y2=second[1])

    def save(self, file_name: str):
        with open(file_name, "w", encoding="utf-8") as file:
            # Write header SVG tag
            file.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" '
                       'width="{x}" height="{y}">\n'.format(x=self.__x_size, y=self.__y_size))

            # Write styles
            file.write(self.__cfg.get("styles")+"\n")

            # Write edges
            for edge in self.__edges:
                file.write(self.edgeToSVG(edge))
                print(self.edgeToSVG(edge))

            # Write nodes
            for node in self.__nodes:
                file.write(nodeToSVG(node))
                print(nodeToSVG(node))

            # Write footer SVG tag
            file.write("</svg>")

    def loadFromJSON(self, file_name: str):
        with open(file_name, "r", encoding="utf-8") as f:
            load = json.loads(f.read())
        for node in load["nodes"]:
            self.__nodes.append((Node(node["key"]), (node["x"], node["y"])))
        for edge in load["edges"]:
            self.__edges.append(Edge(
                [x for x in self.__nodes if edge["first"] == x[0].key][0][0],
                [x for x in self.__nodes if edge["second"] == x[0].key][0][0]
            ))
