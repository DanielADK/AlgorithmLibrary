from unittest import TestCase
from SVGWriter import SVGWriter
from Structures.Node import Node


class TestSVGWriter(TestCase):
    def test_addNodeAndEdge(self):
        writer = SVGWriter(200, 200, "svgWriterConfig.cfg")
        a = Node[int](1)
        b = Node[str]("ABC")
        writer.addNode(a, 80, 80)
        writer.addNode(b, 150, 120)
        writer.addEdge(a, b)
        writer.save("test.svg")

    def test_JSONLoad(self):
        writer = SVGWriter(200, 200, "svgWriterConfig.cfg")
        writer.loadFromJSON("import.json")
        writer.save("test.svg")

