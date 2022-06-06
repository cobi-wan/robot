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
    fileName = "testingNodeLocations.csv"
    nodes = []
    edges = []
    # Read in nodes and edges from filename
    with open(fileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # Skip the first line
        for row in csvreader:
            nodes.append(node(int(row[1]), int(row[2])))
            for i in row[3:]:
                if i != '':
                    edges.append(edge(nodes[int(i)], nodes[int(row[0])]))
            # print()
        # print("Total no of rows: %d"%(csvreader.line_num))

    g = graph(nodes, edges)
    b1 = partRunner(nodes[1].x, nodes[0].y, 0)
    b2 = partRunner(nodes[1].x, nodes[0].y, np.pi/2)
    b3 = partRunner(nodes[1].x, nodes[0].y, np.pi)
    bList = np.array([b1, b2, b3])

    return bList, g

def path(g, n1):
    unvisited = g.nodes.copy() # Set all nodes to unvisited
    shortestPath = {}
    previous = {}
    maxVal = sys.maxsize
    for i in unvisited: # Set the shortestPath to all nodes to the max system size
        shortestPath[i] = maxVal
    shortestPath[n1] = 0 # Shortest path to the current node is 0

    # While 
    while unvisited: 
        currentMin = None
        for i in unvisited: 
            # print("Node:", i.label, "Shortestpath:", shortestPath[i])
            if currentMin == None: # Start at first node in unvisited
                currentMin = i
            elif shortestPath[i] < shortestPath[currentMin]:                
                currentMin = i
        # print(currentMin.label)
        # print()
        neighbors = g.getOutEdges(currentMin.label)
        print(currentMin.label, shortestPath[currentMin])
        for i in neighbors:
            temp = shortestPath[currentMin] + i[1]
            print(temp)
            if temp < shortestPath[i[0]]:
                shortestPath[i[0]] = temp
                previous[i[0]] = currentMin
        print()
        unvisited.remove(currentMin)
    return previous, shortestPath

def test():
        # Initial running stuff
        cv.destroyAllWindows()

        bList, g = startUp()
        file = "ImageFiles\BlankMap.png"
        # Create environment and draw items given in setup
        env = environment(file, bList, g)
        env.updateBotMarker() 
        env.drawPaths()
        env.drawNodes()
        prev, shortest = path(env.network, env.network.nodes[0])

        env.updateBotMarker()
        cv.imshow("Map", env.UIwBots)
        cv.waitKey()
