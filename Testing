import cv2 as cv
import time
import numpy as np

## Graph Definitions ## 
class edge:

    def length(self):
        return np.sqrt((self.n1.x - self.n2.x)**2 + (self.n1.y - self.n2.y)**2)

    def __init__(self, node1, node2):
        self.n1 = node1
        self.n2 = node2
        self.len = self.length()

class node:
    edges = []

    def __init__(self, x, y):
        self.x = x
        self.y = y

class graph:
    def __init__(self, nodes = None, edges = None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        if edges is None:
            edges = []
        self.edges = edges
    
    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, node1, node2):
        pass

nodes = [node(5760, 3240), node(7000, 3240), node(11000, 3240), node(7000, 4500)]
edges = [edge(nodes[0], nodes[1]), edge(nodes[1], nodes[2]), edge(nodes[1], nodes[3])]
g = graph(nodes, edges)