import cv2 as cv
import time
import numpy as np
import sys
import csv
from Classes import environment
from Classes import partRunner
from Classes import edge
from Classes import node
from Classes import graph

def startUp():
    fileName = "nodeLocations.csv"
    nodes = []
    edges = []
    rows = []
    with open(fileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            nodes.append(node(int(row[1]), int(row[2])))
            for i in row[3:]:
                if i != '':
                    edges.append(edge(nodes[int(i)], nodes[int(row[0])]))
            print()
        print("Total no of rows: %d"%(csvreader.line_num))
    
    for i in edges:
        print("Node 1: ", i.n1.label, "Node 2: ", i.n2.label)
    # for i in nodes:
    #     print("Node: ", i.label, "X: ", i.x, "Y: ", i.y)
    

    

    # g = graph(nodes, edges)

    # b1 = partRunner(nodes[0].x, nodes[0].y, 0)
    # b2 = partRunner(nodes[0].x, nodes[0].y, np.pi/2)
    # b3 = partRunner(nodes[0].x, nodes[0].y, np.pi)
    # bList = np.array([b1, b2, b3])

    # return bList, g


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

# [bList, g] = startUp()
# for i in g.edges:
#     print(i.label)
# print()
# print(len(g.edges))
# print()
# g.removeEdges([0, 1, 2, 3, 4, 5, 6, 7])
# print()
# for i in g.edges:
#     print(i.label)
# print()
# print(len(g.edges))
# print()

startUp()