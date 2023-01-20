from unittest import TestCase
from SVGWriter import SVGWriter
from Structures.Node import Node


class TestSVGWriter(TestCase):
    def test_save(self):
        writer = SVGWriter(200, 200, "test.svg", "svgWriterConfig.cfg")
        writer.addNode(Node[int](1), 80, 80)
        writer.addNode(Node[str]("ABC"), 150, 80)
        writer.save()
