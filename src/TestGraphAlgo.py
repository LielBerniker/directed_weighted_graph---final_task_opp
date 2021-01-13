import unittest
import json

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import networkx as nx


def create_graph1() -> DiGraph:
    """
    create a graph version 1
    """
    graph = DiGraph()
    graph.add_node(0)
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)
    graph.add_node(4)
    graph.add_node(5)
    graph.add_node(6)
    graph.add_node(7)

    graph.add_edge(0, 1, 0)
    graph.add_edge(1, 4, 1)
    graph.add_edge(1, 5, 7)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 6, 2)
    graph.add_edge(2, 3, 10)
    graph.add_edge(3, 2, 3)
    graph.add_edge(3, 7, 5)
    graph.add_edge(4, 0, 16)
    graph.add_edge(4, 5, 1)
    graph.add_edge(5, 6, 1)
    graph.add_edge(6, 5, 5)
    graph.add_edge(7, 6, 4)
    graph.add_edge(7, 3, 1)

    return graph


def create_graph_2() -> DiGraph:
    """
    create a graph version 2
    """
    graph = DiGraph()
    for i in range(9):
        graph.add_node(i)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 0, 2)
    graph.add_edge(2, 4, 9)
    graph.add_edge(2, 3, 0.5)
    graph.add_edge(3, 1, 5)
    graph.add_edge(3, 8, 1)
    graph.add_edge(4, 5, 3)
    graph.add_edge(5, 2, 1)
    graph.add_edge(6, 7, 7)
    graph.add_edge(7, 6, 5)

    return graph


def load_to_networkx(j_graph: nx.Graph, file_name: str):
    """
    load to network x graph from a json
    """
    try:
        with open(file_name, "r") as file:
            my_dict = json.load(file)
    except IOError as e:
        print(e)

    for nodes in my_dict["Nodes"]:
        if ["pos"] in my_dict["Nodes"]:
            pos = tuple(nodes["pos"].split(","))
            j_graph.add_node(nodes["id"], pos)
        else:
            j_graph.add_node(nodes["id"])

    for edges in my_dict["Edges"]:
        j_graph.add_edge(edges["src"], edges["dest"], weight=edges["w"])


def test_time_for_networkx(graph_name: str, src: int, dest: int):
    """
    print the time that toke to the graph to complete the functions, network x graph
    """
    import time
    start_time = time.time()
    file = '../data/' + graph_name + '.json'
    g = nx.Graph()
    load_to_networkx(g, file)
    start_time = time.time()
    nx.connected_components(g)
    connected_components_run_time = time.time() - start_time
    start_time = time.time()
    nx.shortest_path(g, source=src, target=dest)
    shortest_path_run_time = time.time() - start_time
    all_info = "\nsize of graph: " + str(
        graph_name) + "\nfunctions run time: \nconnected components function run time: " + \
               str(connected_components_run_time) + "\nshortest path function run time: " + str(shortest_path_run_time)
    print(all_info)


def test_time_for_functions(graph_name: str, src: int, dst: int):
    """
    print the time that toke to the graph to complete the functions, DiGraph in GraphAlgo
    """
    import time
    algo = GraphAlgo()
    algo.load_from_json('../data/' + graph_name + '.json')
    start_time = time.time()
    algo.connected_component(src)
    connected_component_run_time = time.time() - start_time
    start_time = time.time()
    algo.connected_components()
    connected_components_run_time = time.time() - start_time
    start_time = time.time()
    algo.shortest_path(src, dst)
    shortest_path_run_time = time.time() - start_time

    # create a string of the information
    all_info = "\nsize of graph: " + str(
        graph_name) + "\nfunctions run time: " + "\nconnected component function run time: " + str(
        connected_component_run_time) + \
               "\nconnected components function run time: " + str(
        connected_components_run_time) + "\nshortest path function run time: " + str(shortest_path_run_time)
    print(all_info)


def is_lists_equals(list1: list, list2: list):
    """
     inner function that checks if the list are equal
    """
    if len(list1) is not len(list2):
        return False
    for i in list1:
        if i not in list2:
            return False
    return True


def is_list_in_lists(list1: list, list2: list):
    """
    inner function that checks if a list of list is equal , use the is_lists_equals
    """
    flag = True
    if len(list1) is not len(list2):
        return False
    for i in list1:
        for j in list2:
            if is_lists_equals(i, j) is not True:
                flag = False
            else:
                flag = True
                break
    return flag


