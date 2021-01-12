import json
from typing import List
import queue
import sys
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import random


class GraphAlgo(GraphAlgoInterface):
    global graph1

    def __init__(self, graph2: DiGraph = None):
        self.graph1 = graph2

    def initiate_graph(self, graph2: DiGraph):
        self.graph1 = graph2

    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph1

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """

        try:
            with open(file_name, "r") as file:
                my_dict = json.load(file)
        except IOError as e:
            print(e)
            return False

        j_graph = DiGraph()
        for nodes in my_dict["Nodes"]:
            if "pos" in nodes:
                if ["pos"] is None:
                    j_graph.add_node(nodes["id"])
                else:
                    pos = tuple(nodes["pos"].split(","))
                    j_graph.add_node(nodes["id"], pos)
            else:
                j_graph.add_node(nodes["id"])

        for edges in my_dict["Edges"]:
            j_graph.add_edge(edges["src"], edges["dest"], edges["w"])
        self.graph1 = j_graph
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:

            with open(file_name, "w") as file:
                g = self.graph1

                j_dict = {"Nodes": [], "Edges": []}
                all_nodes = g.get_all_v()

                for node in all_nodes:
                    pos_tup = all_nodes[node].getPosition()
                    if pos_tup is None:
                        j_dict["Nodes"].append({"id": node})
                    else:
                        str_pos = ','.join(map(str, pos_tup))
                        j_dict["Nodes"].append({"id": node, "pos": str_pos})
                    edges_out = g.all_out_edges_of_node(node)
                    for node_Ni in edges_out:
                        j_dict["Edges"].append({"src": node, "dest": node_Ni, "w": edges_out[node_Ni]})
                a = dict(j_dict)
                json.dump(a, file, indent=5)
            return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Example:
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        """
        list_of_nodes = []
        short_path = float('inf')
        if id1 not in self.graph1.get_all_v().keys() or id2 not in self.graph1.get_all_v().keys():
            return (list_of_nodes, short_path)
        pr_queue = queue.PriorityQueue()
        if id1 == id2:
            short_path = 0
            list_of_nodes.insert(0, id1)
            return (short_path, list_of_nodes)
        for i in self.graph1.get_all_v().keys():
            self.graph1.get_node(i).setTag(sys.float_info.max)
            self.graph1.get_node(i).setParent(None)
        self.graph1.get_node(id1).setTag(0)
        pr_queue.put((self.graph1.get_node(id1).getTag(), id1))
        while not pr_queue.empty():
            node_id = pr_queue.get()[1]
            if len(self.graph1.all_out_edges_of_node(node_id)) > 0:
                for neighbor in self.graph1.all_out_edges_of_node(node_id).keys():
                    distance = self.graph1.get_edge(node_id, neighbor) + self.graph1.get_node(node_id).getTag()
                    if distance < self.graph1.get_node(neighbor).getTag():
                        self.graph1.get_node(neighbor).setTag(distance)
                        self.graph1.get_node(neighbor).setParent(node_id)
                        pr_queue.put((self.graph1.get_node(neighbor).getTag(), neighbor))
        if self.graph1.get_node(id2).getTag() is sys.float_info.max:
            return (short_path, list_of_nodes)
        short_path = self.graph1.get_node(id2).getTag()
        current_node = self.graph1.get_node(id2).getParent()
        list_of_nodes.append(id2)
        while current_node is not None:
            node_in = current_node
            list_of_nodes.insert(0, node_in)
            current_node = self.graph1.get_node(node_in).getParent()
        return (short_path, list_of_nodes)

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        connected_nodes = []
        if self.graph1 is None:
            return connected_nodes
        if id1 not in self.graph1.graph_nodes.keys():
            return connected_nodes
        regular_nodes = self.find_connected_component(id1)
        temp_out_edge = self.graph1.get_all_edges_out()
        temp_in_edge = self.graph1.get_all_edges_in()
        self.graph1.set_all_edges_out(temp_in_edge)
        self.graph1.set_all_edges_in(temp_out_edge)
        reverse_nodes = self.find_connected_component(id1)
        self.graph1.set_all_edges_out(temp_out_edge)
        self.graph1.set_all_edges_in(temp_in_edge)
        for i in regular_nodes.keys():
            if reverse_nodes.get(i) is not None:
                connected_nodes.append(self.graph1.get_node(i).getKey())
                self.graph1.get_node(i).setParent(id1)
        return connected_nodes

    def find_connected_component(self, src: int) -> dict:
        nodes_in_comp = {}
        nodes_queue = queue.Queue()
        nodes_queue.put(src)
        nodes_in_comp[src] = 1
        while not nodes_queue.empty():
            node_id = nodes_queue.get()
            for neighbor in self.graph1.all_out_edges_of_node(node_id).keys():
                if nodes_in_comp.get(neighbor) is None:
                    nodes_queue.put(neighbor)
                    nodes_in_comp[neighbor] = 1
        return nodes_in_comp

    def reset_nodes_comp(self):
        for node_id in self.graph1.graph_nodes.keys():
            self.graph1.get_node(node_id).setParent(None)

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        Notes:
        If the graph is None the function should return an empty list []
        """
        all_components = []
        if self.graph1 is None:
            return all_components
        self.reset_nodes_comp()
        for node_id in self.graph1.graph_nodes.keys():
            if self.graph1.get_node(node_id).getParent() is None:
                node_component = self.connected_component(node_id)
                all_components.append(node_component)
        return all_components

    def find_position(self, src: int, size: int) -> tuple:
        avg_x = 0
        avg_y = 0
        if size > 100:
            rand = (random.uniform(0, size), random.uniform(0, size))
        else:
            rand = (random.uniform(0, 100), random.uniform(0, 100))
        n_size = len(self.graph1.all_out_edges_of_node(src)) + len(self.graph1.all_in_edges_of_node(src))
        if n_size < 3:
            return rand
        for neighbor in self.graph1.all_in_edges_of_node(src).keys():
            n_pos = self.graph1.get_node(neighbor).getPosition()
            if n_pos is not None:
                avg_x = avg_x + n_pos[0]
                avg_y = avg_y + n_pos[1]
            else:
                n_size = n_size - 1
        for neighbor in self.graph1.all_out_edges_of_node(src).keys():
            n_pos = self.graph1.get_node(neighbor).getPosition()
            if n_pos is not None:
                avg_x = avg_x + n_pos[0]
                avg_y = avg_y + n_pos[1]
            else:
                n_size = n_size - 1
        if n_size == 0:
            return rand
        elif avg_y == 0 and avg_x == 0:
            return rand
        else:
            return (avg_x / n_size, avg_y / n_size)

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        all_nodes = {}
        fig, ax = plt.subplots()
        size_of_nodes = self.graph1.v_size()
        for node_id in self.graph1.graph_nodes.keys():
            if all_nodes.get(node_id) is None:
                n_pos = self.graph1.get_node(node_id).getPosition()
                if n_pos is None:
                    p1 = self.find_position(node_id, size_of_nodes)
                else:
                    p1 = n_pos
                all_nodes[node_id] = p1
                plt.plot(p1[0], p1[1], 'o', color='red',
                         markersize=7, linewidth=7,
                         markerfacecolor='blue',
                         markeredgecolor='black',
                         markeredgewidth=1)

            for neighbor in self.graph1.all_out_edges_of_node(node_id).keys():
                if all_nodes.get(neighbor) is None:
                    neighbor_pos = self.graph1.get_node(neighbor).getPosition()
                    if neighbor_pos is None:
                        p2 = self.find_position(neighbor, size_of_nodes)
                    else:
                        p2 = neighbor_pos
                    all_nodes[neighbor] = p2
                    plt.plot(p2[0], p2[1], 'o', color='red',
                             markersize=7, linewidth=7,
                             markerfacecolor='blue',
                             markeredgecolor='black',
                             markeredgewidth=1)
                n_pos = all_nodes[node_id]
                p1 = (n_pos[0], n_pos[1])
                neighbor_pos = all_nodes[neighbor]
                p2 = (neighbor_pos[0], neighbor_pos[1])
                con = ConnectionPatch(p1, p2, "data", "data", arrowstyle="-|>", mutation_scale=20, fc="w")
                ax.add_artist(con)
        plt.show()
