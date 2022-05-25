from itertools import count
from re import X
import cv2 as cv
import time
from cv2 import MARKER_SQUARE
import numpy as np


## Robot Class Definitions ##
class partRunner:
    numBots = 0
    path = []
    path.append(1) # Assume the bot always has to go to the first node first
    length = 14 # Dimensions of bot in inches
    width = 11
    maxSpeed = 1
    
    def __init__(self, x, y, t):
        self.botIndex = self.numBots
        partRunner.numBots += 1
        self.xCord = x
        self.yCord = y
        self.tCord = t

    def add(self, point):
        self.path.append(point)

class cart:
    numBots = 0
    path = []
    path.append(1) # Assume the bot always has to go to the first node first
    length = 36 # Dimensions of bot in inches
    width = 24
    maxSpeed = 0.75

    
    def __init__(self, x, y, t):
        self.botIndex = self.numBots
        cart.numBots += 1
        self.xCord = x
        self.yCord = y
        self.tCord = t

    def add(self, point):
        self.path.append(point)










## MAP Class Definition ## 
class environment:
    mapScale = 0.1 
    worldScale = 10
    width = int(1152*worldScale*mapScale)
    height = int(648*worldScale*mapScale)
    dimensions = (width, height)
    botList = np.array([])

    def __init__(self, img, bots, graph):
        self.UI = cv.imread(img)
        self.UI = cv.resize(self.UI, self.dimensions, interpolation = cv.INTER_LINEAR)
        self.botList = bots
        self.network = graph

    def robot2World(self, cords, botNum): 
        t = self.botList[botNum].tCord
        x = self.botList[botNum].xCord + cords[0]*np.cos(t) - cords[1]*np.sin(t)
        y = self.botList[botNum].yCord + cords[0]*np.sin(t) - cords[1]*np.cos(t)

        return [x, y]

    def robotPoints(self, botNum):
        bot = self.botList[botNum]
        L = bot.length * 2.54 * 2 # Parameters to be adjusted for robot size and camera resolution
        W = bot.width *2.54 * 2

        w1 = self.robot2World((-W/2, L/2), botNum)
        w2 = self.robot2World((W/2, L/2), botNum)
        w3 = self.robot2World((W/2, -L/2), botNum)
        w4 = self.robot2World((-W/2, -L/2), botNum)
    
        p1 = (int(w1[0]*self.mapScale), self.height - int(w1[1]*self.mapScale))
        p2 = (int(w2[0]*self.mapScale), self.height - int(w2[1]*self.mapScale))
        p3 = (int(w3[0]*self.mapScale), self.height - int(w3[1]*self.mapScale))
        p4 = (int(w4[0]*self.mapScale), self.height - int(w4[1]*self.mapScale))

        pts = np.array([p1, p2, p3, p4])
        return pts


    def updateBotPos(self):
        tempMap = self.UI.copy() 
        for i in self.botList:
            pts = self.robotPoints(i.botIndex)
            cv.drawContours(tempMap, [pts], 0, (255, 0, 0), 1)
        cv.imshow('Map', tempMap)

    def drawNodes(self):
        for i in self.network.nodes:
            cv.drawMarker(self.UI, (int(i.x*self.mapScale), int(i.y*self.mapScale)), (255, 0, 0), MARKER_SQUARE, 6)
        cv.imshow('Map', self.UI)

    def drawPaths(self):
        for i in self.network.edges:
            cv.line(self.UI, (int(i.n1.x*self.mapScale), int(i.n1.y*self.mapScale)), (int(i.n2.x*self.mapScale), int(i.n2.y*self.mapScale)), (0, 0, 0), 2)
        cv.imshow('Map', self.UI)










## Graph Definitions ## 
class edge:
    count = 0

    def length(self):
        return np.sqrt((self.n1.x - self.n2.x)**2 + (self.n1.y - self.n2.y)**2)

    def __init__(self, node1, node2):
        self.label = self.count
        edge.count += 1
        self.n1 = node1
        self.n2 = node2
        self.len = self.length()

class node:
    edges = []
    count = 0

    def __init__(self, x, y):
        self.label = self.count
        node.count += 1
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
# class paths:
#     def __init__(self, gdict=None):
#         if gdict is None:
#             gdict = {}
#         self.gdict = gdict

#     def edges(self):
#         return self.findEdges()
    
#     def addEdge(self, edge):
#         edge = set(edge)
#         (vrtx1, vrtx2) = tuple(edge)
#         if vrtx1 in self.gdict:
#             self.gdict[vrtx1].append(vrtx2)
#         else: 
#             self.gdict[vrtx1] = [vrtx2]

#     def findEdges(self):
#         edgeName = []
#         for vrtx in self.gdict:
#             for nxtvrtx in self.gdict[vrtx]:
#                 if {nxtvrtx, vrtx} not in edgeName:
#                     edgeName.append({vrtx, nxtvrtx})
#         return edgeName


