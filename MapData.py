from turtle import update
import cv2 as cv
from cv2 import MARKER_SQUARE
import time
import numpy as np
import platform
import sys
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

    b1 = partRunner(nodes[0].x, nodes[0].y, 0)
    b2 = partRunner(nodes[0].x, nodes[0].y, np.pi/2)
    b3 = partRunner(nodes[0].x, nodes[0].y, np.pi)
    bList = np.array([b1, b2, b3])

    return bList, g

def calcSpeed(xDist, yDist, max, min):
        dist = np.sqrt(xDist**2 + yDist**2)
        xComp = xDist/dist
        yComp = yDist/dist
        if dist > max:
            return [xComp*max, yComp*max]
        else: 
            spd = [xComp*dist*1.2, yComp*dist*1.2]
            if np.sqrt(spd[0]**2 + spd[1]**2) < min:
                return [xComp*min, yComp*min]
            return spd

def paths(g, n1):
    unvisited = g.nodes.copy()
    shortestPath = {}
    previous = {}
    maxVal = sys.maxsize
    for i in unvisited:
        shortestPath[i] = maxVal
    shortestPath[n1] = 0

    while unvisited: 
        currentMin = None
        for i in unvisited: 
            if currentMin == None:
                currentMin = i
            elif shortestPath[i] < shortestPath[currentMin]:                
                currentMin = i

        neighbors = g.getOutEdges(currentMin.label)
        
        for i in neighbors:
            temp = shortestPath[currentMin] + i[1]
            if temp < shortestPath[i[0]]:
                shortestPath[i[0]] = temp
                previous[i[0]] = currentMin
        unvisited.remove(currentMin)
    return previous, shortestPath

def getResult(previous, shortest, start, target):
    path = []
    node = target

    while node != start:
        path.append(node)
        node = previous[node]
    path.append(start)
    return reversed(path), shortest[target]
        
if __name__ == '__main__':

    # Initial running stuff
    cv.destroyAllWindows()
    bList, g = startUp()
    if platform.system() == 'Windows':
        file = "ImageFiles\BlankMap.png"
    else: 
        file = "ImageFiles/BlankMap.png"
    env = environment(file, bList, g)
    env.updateBotMarker() 
    env.drawPaths()
    env.drawNodes()
    
    # Temporary setup stuff. Delete Later 
    env.botList[0].add(env.network.nodes[1])
    env.botList[0].add(env.network.nodes[3])
    env.botList[0].add(env.network.nodes[5])
    env.botList[0].add(env.network.nodes[6])

    env.botList[1].add(env.network.nodes[10])
    env.botList[1].add(env.network.nodes[9])
    env.botList[1].add(env.network.nodes[8])

    env.botList[2].add(env.network.nodes[8])
    env.botList[2].add(env.network.nodes[7])
    env.botList[2].add(env.network.nodes[6])

    # Nice little printy guys
    # for i in env.botList:
    #     print(i.botIndex)
    # for i in env.network.edges:
    #     print(i.label, ": (", i.n1.x, ", ", i.n1.y, "), (", i.n2.x, ", ", i.n2.y, ")")

    try:
        tS = time.monotonic_ns()
        while True:
            if time.monotonic_ns() - tS > 1000000 * env.timeStep:
                env.updateBotMarker()
                cv.imshow("Map", env.UIwBots)
                cv.waitKey(int(env.timeStep*1000))
                for i in env.botList:
                    if i.path == []:                        # If its at the goal dont move
                        continue

                    if (i.xCord - i.path[0].x) != 0:        # Set the angle of movement
                        i.tCord = np.arctan((i.yCord - i.path[0].y)/(i.xCord - i.path[0].x)) # - np.pi/2
                    elif (i.yCord - i.path[0].y) > 0:
                        i.tCord = -np.pi/2 
                    else:
                        i.tCord = np.pi/2
                    # print("Bot #:", i.botIndex, "is should be moving at an angle", i.tCord*180/np.pi)
                    # print("Its goal point is at (", i.path[0].x, ",", i.path[0].y, ")")
                    xDist = i.path[0].x - i.xCord
                    yDist = i.path[0].y - i.yCord
                    if abs(xDist) > 15 or abs(yDist) > 15: 
                        speeds = calcSpeed(xDist, yDist, i.maxSpeed, i.minSpeed)
                        i.xCord += speeds[0]*env.timeStep
                        i.yCord += speeds[1]*env.timeStep
                    else:
                        del(i.path[0]) 
                        
                tS = time.monotonic_ns()


    except KeyboardInterrupt: # If you want to stop the program press crtl + c
        #cv.destroyAllWindows
        # cv.imshow("Map", env.UIwBots)
        # cv.waitKey(0)
        print("Aww, you stopped it. Whats wrong with you?")

    