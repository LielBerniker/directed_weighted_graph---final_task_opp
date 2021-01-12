from unittest import TestCase
from GraphAlgo import GraphAlgo
from network import Network
from DiGraph import DiGraph
import networkx as nx


class TestDiGraph(TestCase):

    def setUp(self) -> None:
        global Galgo
        global NG
        Galgo = GraphAlgo()
        NG = Network('../data/A5')
        Galgo.load_from_json('../data/A5')

    def test_v_size(self):
        self.assertEqual(Galgo.G.v_size(), nx.number_of_nodes(NG.G), "Both graph made by A5 so they should be the same")
        Galgo.G.remove_node(0)
        Galgo.G.remove_node(1)
        Galgo.G.remove_node(2)
        self.assertNotEqual(Galgo.G.v_size(), nx.number_of_nodes(NG.G),
                            "Galgo should have less Nodes in it after removing 3 nodes")
        Galgo.G.add_node(100)
        Galgo.G.add_node(80)
        Galgo.G.add_node(95)
        self.assertEqual(Galgo.G.v_size(), nx.number_of_nodes(NG.G),
                         "after adding 3 nodes size should be the same again")

    def test_e_size(self):
        self.assertEqual(Galgo.G.e_size(), nx.number_of_edges(NG.G), "Both graphs should have number of edges like A5")
        Galgo.G.remove_edge(0, 1)
        Galgo.G.remove_edge(0, 8)
        Galgo.G.remove_edge(1, 0)
        self.assertNotEqual(Galgo.G.e_size(), nx.number_of_edges(NG.G),
                            "removing 3 edges, edges number shouldnt be even")
        Galgo.G.add_edge(0, 1, 1)
        Galgo.G.add_edge(0, 8, 1)
        Galgo.G.add_edge(1, 0, 1)
        self.assertEqual(Galgo.G.e_size(), nx.number_of_edges(NG.G),
                         "after adding the 3 edges should be the same again")

    def test_get_all_v(self):
        tmp_list = [i for i in Galgo.G.get_all_v().keys()]
        j = 0
        for i in nx.nodes(NG.G):
            self.assertEqual(tmp_list[j], i, "should have same keys")
            j = j + 1
        Galgo.G.remove_node(0)
        tmp_list1 = [i for i in Galgo.G.get_all_v().keys()]
        self.assertNotEqual(tmp_list1[0], nx.nodes(NG.G)[0], "should have this key")

    def test_all_in_edges_of_node(self):
        tmp_list = [i for i in Galgo.G.all_in_edges_of_node(1).keys()]
        self.assertEqual(0, tmp_list[0])
        self.assertEqual(2, tmp_list[1])
        self.assertEqual(8, tmp_list[2])
        self.assertEqual(9, tmp_list[3])
        self.assertEqual(10, tmp_list[4])

    def test_all_out_edges_of_node(self):
        tmp_list = [i for i in Galgo.G.all_out_edges_of_node(0).keys()]
        self.assertEqual(1, tmp_list[0])
        self.assertEqual(2, tmp_list[1])
        self.assertEqual(8, tmp_list[2])
        self.assertEqual(9, tmp_list[3])

    def test_add_edge(self):
        self.assertFalse(Galgo.G.add_edge(0, 1, Galgo.G.oute[0][1]), "this edge already exist->should be False")
        self.assertTrue(Galgo.G.add_edge(0, 1, 3), "different weight should change the edge ")
        self.assertFalse(Galgo.G.add_edge(0, 1, -1), "shouldnt add edge with negative weight")
        self.assertTrue(Galgo.G.add_edge(7, 1, 1), "should add a new edge to the graph")
        self.assertEqual(3, Galgo.G.oute[0][1], "edge should weight 3 after we changed it")
        self.assertEqual(1, Galgo.G.oute[7][1], "edge should weight 1 after adding it")

    def test_add_node(self):
        self.assertFalse(Galgo.G.add_node(0), "this node already exists in the graph")
        Galgo.G.remove_node(0)
        self.assertTrue(Galgo.G.add_node(0), "should add it after we removed it")
        self.assertEqual(48, Galgo.G.v_size(), "the graph should have 48 nodes")
        self.assertTrue(Galgo.G.add_node(50), "adding a new node to the graph")
        self.assertEqual(49, Galgo.G.v_size(), "the graph should have 40 nodes after adding one")

    def test_remove_node(self):
        self.assertEqual(48, Galgo.G.v_size(), "the graph should have 48 nodes")
        self.assertTrue(Galgo.G.remove_node(0), "should remove node with key 0")
        self.assertEqual(47, Galgo.G.v_size(), "after removing node should be 47 nodes")
        self.assertFalse(Galgo.G.remove_node(50), "cant remove a node that isnt exists")

    def test_remove_edge(self):
        self.assertEqual(166, Galgo.G.e_size(), "this graph should have 166 edges")
        self.assertTrue(Galgo.G.remove_edge(0, 1), "should remove edge s:0 d:1")
        self.assertFalse(Galgo.G.remove_edge(0, 1), "this edge already been removed")
        self.assertEqual(165, Galgo.G.e_size(), "after removing an edge should be 165 edges")
        self.assertFalse(Galgo.G.remove_edge(100, 234), "there arent such nodes at the graph")
