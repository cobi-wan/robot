from itertools import count
import cv2 as cv
from cv2 import MARKER_SQUARE
from cv2 import MARKER_TRIANGLE_DOWN
import numpy as np
import sys
from communication import send_update


## Robot Class Definitions ##
class partRunner:    
    def __init__(self, bNum, x, y, t, MAC):
        # Bot Number 
        self.botIndex = bNum
        self.MAC = MAC
        self.activated = False

        # Self coordinates. Updated in main loop. 
        self.xCord = x
        self.yCord = y
        self.tCord = t

        # Path updating variables
        self.currGoal = None
        self.arrived = False
        self.path = []
        self.dist_to_dest = 0
        self.dist_to_end = 0

        # Dimensions and speed values
        self.length = 14 # Dimensions of bot in inches
        self.width = 11
        self.maxSpeed = 1000 # Speed in inches per second. To be calibrated later
        self.minSpeed = 100
        

    def add(self, point):
        self.path.append(point)


class cart:
    numBots = 0
    
    def __init__(self, x, y, t):
        # Bot number
        self.botIndex = self.numBots
        cart.numBots += 1

        # Self coordinates. Updated in main loop.
        self.xCord = x
        self.yCord = y
        self.tCord = t

        # Path updating variables
        self.currGol = None
        self.arrived = False
        self.path = []
        self.dist_to_dest = 0
        self.dist_to_end = 0

        # Dimensions and speed values
        self.length = 36 # Dimensions of bot in inches
        self.width = 24
        self.maxSpeed = 1000 # Speed in inches per second. To be calibrated later
        self.minSpeed = 800

    def add(self, point):
        self.path.append(point)










## MAP Class Definition ## 
class environment:
    mapScale = 0.1 
    worldScale = 5
    width = int(2873*worldScale*mapScale)
    height = int(1615*worldScale*mapScale)
    dimensions = (width, height)
    botList = np.array([])
    timeStep = 0.02
    accuracy = 15
    calcRate = 5
    RFID_Dist2Node = 50

    def __init__(self, img, bots, graph, destinations):
        self.UI = cv.imread(img)
        self.UI = cv.resize(self.UI, self.dimensions, interpolation = cv.INTER_LINEAR)
        self.UIwBots = self.UI.copy()
        self.botList = bots
        self.network = graph
        # self.activeNetwork = graph
        self.destination_list = {}
        for i in self.botList:
            self.destination_list[i] = [0]
        for i in destinations:
            # destinations[i].insert(0, 0) # Ensure the bot always starts at node 0
            # for j in destinations[i]:
            self.addStop(i)
            # self.destination_list[self.botList[i]] = destinations[i]
        
    def robot2World(self, cords, botNum): 
        t = self.botList[botNum].tCord
        x = self.botList[botNum].xCord + cords[0]*np.cos(t) - cords[1]*np.sin(t)
        y = self.botList[botNum].yCord + cords[0]*np.sin(t) - cords[1]*np.cos(t)

        return [x, y]

    def robotPoints(self, botNum):
        bot = self.botList[botNum]
        L = bot.length * 2.54 * 2 # Parameters to be adjusted for robot size and camera resolution
        W = bot.width * 2.54 * 2

        w1 = self.robot2World((L/2, -W/2), botNum)
        w2 = self.robot2World((L/2, W/2), botNum)
        w3 = self.robot2World((-L/2, W/2), botNum)
        w4 = self.robot2World((-L/2, -W/2), botNum)
    
        p1 = (int(w1[0]*self.mapScale), int(w1[1]*self.mapScale))
        p2 = (int(w2[0]*self.mapScale), int(w2[1]*self.mapScale))
        p3 = (int(w3[0]*self.mapScale), int(w3[1]*self.mapScale))
        p4 = (int(w4[0]*self.mapScale), int(w4[1]*self.mapScale))

        pts = np.array([p1, p2, p3, p4])
        return pts

    def updateBotMarker(self):
        self.UIwBots = self.UI.copy()
        for i in self.botList:
            if i.activated:
                pts = self.robotPoints(i.botIndex)
                cv.drawContours(self.UIwBots, [pts], 0, (255, 0, 0), 1)
                front = self.robot2World((100, 0), i.botIndex)
                cv.drawMarker(self.UIwBots, (int(front[0]*self.mapScale), int(front[1]*self.mapScale)), (0, 0, 255), MARKER_TRIANGLE_DOWN, 5)
                cv.putText(self.UIwBots, str(i.botIndex), (int(i.xCord*self.mapScale), int(i.yCord*self.mapScale)), cv.FONT_HERSHEY_SIMPLEX, 0.35, (255, 0, 0), 1)
                if i.arrived == True:
                    cv.putText(self.UIwBots, "Bot " + str(i.botIndex) + " Arrived", (800, 25*i.botIndex + 50), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0))
                else: 
                    cv.putText(self.UIwBots, "Bot " + (str(i.botIndex)) + " in progress. Next nodes: " + ', '.join(str(i) for i in self.destination_list[i]), (800, 25*i.botIndex + 50), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0))

    def drawNodes(self):
        for i in self.network.nodes:
            cv.drawMarker(self.UI, (int(i.x*self.mapScale), int(i.y*self.mapScale)), (255, 0, 0), MARKER_SQUARE, 6)
            cv.putText(self.UI, str(i.label), (int(i.x*self.mapScale) + 10, int(i.y*self.mapScale) + 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

    def drawPaths(self):
        for i in self.network.edges:
            cv.line(self.UI, (int(i.n1x*self.mapScale), int(i.n1y*self.mapScale)), (int(i.n2x*self.mapScale), int(i.n2y*self.mapScale)), (230, 230, 230), 3)
            cv.line(self.UI, (int(i.n1x*self.mapScale), int(i.n1y*self.mapScale)), (int(i.n2x*self.mapScale), int(i.n2y*self.mapScale)), (0, 0, 0), 1)

    def addStop(self, nodeNum):
        # self.get_closest_bot()
        self.destination_list[self.botList[0]].append(nodeNum)
        return True 

    def get_closest_bot(self):
        max_dist = sys.maxsize
        for i in self.botList:
            if i.dist_to_end < max_dist:
                closest_bot = i
                max_dist = i.dist_to_end
        return closest_bot










## Graph Definitions ## 
class edge:
    count = 0

    def length(self):
        return np.sqrt((self.n1x - self.n2x)**2 + (self.n1y - self.n2y)**2)

    def __init__(self, node1, node2):
        self.label = self.count
        edge.count += 1
        self.n1 = node1
        self.n2 = node2
        self.n1x = node1.x
        self.n1y = node1.y
        self.n2x = node2.x
        self.n2y = node2.y
        self.len = self.length()

class node:
    edges = []
    count = 0

    def __init__(self, x, y, tag=None):
        self.label = self.count
        node.count += 1
        self.x = x
        self.y = y
        self.tag = tag


class graph:
    def __init__(self, nodes = None, edges = None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        if edges is None:
            edges = []
        self.edges = edges
        self.nodeNum = 0
        for i in nodes:
            if i.label > self.nodeNum:
                self.nodeNum = i.label
    
    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, node1, node2):
        self.edges.append(edge(node1, node2))
    
    def getOutEdges(self, node):
        outEdges = []
        for i in self.edges:
            if i.n1.label is node:
                outEdges.append((i.n2, i.len))
            if i.n2.label is node:
                outEdges.append((i.n1, i.len))
        return outEdges

    def removeEdges(self, rem):
        t = slice(len(rem))
        for i in reversed(rem):
            del(self.edges[i])
            

    