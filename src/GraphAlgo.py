import json
from typing import List
import queue
import sys
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


class GraphAlgo(GraphAlgoInterface):
    """
    this class represent a algorithms that being executed on a directed weighted graph
    """
    global graph1  # a directed weighted graph

    def __init__(self, graph2: DiGraph = None):
        """
        a constructor to the graph, reset graph
        """
        self.graph1 = graph2

    def initiate_graph(self, graph2: DiGraph):
        """
        function that initiate the graph of the graphalgo
        """
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
        try:
            with open(file_name, "r") as file:
                my_dict = json.load(file)
        except IOError as e:
            print(e)
            return False

        # go over the information in json and extract the information into the graph
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
                # go over the information in graph and extract the information into the json
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
        the function goi from the id1 node and check hus neighbors and their neighbors and so go on.
        insert each node in the way to a priority queue and extract each time the one with the lowest distance
        do on until the priority queue is empty, update eace node of the distance from the id1 node and the previus node.
        if there is a path from id1 to id2 , create a list of the nodes if from id1 to id2 ,
        do this by checking the previous node each time
        return a tuple of the distance and the list of nodes in the path
        """
        list_of_nodes = []
        short_path = float('inf')
        if self.graph1 is None:
            return (list_of_nodes, short_path)
        # checks if the two n odes are in the graph
        if id1 not in self.graph1.get_all_v().keys() or id2 not in self.graph1.get_all_v().keys():
            return (list_of_nodes, short_path)
        pr_queue = queue.PriorityQueue()
        if id1 == id2:
            short_path = 0
            list_of_nodes.insert(0, id1)
            return (short_path, list_of_nodes)
        # reset the nodes tag and parent
        for i in self.graph1.get_all_v().keys():
            self.graph1.get_node(i).setTag(sys.float_info.max)
            self.graph1.get_node(i).setParent(None)
        self.graph1.get_node(id1).setTag(0)
        pr_queue.put((self.graph1.get_node(id1).getTag(), id1))
        # go over the priority queue until is empty
        while not pr_queue.empty():
            node_id = pr_queue.get()[1]
            if len(self.graph1.all_out_edges_of_node(node_id)) > 0:
                # go over the node edges that go out from the node
                for neighbor in self.graph1.all_out_edges_of_node(node_id).keys():
                    distance = self.graph1.get_edge(node_id, neighbor) + self.graph1.get_node(node_id).getTag()
                    # check if the distance of the edge between the nodes and the nodes
                    # tag is lower the distance of the neighbor
                    if distance < self.graph1.get_node(neighbor).getTag():
                        self.graph1.get_node(neighbor).setTag(distance)
                        self.graph1.get_node(neighbor).setParent(node_id)
                        pr_queue.put((self.graph1.get_node(neighbor).getTag(), neighbor))
        # checks if there is a path from id1 to id2
        if self.graph1.get_node(id2).getTag() is sys.float_info.max:
            return (short_path, list_of_nodes)
        short_path = self.graph1.get_node(id2).getTag()
        current_node = self.graph1.get_node(id2).getParent()
        list_of_nodes.append(id2)
        # crate the list of nodes in the path
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
         the function call an inner function that go over the graph from the id1 node
         then get all of the nodes that can be reached from id1.
         then the function create a reverse graph and call the inner function again with the reverse graph
         then take only n odes that are in both of the lists an return a list with this nodes
        """
        connected_nodes = []
        if self.graph1 is None:
            return connected_nodes
        if id1 not in self.graph1.graph_nodes.keys():
            return connected_nodes
        # dict of all the nodes that can be reached from id1
        regular_nodes = self.find_connected_component(id1)
        temp_out_edge = self.graph1.get_all_edges_out()
        temp_in_edge = self.graph1.get_all_edges_in()
        # reverse the graph
        self.graph1.set_all_edges_out(temp_in_edge)
        self.graph1.set_all_edges_in(temp_out_edge)
        # dict of all the nodes that can be reached from id1 in the revers graph
        reverse_nodes = self.find_connected_component(id1)
        self.graph1.set_all_edges_out(temp_out_edge)
        self.graph1.set_all_edges_in(temp_in_edge)
        # create a list take only nodes that are in both of the dicts
        for i in regular_nodes.keys():
            if reverse_nodes.get(i) is not None:
                connected_nodes.append(self.graph1.get_node(i).getKey())
                self.graph1.get_node(i).setParent(id1)
        return connected_nodes

    def find_connected_component(self, src: int) -> dict:
        """
        find all the nodes that can be reached from src node
        @param src: The node id
        @return: The list of nodes that can be reached from src node
        Notes:
        go over the graph from the id1 node than go over its neighbors and so on
        return a dict of all the nodes that can be reached from src node.
        """
        nodes_in_comp = {}
        nodes_queue = queue.Queue()
        nodes_queue.put(src)
        nodes_in_comp[src] = 1
        # go until the queue is empty
        while not nodes_queue.empty():
            node_id = nodes_queue.get()
            # go over the node neighbors
            for neighbor in self.graph1.all_out_edges_of_node(node_id).keys():
                if nodes_in_comp.get(neighbor) is None:
                    nodes_queue.put(neighbor)
                    nodes_in_comp[neighbor] = 1
        return nodes_in_comp

    def reset_nodes_comp(self):
        """
          reset the parent to none, to all of the nodes in the graph
        """
        for node_id in self.graph1.graph_nodes.keys():
            self.graph1.get_node(node_id).setParent(None)

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        Notes:
        If the graph is None the function should return an empty list []
        first call an inner function to  reset the parent to none, to all of the nodes in the graph
        then go over each node in graph and check if is none , if it is,
        call the connected_component function to get the the Strongly Connected Component for the node
        the return a list that contain all of the the Strongly Connected Components in the graph
        """
        all_components = []
        if self.graph1 is None:
            return all_components
        self.reset_nodes_comp()
        #  go over the nodes in the graph
        for node_id in self.graph1.graph_nodes.keys():
            if self.graph1.get_node(node_id).getParent() is None:
                node_component = self.connected_component(node_id)
                all_components.append(node_component)
        return all_components

    def find_position(self, side: int, size: int) -> tuple:
        """
        return a position that fits in the square in the plot, by the size of the nodes in the graph
        and by the counter of nodes that been printed to the plot
        @param side: the counter of nodes that been printed
        @param size: The number of nodes in the graph
        @return: tuple of the x and y values
        """
        if side % 4 == 0:
            x_val = side
            y_val = size
        elif side % 4 == 1:
            x_val = size
            y_val = side
        elif side % 4 == 2:
            x_val = side
            y_val = 0
        else:
            x_val = 0
            y_val = side

        return (x_val, y_val)

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        the function go over the graph nodes and plot the node by his position, if the node dont have a position
        than by the function find_position the node get a position that match a square.
        then the function lso plot the node id.
        the function plot the edge by an arrow from the source node to the destination node.
        """
        if self.graph1 is None:
            return None
        all_nodes = {}
        side = 0
        fig, ax = plt.subplots()
        size_of_nodes = self.graph1.v_size()
        # go over the node in the graph , if they haven't been plot , plot them
        for node_id in self.graph1.graph_nodes.keys():
            if all_nodes.get(node_id) is None:
                n_pos = self.graph1.get_node(node_id).getPosition()
                if n_pos is None:
                    p1 = self.find_position(side, size_of_nodes)
                    side = side + 1
                else:
                    p1 = (float(n_pos[0]), float(n_pos[1]))
                all_nodes[node_id] = p1
                plt.plot(p1[0], p1[1], 'o', color='b')
                ax.annotate(node_id, p1,
                            color='black',
                            fontsize=12)
            # go over the node neighbors , if they haven't been plot , plot them
            for neighbor in self.graph1.all_out_edges_of_node(node_id).keys():
                if all_nodes.get(neighbor) is None:
                    neighbor_pos = self.graph1.get_node(neighbor).getPosition()
                    if neighbor_pos is None:
                        p2 = self.find_position(side, size_of_nodes)
                        side = side + 1
                    else:
                        p2 = (float(neighbor_pos[0]), float(neighbor_pos[1]))
                    all_nodes[neighbor] = p2
                    plt.plot(p2[0], p2[1], 'o', color='b')
                    ax.annotate(neighbor, p2,
                                color='black',
                                fontsize=12)

                n_pos = all_nodes[node_id]
                neighbor_pos = all_nodes[neighbor]
                # plot the edge
                con = ConnectionPatch(n_pos, neighbor_pos, "data", "data", arrowstyle="-|>", mutation_scale=15, fc="r")
                ax.add_artist(con)
        plt.show()
        print(all_nodes)
