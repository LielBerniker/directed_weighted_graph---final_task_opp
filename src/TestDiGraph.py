import unittest

from src.DiGraph import DiGraph


def create_graph():
    graph1 = DiGraph()
    for i in range(10):
       graph1.add_node(i)
    return graph1


class MyTestCase(unittest.TestCase):

    def test_add_node(self):
        graph1 = create_graph()
        self.assertEqual(10, graph1.v_size())
        graph1.add_node(0)
        self.assertEqual(10, graph1.v_size())
        for i in range(3):
            graph1.add_node(i+10)
        self.assertEqual(13, graph1.v_size())
        for i in range(13):
            graph1.add_node(i)
        self.assertEqual(13, graph1.v_size())

    def test_add_edge(self):
        graph1 = create_graph()
        self.assertEqual(0, graph1.e_size())
        graph1.add_edge(20, 30, 3434.5)
        self.assertEqual(0, graph1.e_size())
        for i in range(5):
            check = graph1.add_edge(i, i+1, i+10)
            self.assertTrue(check)
        self.assertEqual(5, graph1.e_size())
        for i in range(5):
            check = graph1.add_edge(i, i+1, i+20)
            self.assertFalse(check)
        self.assertEqual(5, graph1.e_size())
        graph1.add_edge(9, 0, 45)
        self.assertEqual(6, graph1.e_size())

    def test_remove_edge(self):
        graph1 = create_graph()
        self.assertEqual(0, graph1.e_size())
        check = graph1.remove_edge(9, 8)
        self.assertFalse(check)
        graph1.add_edge(9, 8, 90)
        check = graph1.remove_edge(9, 8)
        self.assertTrue(check)
        for i in range(8):
            graph1.add_edge(i, i+1, i+30)
        self.assertEqual(8, graph1.e_size())
        graph1.remove_edge(7, 8)
        self.assertEqual(7, graph1.e_size())
        for i in range(8):
            graph1.remove_edge(i, i+1)
        self.assertEqual(0, graph1.e_size())

    def test_remove_node(self):
        graph1 = create_graph()
        self.assertEqual(10, graph1.v_size())
        check = graph1.remove_node(11)
        self.assertFalse(check)
        check = graph1.remove_node(9)
        self.assertTrue(check)
        self.assertEqual(9, graph1.v_size())
        for i in range(9):
            check = graph1.remove_node(i)
            self.assertTrue(check)
        self.assertEqual(0, graph1.v_size())

        graph2 = create_graph()
        for i in range(10):
            graph2.add_edge(0, i, i+3)
        self.assertEqual(9, graph2.e_size())
        graph2.remove_node(0)
        self.assertEqual(0, graph2.e_size())
        graph2.add_node(0)
        for j in range(10):
            graph2.add_edge(0, j, j+3)
            graph2.add_edge(j, 0, j*2)
        self.assertEqual(18, graph2.e_size())
        graph2.remove_node(0)
        self.assertEqual(0, graph2.e_size())

    def test_in_and_out_edges(self):
        graph1 = create_graph()
        for key in range(10):
            self.assertEqual(0, len(graph1.all_out_edges_of_node(key)))
            self.assertEqual(0, len(graph1.all_in_edges_of_node(key)))
        graph1.add_edge(9, 8, 90)
        self.assertEqual(1, len(graph1.all_out_edges_of_node(9)))
        self.assertEqual(1, len(graph1.all_in_edges_of_node(8)))
        graph1.remove_edge(9, 8)

        for i in range(9):
            graph1.add_edge(i, i+1, i+30)
            self.assertTrue(i+1 in graph1.all_out_edges_of_node(i).keys())
        graph1.add_edge(9, 0, 789)
        for key2 in range(10):
            self.assertEqual(1, len(graph1.all_out_edges_of_node(key2)))
            self.assertEqual(1, len(graph1.all_in_edges_of_node(key2)))
        self.assertTrue(8 in graph1.all_in_edges_of_node(9).keys())
        self.assertFalse(9 in graph1.all_in_edges_of_node(8).keys())

    def test_vertices_size(self):
        graph1 = create_graph()
        self.assertEqual(10, graph1.v_size())
        graph1.add_node(6)
        self.assertEqual(10, graph1.v_size())
        for i in range(100):
            graph1.add_node(i)
        self.assertEqual(100, graph1.v_size())
        for i in range(10):
            graph1.remove_node(i)
        self.assertEqual(90, graph1.v_size())

    def test_edges_size(self):
        graph1 = create_graph()
        self.assertEqual(0, graph1.e_size())
        graph1.add_edge(1000, 3000, 1.4)
        self.assertEqual(0, graph1.e_size())
        for i in range(50):
            graph1.add_node(i)
            graph1.add_edge(i, i-1, i*3)
        self.assertEqual(49, graph1.e_size())
        for i in range(50):
            graph1.add_edge(0, i, i*1.4)
        self.assertEqual(98, graph1.e_size())
        graph1.remove_node(0)
        self.assertEqual(48, graph1.e_size())

    def test_MC(self):
        graph1 = create_graph()
        self.assertEqual(10, graph1.get_mc())
        graph1.add_node(3)
        self.assertEqual(10, graph1.get_mc())

        for i in range(20):
            graph1.add_node(i)
        self.assertEqual(20, graph1.get_mc())

        for i in range(10):
            graph1.remove_node(i)
        self.assertEqual(30, graph1.get_mc())
        for i in range(10):
            graph1.add_node(i)
            graph1.add_edge(i, i+10, i+2)
        self.assertEqual(50, graph1.get_mc())

        graph1.remove_edge(0, 10)
        self.assertEqual(51, graph1.get_mc())
        graph1.remove_edge(0, 60)
        self.assertEqual(51, graph1.get_mc())
        graph1.add_node(10)
        self.assertEqual(51, graph1.get_mc())
        graph1.add_edge(0, 10, 3454)
        self.assertEqual(52, graph1.get_mc())
        graph1.add_edge(0, 10, 3454)
        self.assertEqual(52, graph1.get_mc())

    def test_get_all_vertices(self):
        graph1 = create_graph()
        self.assertEqual(10, graph1.v_size())
        all_v = graph1.get_all_v()
        for i in range(10):
            check = i in all_v.keys()
            self.assertTrue(check)
        self.assertFalse(30 in all_v.keys())

    def test_forme(self):
        graph1 = create_graph()
        f = graph1.get_node(40)
        mvmdvdvdvfv = 33535