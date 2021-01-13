import random


class NodeGraph:
    """
    this class represent a node in a directed weighted graph
    """
    global key  # a unique key to the node
    global position   # position of the node, can be NONE or a x,y,z tuple
    global tag   # help in the algorithms class
    global information   # a information about the node
    global parent   # help in the algorithms class

    def __init__(self, key1: int, pos: tuple = None):
        """
        a constructor to the node
        reset the parent ,tag and the information
        """
        self.key = key1
        self.position = pos
        self.information = ""
        self.tag = -1
        self.parent = None


    def getKey(self) -> int:
        """
        @return: int, the key of the node
        """
        return self.key

    def getPosition(self) -> tuple:
        """
        @return: tuple or none, the position of the node
        """
        return self.position

    def getTag(self) -> float:
        """
        @return: float, the tag of the graph
        """
        return self.tag

    def setTag(self, tag_n: float):
        """
        set the tag of the node
        @param tag_n: the new value
        """
        self.tag = tag_n

    def getParent(self) -> int:
        """
        @return: float, the parent of the node
        """
        return self.parent

    def setParent(self, per_n: int):
        """
        set the parent of the node
        @param per_n: the new value
        """
        self.parent = per_n

    def getInfo(self) -> str:
        """
        @return: str, the information about the node
        """
        return self.information

    def setInfo(self, info_n: str):
        """
        set the information of the node
        @param info_n: the new value
        """
        self.information = info_n

    def __str__(self) -> str:
        """
        @return: str, the information about the node as a string , contain key and position
        """
        return "node key: " + str(self.key) + "node position: " + str(self.position) + "\n"

    def __repr__(self):
        """
        @return: str, the information about the node as a string , contain key and position
        """
        return "node key : " + str(self.key) + " node position:" + str(self.position) + "\n"

    def __eq__(self, other):
        """
        return true or false if the nodes are equal
        @return: bool, return if the two nodes are equal
        @param other: the object to compare with
        """
        if isinstance(other, NodeGraph) is False:
            return False
        if self.key == other.key:
            return True
        else:
            return False
