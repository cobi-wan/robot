import cv2 as cv
import time
import numpy as np
import sys
from Classes import environment
from Classes import partRunner
from Classes import edge
from Classes import node
from Classes import graph

def startUp():
    nodes = [node(5760, 3240), 
            node(7000, 3240), 
            node(11000, 3240), 
            node(7000, 4500), 
            node(11000, 4500), 
            node(9000, 4500), 
            node(9000, 5500), 
            node(2500, 5500), 
            node(2500, 3240),
            node(2500, 500),
            node(5760, 500)]

    edges = [edge(nodes[0], nodes[1]),
            edge(nodes[0], nodes[8]),
            edge(nodes[0], nodes[10]),
            edge(nodes[1], nodes[2]), 
            edge(nodes[1], nodes[3]),
            edge(nodes[2], nodes[4]),
            edge(nodes[3], nodes[5]),
            edge(nodes[4], nodes[5]),
            edge(nodes[5], nodes[6]),
            edge(nodes[6], nodes[7]),
            edge(nodes[7], nodes[8]),
            edge(nodes[8], nodes[9]),
            edge(nodes[9], nodes[10])]

    g = graph(nodes, edges)

    b1 = partRunner(nodes[0].x, nodes[0].y, 0)
    b2 = partRunner(nodes[0].x, nodes[0].y, np.pi/2)
    b3 = partRunner(nodes[0].x, nodes[0].y, np.pi)
    bList = np.array([b1, b2, b3])

    return bList, g


# def paths(g, n1):
#     unvisited = g.nodes.copy()
#     shortestPath = {}
#     previous = {}
#     maxVal = sys.maxsize
#     for i in unvisited:
#         shortestPath[i] = maxVal
#     shortestPath[n1] = 0

#     while unvisited:                                                        # While there are still unvisited nodes
#         currentMin = None
#         for i in unvisited:                                                 # Loop through all unvisited nodes
#             if currentMin == None:
#                 currentMin = i                                              # Set the current minimum node to the first in unvisited
#             elif shortestPath[i] < shortestPath[currentMin]:                
#                 currentMin = i

#         neighbors = g.getOutEdges(currentMin.label)
        
#         for i in neighbors:
#             temp = shortestPath[currentMin] + i[1]
#             if temp < shortestPath[i[0]]:
#                 shortestPath[i[0]] = temp
#                 previous[i[0]] = currentMin
#         unvisited.remove(currentMin)
#     return previous, shortestPath

# def getResult(previous, shortest, start, target):
#     path = []
#     node = target

#     while node != start:
#         path.append(node)
#         node = previous[node]
#     path.append(start)
#     return reversed(path), shortest[target]

# [bList, g] = startUp()
# previous, p = paths(g, g.nodes[8])
# path1, length = getResult(previous, p, g.nodes[8], g.nodes[5])

# for i in path1:
#     print(i.label)
# print(length)
# for i in p:
#     print(p[i])
#     print()

# print(type(previous))
# for i in previous:
#     print(previous[i].label)

[bList, g] = startUp()
for i in g.edges:
    print(i.label)
print()
print(len(g.edges))
print()
g.removeEdges([0, 1, 2, 3, 4, 5, 6, 7])
print()
for i in g.edges:
    print(i.label)
print()
print(len(g.edges))
print()
