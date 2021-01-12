from src.GraphInterface import GraphInterface
from src.NodeGraph import NodeGraph


class DiGraph(GraphInterface):
    global MC
    global graph_nodes
    global graph_edges
    global edge_counter

    def __init__(self):
        self.MC = 0
        self.graph_nodes = {}
        self.graph_edges_in = {}
        self.graph_edges_out = {}
        self.edge_counter = 0

    def get_node(self, node_id: int) -> NodeGraph:
        """
        Returns a vertex in the graph (NodeGraph)
        :return: return NodeGraph
        if there the graph do not have a node with the key node_id return None
        """
        if node_id not in self.graph_nodes.keys():
            return None
        else:
            return self.graph_nodes[node_id]

    def get_edge(self, src: int, dst: int) -> float:
        """
        Returns the edge size from gogo vertex to dst vertex in this graph
        :return: size of edge
        if the edge not exist return -1
        """
        if src not in self.graph_edges_out.keys():
            return -1
        if dst not in self.graph_edges_out[src].keys():
            return -1
        return self.graph_edges_out[src][dst]

    def get_all_edges_in(self) -> dict:
        return self.graph_edges_in

    def get_all_edges_out(self) -> dict:
        return self.graph_edges_out

    def set_all_edges_in(self, in_edges: dict):
        self.graph_edges_in = in_edges

    def set_all_edges_out(self, out_edges: dict):
        self.graph_edges_out = out_edges

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        :return: The number of vertices in this graph
        """
        return len(self.graph_nodes)

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if id1 not in self.graph_nodes.keys() or id2 not in self.graph_nodes.keys():
            return False
        if weight < 0:
            return False
        if id2 == id1:
            return False
        if id1 in self.graph_edges_out.keys():
            if id2 in self.graph_edges_out[id1].keys():
                if self.graph_edges_out[id1][id2] != weight:
                    self.graph_edges_out[id1][id2] = weight
                    self.graph_edges_in[id2][id1] = weight
                    self.MC = self.MC + 1
                return False
            else:
                self.graph_edges_out[id1][id2] = weight
                if id2 not in self.graph_edges_in.keys():
                    edge_in1 = {id1: weight}
                    self.graph_edges_in[id2] = edge_in1
                else:
                    self.graph_edges_in[id2][id1] = weight
        else:
            edge_out = {id2: weight}
            self.graph_edges_out[id1] = edge_out
            if id2 not in self.graph_edges_in.keys():
                edge_in2 = {id1: weight}
                self.graph_edges_in[id2] = edge_in2
            else:
                self.graph_edges_in[id2][id1] = weight
        self.MC = self.MC + 1
        self.edge_counter = self.edge_counter + 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if node_id not in self.graph_nodes.keys():
            node_temp = NodeGraph(node_id, pos)
            self.graph_nodes[node_id] = node_temp
            self.MC = self.MC + 1
            return True
        else:
            return False

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if node_id not in self.graph_nodes.keys():
            return False
        edge_out = self.all_out_edges_of_node(node_id)
        for key in edge_out.keys():
            del self.graph_edges_in[key][node_id]
            self.edge_counter = self.edge_counter - 1
        edge_in = self.all_in_edges_of_node(node_id)
        for key2 in edge_in.keys():
            del self.graph_edges_out[key2][node_id]
            self.edge_counter = self.edge_counter - 1
        if node_id in self.graph_edges_out.keys():
            del self.graph_edges_out[node_id]
        if node_id in self.graph_edges_in.keys():
            del self.graph_edges_in[node_id]
        del self.graph_nodes[node_id]
        self.MC = self.MC + 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 not in self.graph_nodes.keys() or node_id2 not in self.graph_nodes.keys():
            return False
        if node_id1 not in self.graph_edges_out.keys():
            return False
        if node_id2 not in dict(self.graph_edges_out[node_id1]).keys():
            return False
        del self.graph_edges_out[node_id1][node_id2]
        del self.graph_edges_in[node_id2][node_id1]
        self.edge_counter = self.edge_counter - 1
        self.MC = self.MC + 1
        return True

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.edge_counter

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        if id1 not in self.graph_edges_in.keys():
            return {}
        return self.graph_edges_in[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        if id1 not in self.graph_edges_out.keys():
            return {}
        return self.graph_edges_out[id1]

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return dict(self.graph_nodes)

    def __str__(self) -> str:
        graph_str = "graph details: \n"
        graph_str = graph_str + "number of nodes: " + str(len(self.graph_nodes)) + "\n"
        graph_str = graph_str + "number of edges: " + str(self.edge_counter) + "\n"
        graph_str = graph_str + "number of changes in the graph: " + str(self.MC) + "\n"
        graph_str = graph_str + " nodes:\n"
        for i in self.graph_nodes.keys():
            graph_str = graph_str + 'node: ' + str(i) + '  :connect to nodes: '
            for j in self.all_out_edges_of_node(i).keys():
                graph_str = graph_str + str(j) + ", "
            graph_str = graph_str + "\n"
        return graph_str

    def __repr__(self) -> str:
        graph_str = "graph details: \n"
        graph_str = graph_str + "number of nodes: " + str(len(self.graph_nodes)) + "\n"
        graph_str = graph_str + "number of edges: " + str(self.edge_counter) + "\n"
        graph_str = graph_str + "number of changes in the graph: " + str(self.MC) + "\n"
        graph_str = graph_str + " nodes:\n"
        for i in self.graph_nodes.keys():
            graph_str = graph_str + 'node: ' + str(i) + '  :connect to nodes: '
            for j in self.all_out_edges_of_node(i).keys():
                graph_str = graph_str + str(j) + ", "
            graph_str = graph_str + "\n"
        return graph_str

    def __eq__(self, other) -> bool:
        if isinstance(other, DiGraph) is False:
            return False
        if self.v_size() is not other.v_size() or self.e_size() is not other.e_size():
            return False
        for node_id in self.get_all_v().keys():
            if node_id not in other.get_all_v().keys():
                return False
            for neighbor in self.all_out_edges_of_node(node_id).keys():
                if neighbor not in other.all_out_edges_of_node(node_id).keys():
                    return False
                if self.get_edge(node_id, neighbor) is not other.get_edge(node_id, neighbor):
                    return False
        return True

