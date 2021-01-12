import random


class NodeGraph:
    global key
    global position
    global tag
    global information
    global parent

    def __init__(self, key1: int, pos: tuple = None):
        self.key = key1
        self.position = pos
        self.information = ""
        self.tag = -1
        self.parent = None
        self.component = -1

    def getKey(self) -> int:
        return self.key

    def getPosition(self) -> tuple:
        return self.position

    def getTag(self) -> float:
        return self.tag

    def setTag(self, tag_n: float):
        self.tag = tag_n

    def getParent(self) -> int:
        return self.parent

    def setParent(self, per_n: int):
        self.parent = per_n

    def getInfo(self) -> str:
        return self.information

    def setInfo(self, info_n: str):
        self.information = info_n

    def __str__(self) -> str:
        return "node key: " + str(self.key) + "node position: " + str(self.position) + "\n"

    def __repr__(self):
        return "node key : " + str(self.key) + " node position:" + str(self.position) + "\n"

    def __eq__(self, other):
        if isinstance(other, NodeGraph) is False:
            return False
        if self.key == other.key:
            return True
        else:
            return False
