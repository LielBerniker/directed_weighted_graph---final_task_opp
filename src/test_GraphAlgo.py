import math
from unittest import TestCase

from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import networkx as nx


class TestGraphAlgo(TestCase):
    def setUp(self) -> None:
        global Galgo
        global NG
        global graph
        Galgo = GraphAlgo()
        Galgo.load_from_json('../data/A5')
        graph = DiGraph()
        for i in range(6):
            graph.add_node(i)
        graph.add_edge(0, 3, 1)
        graph.add_edge(3, 1, 0)
        graph.add_edge(2, 0, 1)
        graph.add_edge(2, 5, 5)
        graph.add_edge(2, 4, 1.5)
        graph.add_edge(4, 5, 3)
        graph.add_edge(5, 4, 2.5)
        graph.add_edge(3, 2, 2)

    def test_load_save_from_json(self):
        Gr = GraphAlgo(graph)
        self.assertTrue(Gr.save_to_json("savie"),"should return true if saved properly")
        Gr1 = GraphAlgo()
        self.assertTrue(Gr1.load_from_json("savie"),"should return true if loaded properly")
        self.assertEqual(Gr.G,Gr1.G)
        Gr1.G.remove_node(1)
        self.assertNotEqual(Gr1.G,Gr.G,"after removing node1 should be equal")
        Gr1.G.add_node(1)
        self.assertNotEqual(Gr.G,Gr1.G,"still should be euals missing edge 3->1")
        Gr2 = GraphAlgo()
        self.assertTrue(Gr2.load_from_json("../data/A3"))
        self.assertEqual(49,Gr2.G.v_size(),"should have 49 nodes")
        self.assertEqual(136,Gr2.G.edgeSize,"should have 136 edges")



    def test_shortest_path(self):
        (dis, test_list) = Galgo.shortest_path(0, 5)
        self.assertEqual(1, 1)
        self.assertEqual(0, test_list[0].id, "key of this node should be 0")
        self.assertEqual(2, test_list[1].id, "key of this node should be 2")
        self.assertEqual(3, test_list[2].id, "key of this node should be 3")
        self.assertEqual(13, test_list[3].id, "key of this node should be 13")
        self.assertEqual(5, test_list[4].id, "key of this node should be 5")
        self.assertEqual(5, test_list.__len__(), "there should be 5 nodes in that path")
        self.assertEqual(4.685698594072881, dis, "shortest path distance should be 4.685698594072881")
        Galgo.G.remove_node(13)
        (dis1, test_list1) = Galgo.shortest_path(0, 5)
        self.assertNotEqual(dis, dis1, "after removing node 13 should be different distance")
        Gr = GraphAlgo(graph)
        (dis2, testi) = Gr.shortest_path(1, 0)
        self.assertEqual(math.inf, dis2, "there isnt a path between 1 to 0 so should be inf")
        with self.assertRaises(ValueError):
            Gr.shortest_path(13, 14)
        (dis3, test_list2) = Gr.shortest_path(2, 5)
        self.assertEqual(4.5, dis3, "shortest dis should be 4.5")
        self.assertEqual(2, test_list2[0].id, "key of this node should be 2")
        self.assertEqual(4, test_list2[1].id, "key of this node should be 4")
        self.assertEqual(5, test_list2[2].id, "key of this node should be 5")

    def test_connected_component_s(self):
        test_list = Galgo.connected_components()
        self.assertEqual(1, test_list.__len__(), "the graph is connected so it will contain 1 list with all nodes")
        for i in range(48):
            self.assertTrue(test_list[0].__contains__(i))
        test_list1 = Galgo.connected_component(0)
        self.assertEqual(test_list1, test_list[0], "same lists because is connected")
        with self.assertRaises(ValueError):
            Galgo.connected_component(100)
        Gr = GraphAlgo(graph)
        test_list2 = Gr.connected_components()
        self.assertEqual(3, test_list2.__len__(), "should be three lists in that list")
        test_list3 = Gr.connected_component(2)
        test_list4 = Gr.connected_component(0)
        self.assertEqual(test_list3, test_list4, "same list because they are strongly connected")
        self.assertTrue(test_list3.__contains__(2),"should contain this key because they SCC")
        self.assertTrue(test_list3.__contains__(0),"should contain this key because they SCC")
        self.assertTrue(test_list3.__contains__(3),"should contain this key because they SCC")


