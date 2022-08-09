import cv2 as cv
from cv2 import MARKER_SQUARE
from cv2 import MARKER_TRIANGLE_DOWN
import numpy as np
import sys
from WebAndAPI.request import Request
from PathPlanning.pathPlanning import updatePath

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

    def __init__(self, img, bots, graph):
        self.UI = cv.imread(img)
        self.UI = cv.resize(self.UI, self.dimensions, interpolation = cv.INTER_LINEAR)
        self.UIwBots = self.UI.copy()

        self.botList = bots
        self.botDict = {}
        self.activeBots = {}
        for i in self.botList:
            self.botDict[i.MAC] = i

        self.network = graph
        self.homeNode = graph.nodes[1]
        self.nodeDict = {}
        self.reachableWorkstations = []
        print("Workstations: ")
        for i in self.network.nodes:
            if i.ws is not None: 
                print("Workstation ID:", i.ws, "at Node:", i.label)
                self.nodeDict[i.ws] = i 
                self.reachableWorkstations.append(i.ws)
        # print(" ".join(str(i)+" "+str(self.nodeDict[i].tag) for i in self.nodeDict))

        self.requestQueue = []
        self.activeRequests = []
        self.completedRequests = []
        # self.destination_list = {}
        # for i in self.botList:
        #     self.destination_list[i] = []
        # for i in destinations:
            # destinations[i].insert(0, 0) # Ensure the bot always starts at node 0
            # for j in destinations[i]:
            # self.addStop(i)
            # self.destination_list[self.botList[i]] = destinations[i]

        
    def robot2World(self, cords, bot): 
        t = bot.tCord
        x = bot.xCord + cords[0]*np.cos(t) - cords[1]*np.sin(t)
        y = bot.yCord + cords[0]*np.sin(t) - cords[1]*np.cos(t)

        return [x, y]

    def robotPoints(self, bot):
        L = bot.length * 2.54 * 2 # Parameters to be adjusted for robot size and camera resolution
        W = bot.width * 2.54 * 2

        w1 = self.robot2World((L/2, -W/2), bot)
        w2 = self.robot2World((L/2, W/2), bot)
        w3 = self.robot2World((-L/2, W/2), bot)
        w4 = self.robot2World((-L/2, -W/2), bot)
    
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
                pts = self.robotPoints(i)
                cv.drawContours(self.UIwBots, [pts], 0, (0, 0, 0), 1)
                front = self.robot2World((100, 0), i)
                cv.drawMarker(self.UIwBots, (int(front[0]*self.mapScale), int(front[1]*self.mapScale)), (0, 0, 255), MARKER_TRIANGLE_DOWN, 5)
                cv.putText(self.UIwBots, str(i.botIndex), (int(i.xCord*self.mapScale), int(i.yCord*self.mapScale)), cv.FONT_HERSHEY_SIMPLEX, 0.35, (255, 0, 0), 1)
                if i.arrived == True:
                    cv.putText(self.UIwBots, "Bot " + str(i.botIndex) + ": Arrived", (800, 25*i.botIndex + 50), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0))
                else: 
                    cv.putText(self.UIwBots, "Bot " + (str(i.botIndex)) + ": in progress. Next nodes: " + str(i.currentGoal), (800, 25*i.botIndex + 50), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0))# + ', '.join(str(j) for j in self.destination_list[i]))
                cv.putText(self.UIwBots, str(i.dist_to_end), (200, 25*i.botIndex + 550), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0))
                cv.putText(self.UIwBots, "Bot: "+str(i.botIndex)+" path:"+", ".join(str(j[0].label) for j in i.path), (200, 25*i.botIndex + 500), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0))

                # 
    def drawNodes(self):
        for i in self.network.nodes:
            if i.ws is not None:
                cv.drawMarker(self.UI, (int(i.x*self.mapScale), int(i.y*self.mapScale)), (0, 0, 255), MARKER_SQUARE, 6)
            else:
                cv.drawMarker(self.UI, (int(i.x*self.mapScale), int(i.y*self.mapScale)), (255, 0, 0), MARKER_SQUARE, 6)
            cv.putText(self.UI, str(i.label), (int(i.x*self.mapScale) + 10, int(i.y*self.mapScale) + 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

    def drawPaths(self):
        for i in self.network.edges:
            cv.line(self.UI, (int(i.n1x*self.mapScale), int(i.n1y*self.mapScale)), (int(i.n2x*self.mapScale), int(i.n2y*self.mapScale)), (230, 230, 230), 3)
            cv.line(self.UI, (int(i.n1x*self.mapScale), int(i.n1y*self.mapScale)), (int(i.n2x*self.mapScale), int(i.n2y*self.mapScale)), (0, 0, 0), 1)

    def get_closest_bot_Dist2End(self):
        max_dist = sys.maxsize
        for i in self.botList:
            print("Bot: ", i.botIndex, "Distance to end: ", i.dist_to_end, "Distance to destination: ", i.dist_to_dest)
            if i.dist_to_end < max_dist:
                closest_bot = i
                max_dist = i.dist_to_end
        print(closest_bot.botIndex)
        return closest_bot

    def node2wc(self, node):
        for i in self.network.nodes:
            if i.label == node:
                return i.ws
        return None

    def wc2node(self, wc):
        for i in self.network.nodes:
            if i.ws == wc:
                return i
        return None

    def createRequest(self, pickup, dropoff):
        # Find pickup node
        pickup = self.nodeDict[pickup]
        print("Pickup from:", pickup.label)
        # If there is a dropoff create it as a request and pass to the pickup request
        if dropoff is not None:
            dropoff = self.nodeDict[dropoff]
            print("Dropoff at:", dropoff.label)
            dropoffReq = Request(dropoff)
        else:
            dropoffReq = None
        pickupReq = Request(pickup, dropoffReq)

        # If there are no active bots append the request to the unassigned queue
        if not len(self.activeBots): 
            print("No Bots active")
            self.requestQueue.append(pickupReq)
            if dropoff is not None:
                self.requestQueue.append(dropoffReq)
        # Otherwise call addStop on pickup and then dropoff
        else: 
            self.addStop(pickupReq) # addStop handles both pickup and dropoff addition to robot path
        return (pickupReq, dropoffReq)



    def addStop(self, pickupReq):
        # Choose which bot to send
        soonestEnd = sys.maxsize
        for bot in self.activeBots: 
            if self.activeBots[bot].dist_to_end < soonestEnd: 
                chosenBot = self.activeBots[bot]
        print("Bot assigned to request: ", pickupReq.requestID, ": ", chosenBot.botIndex)
                    
        # Append given request to that bot 
        chosenBot.requestList.append(pickupReq)
        pickupLoc = pickupReq.destination
        dropoffLoc = None
        if pickupReq.next is not None:
            chosenBot.requestList.append(pickupReq.next)
            dropoffLoc = pickupReq.next.destination


        # Update chosen bots dist_to_end variable and add requests to its path 
        updatePath(self, chosenBot, pickupLoc, dropoffLoc, pickupReq.requestID)
        return chosenBot
