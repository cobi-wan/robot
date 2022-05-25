import cv2 as cv
import time
import numpy as np
from Classes import partRunner
from Classes import cart
from Classes import environment
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

    b1 = partRunner(1000, 600, 0)
    b2 = partRunner(1000, 2000, np.pi/2)
    bList = np.array([b1, b2])

    return bList, g

def drawPaths(paths):
    map = MAP.copy()                   
    cv.drawContours(map, [paths], 0, (255, 255, 255), 2)
    cv.imshow('Map', map)
    cv.waitKey(33)
    pass

if __name__ == '__main__':
    cv.destroyAllWindows()
    bList, g = startUp()
    env = environment("ImageFiles\BlankMap.png", bList, g)
    #defineMap([(p1, p2), (p2, p3)])
    env.updateBotPos()
    env.drawNodes() 
    env.drawPaths()
    try:
        while True:
            cv.imshow("Map", env.UI)
            cv.waitKey(100)
    except KeyboardInterrupt: # If you want to stop the program press crtl + c
        cv.destroyAllWindows
        print("Aww, you stopped it. Whats wrong with you?")

    # for i in Map.network.edges:
    #     print(i.label, ": (", i.n1.x, ", ", i.n1.y, "), (", i.n2.x, ", ", i.n2.y, ")")
    # try: 
    #     for i in range(100):
    #         updateMap(Map)
    #         posRobx += 10
    #         posRoby += 10
    # except KeyboardInterrupt:
    #     print("Darn")