class MyTestCase(unittest.TestCase):

    def test_shortest_path(self):
        """
        test that check the shortest path in a graph, checks if hte list of the node id is in the right order
        and if the distance is right
        """
        graph = create_graph1()
        graph_algo = GraphAlgo(graph)

        path_0to1 = graph_algo.shortest_path(0, 1)
        list_chek_0to1 = [0, 1]
        path_0to4 = graph_algo.shortest_path(0, 4)
        list_chek_0to4 = [0, 1, 4]
        path_0to5 = graph_algo.shortest_path(0, 5)
        list_chek_0to5 = [0, 1, 4, 5]
        path_0to6 = graph_algo.shortest_path(0, 6)
        list_chek_0to6 = [0, 1, 2, 6]
        path_0to2 = graph_algo.shortest_path(0, 2)
        list_chek_0to2 = [0, 1, 2]
        path_0to3 = graph_algo.shortest_path(0, 3)
        list_chek_0to3 = [0, 1, 2, 3]
        path_0to7 = graph_algo.shortest_path(0, 7)
        list_chek_0to7 = [0, 1, 2, 3, 7]

        path_1to7 = graph_algo.shortest_path(1, 7)
        list_chek_1to7 = [1, 2, 3, 7]
        # not posiball path
        path_5to1 = graph_algo.shortest_path(5, 1)
        path_1to1 = graph_algo.shortest_path(1, 1)
        list_chek_1to1 = [1]

        self.assertEqual(path_0to1[0], 0)
        self.assertEqual(path_0to2[0], 1)
        self.assertEqual(path_0to3[0], 11)
        self.assertEqual(path_0to4[0], 1)
        self.assertEqual(path_0to5[0], 2)
        self.assertEqual(path_0to6[0], 3)
        self.assertEqual(path_0to7[0], 16)
        self.assertEqual(16, path_1to7[0])
        self.assertEqual(float('inf'), path_5to1[0])
        self.assertEqual(path_1to1[0], 0)

        self.assertTrue(is_lists_equals(path_0to1[1], list_chek_0to1))
        self.assertTrue(is_lists_equals(path_0to2[1], list_chek_0to2))
        self.assertTrue(is_lists_equals(path_0to3[1], list_chek_0to3))
        self.assertTrue(is_lists_equals(path_0to4[1], list_chek_0to4))
        self.assertTrue(is_lists_equals(path_0to5[1], list_chek_0to5))
        self.assertTrue(is_lists_equals(path_0to6[1], list_chek_0to6))
        self.assertTrue(is_lists_equals(path_0to7[1], list_chek_0to7))
        self.assertTrue(is_lists_equals(path_1to7[1], list_chek_1to7))
        self.assertTrue(is_lists_equals(path_5to1[1], []))
        self.assertTrue(is_lists_equals(path_1to1[1], list_chek_1to1))

        graph2 = create_graph_2()
        algo = GraphAlgo(graph2)

        path_0_1 = algo.shortest_path(0, 1)
        list0_1 = [0, 1]
        path5_0 = algo.shortest_path(5, 0)
        list5_0 = [5, 2, 3, 1, 0]
        self.assertEqual(path_0_1[0], 1)
        self.assertEqual(path5_0[0], 8.5)

        self.assertTrue(is_lists_equals(path_0_1[1], list0_1))
        self.assertTrue(is_lists_equals(path5_0[1], list5_0))
        self.assertFalse(is_lists_equals(path_0_1[1], list5_0))

    def test_initiate_graph(self):
        """
        test the initiate function in graph
        """
        graph = create_graph1()
        graph1 = DiGraph()
        graph_algo = GraphAlgo(graph1)
        graph_algo.initiate_graph(graph)
        self.assertEqual(graph_algo.get_graph(), graph)

    def test_get_graph(self):
        """
        test the return of the graph algo function
        """
        graph = create_graph1()
        graph_algo = GraphAlgo(graph)
        g = graph_algo.get_graph
        self.assertEqual(graph_algo.get_graph(), graph)

    def test_save_and_load(self):
        """
        test save and load functions in the graph algo
        """
        graph = create_graph1()
        graph_algo = GraphAlgo(graph)
        graph_algo.save_to_json('../src/a7')
        graph_algo.load_from_json('../src/a7')
        self.assertEqual(graph, graph_algo.get_graph())

    def test_connected_component(self):
        """
        test the connected component in a graph, check if the connected component of a node is right,
        check various nodes in the graph and check if they belong to the right connected component.
        """
        graph = create_graph1()
        graph_algo = GraphAlgo(graph)
        list0 = graph_algo.connected_component(0)
        list1 = graph_algo.connected_component(1)
        list0_check = [0, 1, 4]
        self.assertTrue(is_lists_equals(list0, list0_check))
        self.assertTrue(is_lists_equals(list1, list0_check))
        list5 = graph_algo.connected_component(5)
        list5_chek = [5, 6]
        self.assertTrue(is_lists_equals(list5, list5_chek))
        list3 = graph_algo.connected_component(3)
        list3_chek = [2, 3, 7]
        self.assertTrue(is_lists_equals(list3, list3_chek))
        self.assertFalse(is_lists_equals(list3, list0_check))

        graph2 = create_graph_2()
        algo = GraphAlgo(graph2)
        comp1 = algo.connected_component(1)
        comp3 = algo.connected_component(3)
        comp7 = algo.connected_component(7)
        comp2 = algo.connected_component(2)
        comp4 = algo.connected_component(4)
        comp8 = algo.connected_component(8)
        comp6 = algo.connected_component(6)
        comp0 = algo.connected_component(0)
        list_comp0 = [0, 1]
        list_comp6 = [6, 7]
        list_comp2 = [2, 4, 5]
        list_comp3 = [3]
        list_comp8 = [8]
        self.assertTrue(is_lists_equals(comp1, list_comp0))
        self.assertTrue(is_lists_equals(comp3, list_comp3))
        self.assertTrue(is_lists_equals(comp7, list_comp6))
        self.assertTrue(is_lists_equals(comp2, list_comp2))
        self.assertTrue(is_lists_equals(comp4, list_comp2))
        self.assertTrue(is_lists_equals(comp8, list_comp8))
        self.assertTrue(is_lists_equals(comp6, list_comp6))
        self.assertTrue(is_lists_equals(comp0, list_comp0))

    def test_connected_components(self):
        """
        test the connected components function in the graph algo
        """
        graph = create_graph1()
        graph_algo = GraphAlgo(graph)
        comp = graph_algo.connected_components()
        list_comp = [[0, 1, 4], [5, 6], [2, 3, 7]]
        self.assertTrue(is_list_in_lists(comp, list_comp))
        graph2 = create_graph_2()
        algo = GraphAlgo(graph2)
        comp2 = algo.connected_components()
        list_comp2 = [[0, 1], [2, 4, 5], [3], [8], [6, 7]]
        self.assertTrue(is_list_in_lists(comp2, list_comp2))

    def test_all_graphs_time(self):
        """
        test for a vireos graph jsons, checks and print their time of completing the algorithms in the graph algo.
        """
        graph1 = "G_10_80_1"
        graph2 = "G_100_800_1"
        graph3 = "G_1000_8000_1"
        graph4 = "G_10000_80000_1"
        graph5 = "G_20000_160000_1"
        graph6 = "G_30000_240000_1"
        test_time_for_functions(graph1, 1, 3)
        test_time_for_functions(graph2, 1, 3)
        test_time_for_functions(graph3, 1, 3)
        test_time_for_functions(graph4, 1, 3)
        test_time_for_functions(graph5, 1, 3)
        test_time_for_functions(graph6, 1, 3)

    def test_networkx_time(self):
        """
        test for a vireos graph jsons, checks and print their time of completing the algorithms in the network x
        """
        graph1 = "G_10_80_0"
        graph2 = "G_100_800_0"
        graph3 = "G_1000_8000_0"
        graph4 = "G_10000_80000_0"
        graph5 = "G_20000_160000_0"
        graph6 = "G_30000_240000_0"
        test_time_for_networkx(graph1, 0, 9)
        test_time_for_networkx(graph2, 0, 9)
        test_time_for_networkx(graph3, 0, 9)
        test_time_for_networkx(graph4, 0, 9)
        test_time_for_networkx(graph5, 0, 9)
        test_time_for_networkx(graph6, 0, 9)
