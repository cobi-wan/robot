from cProfile import run
from re import M
from turtle import update
import cv2 as cv
from cv2 import MARKER_SQUARE
import time
import numpy as np
import platform
import sys
import csv
from Classes import partRunner
from Classes import cart
from Classes import environment
from Classes import edge
from Classes import node
from Classes import graph

def startUp():
    fileName = "nodeLocations.csv"
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

    b1 = partRunner(nodes[1].x, nodes[1].y, 0)
    b2 = partRunner(nodes[1].x, nodes[1].y, np.pi/2)
    b3 = partRunner(nodes[1].x, nodes[1].y, np.pi)
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

def path(g, n1):
    unvisited = g.nodes.copy() # Set all nodes to unvisited
    shortestPath = {}
    previous = {}
    maxVal = sys.maxsize
    for i in unvisited: # Set the shortestPath to all nodes to the max system size
        shortestPath[i] = maxVal
    shortestPath[n1] = 0 # Shortest path to the current node is 0

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
        
def runDijkstras(environ, calledNodes):
    botNum = calledNodes[0]
    [curr, dest] = calledNodes[1]
    previous, shortestPath = path(environ.network, environ.network.nodes[curr])
    path1, length = getResult(previous, shortestPath, environ.network.nodes[curr], environ.network.nodes[dest])
    for i in path1:
        environ.botList[botNum].add(environ.network.nodes[i.label])

def getCurrLocation(environ, botNum):
    for i in environ.network.nodes:
        if abs(environ.botList[botNum].xCord - i.x) < 10 and abs(environ.botList[botNum].yCord - i.y) < 10:
            return i
    return environ.network.nodes[0]


if __name__ == '__main__':

    # Initial running stuff
    cv.destroyAllWindows()

    # Run startup procedure to read in nodes and create network 
    bList, g = startUp()

    # Load in blank image in given folder. Allow for Windows and Mac OS
    if platform.system() == 'Windows':
        file = "ImageFiles\BlankMap.png"
    else: 
        file = "ImageFiles/BlankMap.png"
    
    # Create environment and draw items given in setup
    env = environment(file, bList, g)
    env.updateBotMarker() 
    env.drawPaths()
    env.drawNodes()
    print("*******************")
    print("Network Initialized")
    print("*******************")


    runDijkstras(env, [0, [1, 19]])
    runDijkstras(env, [1, [1, 27]])
    runDijkstras(env, [2, [1, 10]])

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
                    xDist = i.path[0].x - i.xCord
                    yDist = i.path[0].y - i.yCord
                    if abs(xDist) > 15 or abs(yDist) > 15: 
                        speeds = calcSpeed(xDist, yDist, i.maxSpeed, i.minSpeed)
                        i.xCord += speeds[0]*env.timeStep
                        i.yCord += speeds[1]*env.timeStep
                    else:
                        del(i.path[0]) 
                        
                tS = time.monotonic_ns()
                
            for i in env.botList:
                if len(i.path) == 0:
                    t = getCurrLocation(env, i.botIndex)
                    runDijkstras(env, [i.botIndex, [t.label, 1]])
                    
            

    except KeyboardInterrupt: # If you want to stop the program press crtl + c
        # cv.imshow("Map", env.UIwBots)
        # cv.waitKey()
        print("Aww, you stopped it. Whats wrong with you?")

    