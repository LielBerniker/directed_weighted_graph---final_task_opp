import unittest

from src.NodeGraph import NodeGraph


class MyTestCase(unittest.TestCase):
    def test_node_key(self):
        node_1 = NodeGraph(0)
        self.assertEqual(0, node_1.getKey())
        node_2 = NodeGraph(1)
        self.assertEqual(1, node_2.getKey())

    def test_node_position(self):
        node_1 = NodeGraph(0,(534,436,2332))
        self.assertEqual(534, node_1.getPosition()[0])
        self.assertEqual(436, node_1.getPosition()[1])
        self.assertEqual(2332, node_1.getPosition()[2])
        node_2 = NodeGraph(1,(0,3,5))
        self.assertEqual(0, node_2.getPosition()[0])
        self.assertEqual(3, node_2.getPosition()[1])
        self.assertEqual(5, node_2.getPosition()[2])

    def test_node_tag(self):
        node_1 = NodeGraph(0)
        self.assertEqual(-1, node_1.getTag())
        node_1.setTag(45454540)
        self.assertEqual(45454540, node_1.getTag())
        node_2 = NodeGraph(1)
        self.assertEqual(-1, node_2.getTag())
        node_2.setTag(45454540)
        self.assertEqual(node_1.getTag(), node_2.getTag())

    def test_node_parent(self):
        node_1 = NodeGraph(0)
        self.assertIsNone(node_1.getParent())
        node_1.setParent(45)
        self.assertEqual(45, node_1.getParent())
        node_2 = NodeGraph(1)
        node_2.setParent(7)
        self.assertEqual(7, node_2.getParent())

    def test_node_information(self):
        node_1 = NodeGraph(0)
        self.assertEqual("", node_1.getInfo())
        node_1.setInfo("go on")
        self.assertEqual("go on", node_1.getInfo())
        node_2 = NodeGraph(1)
        node_2.setInfo("finish")
        self.assertEqual("finish", node_2.getInfo())

    def test_node_equal(self):
        node_1 = NodeGraph(0)
        node_2 = NodeGraph(54)
        node_3 = NodeGraph(5)
        node_4 = NodeGraph(5)
        node_5 = NodeGraph(0)

        self.assertTrue(node_1 == node_5)
        self.assertFalse(node_1 == node_2)
        self.assertTrue(node_3 == node_4)
        self.assertFalse(node_5 == node_4)
