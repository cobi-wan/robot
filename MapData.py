import cv2 as cv
import time
import numpy as np
from Classes import partRunner
from Classes import cart
from Classes import MAP
from Classes import edge
from Classes import node
from Classes import graph

# Robot path points
p1 = (int(1), int(1))
p2 = (int(100), int(100))
p3 = (int(100), int(400))

# Initial Robot Position 
posRobx = 1000
posRoby = 1000
posRobt = 0

def startUp():
    b1 = partRunner(1000, 600, 0)
    b2 = partRunner(1000, 2000, np.pi/2)
    bList = np.array([b1, b2])
    
    # n1 = np.array([5760, 3240])
    # n2 = np.array([7000, 3240])
    # n3 = np.array([11000, 3240])
    # n4 = np.array([7000, 4500])
    # n5 = np.array([11000, 4500])
    # n6 = np.array([9000, 4500])
    # n7 = np.array([9000, 5500])
    # n8 = np.array([2500, 5500])
    # n9 = np.array([2500, 3240])
    # n10 = np.array([2500, 500])
    # n11 = np.array([5760, 500])
    # nodes = np.array([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11])
    # p1 = np.array([1, 2])
    # p2 = np.array([1, 11, 10])
    # p3 = np.array([1, 11])
    # p4 = np.array([2, 3])
    # p5 = np.array([2, 4, 6])
    # p6 = np.array([3, 5, 6])
    # p7 = np.array([6, 7, 8, 9])
    # p8 = np.array([9, 10])
    # paths = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
    nodes = [node(5760, 3240), node(7000, 3240), node(11000, 3240), node(7000, 4500)]
    edges = [edge(nodes[0], nodes[1]), edge(nodes[1], nodes[2]), edge(nodes[1], nodes[3])]
    g = graph(nodes, edges)

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
    Map = MAP("lib\BlankMap.png", bList, g)
    #defineMap([(p1, p2), (p2, p3)])
    Map.updateBotPos()
    Map.drawNodes()
    Map.drawPaths()
    # try: 
    #     for i in range(100):
    #         updateMap(Map)
    #         posRobx += 10
    #         posRoby += 10
    # except KeyboardInterrupt:
    #     print("Darn")