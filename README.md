# directed weighted graph

This repository represents a structure of a directed weighted graph, with some algorithms that can be used on the graph. 

### uses of the program:
can be used as a GPS, can contain many city locations, and calculate the shortest path from one destination to another
can be used as a shape creator, create mane nodes and edges for a shape, and calculate the shortest path from one node to another. 
Part 1:
structure:
the graph is built from vertices that are represented by the NodeGraph class. 
. the graph is represented by the DiGraph class that inherits from the graph interface. the algorithms of the graph are represented by the GraphAlgo, which inherits from the GraphAlgointerface.

### the graph:
the graph class includes functions such as:
* add node - add a new node to the graph
* add_edge - add a new edge to the graph between two vertices
* get_all_ v - return a dictionary contains all the graph vertices 
* remove node - remove a vertex from the graph
* remove edge - remove an edge between two vertices
* all_in_edges_of_node-returns a dictionary of all nodes connected to the given node.
* all_out_edeges_of_node-returns a dictionary of all nodes connected from the given node.
* e_size - return the number of edges in the graph
* v_size-returns the number of vertices in the graph
* get_mc-return the number of changes computed on the graph
 
### the graph algorithms :
the graph algorithms class includes functions such as:
* initiate_graph - initiate the graph algorithm to point on a graph
* is connected - return true if all of the graph vertices have a path from one to another.
* shortest_Path - returns the distance of the shortest path from one vertex to another and a list with the id of the path vertices.
* save_from_json- save a graph from the graph algorithms as a Jasonobject
* load_from_json - load a graph from a Jasonobject to the graph algorithms
* conected_component-returns a list contains all id of the nodes in the connected component of a given vertex.
* conected_components-returns a list of all the connected components.
* plot_graph-plots the graph

### part 3:
in the 3 part of the project, we make a comparison between the run times of our python project to a previous java project .and also to networkX graph algorithms.

### particulars functions that based on an external code:
shortest path Dist and shortest Path based on the "Dijkstra's " algorithm.
connected components make use of the BFS algorithm.

### links:
Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
breadth-first search algorithm: https://en.wikipedia.org/wiki/Breadth-first_search


