from Structures.Node import Node
from Structures.Edge import Edge
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

    def addEdge(self, a: Node, b: Node) -> None:
        self.__edges.append(Edge(a,b))

    def edgeToSVG(self, edge: Edge) -> str:
        # find coods of nodes
        first: (int, int) = ()
        second: (int, int) = ()
        for node in self.__nodes:
            if edge.first == node[0] or edge.second == node[0]:
                if first == ():
                    first = (node[1], node[2])
                elif second == ():
                    second = (node[1], node[2])
            if first != () and second != ():
                break

        return '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black"/>' \
            .format(x1=first[0], y1=first[1], x2=second[0], y2=second[1])

    def save(self):
        with open(self.__file, "w", encoding="utf-8") as file:
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
