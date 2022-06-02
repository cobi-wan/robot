from cProfile import run
from logging import exception
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


# Reads in mapping file that specifies node locations and paths
def startUp():
    fileName = "nodeLocations.csv"
    nodes = []
    edges = []
    # Read in nodes and edges from filename
    with open(fileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # Skip the first line. When saving the CSV it always has weird charaters at the first index. 
        # Iterate through each row in the file. Each row has a node location and a list of nodes it is connected to 
        # Each connection must be to a node that is already created 
        for row in csvreader: 
            nodes.append(node(int(row[1]), int(row[2])))
            for i in row[3:]:
                if i != '':
                    edges.append(edge(nodes[int(i)], nodes[int(row[0])]))

    g = graph(nodes, edges)

    b1 = partRunner(nodes[1].x, nodes[1].y, 0)
    b2 = partRunner(nodes[1].x, nodes[1].y, np.pi/2)
    # b3 = partRunner(nodes[1].x, nodes[1].y, np.pi)
    bList = np.array([b1, b2])

    return bList, g


# Calculate the speed the robot should be moving
def calcSpeed(xDist, yDist, max, min, RFID_Dist):
        dist = np.sqrt(xDist**2 + yDist**2)
        xComp = xDist/dist
        yComp = yDist/dist
        if dist > RFID_Dist:
            return [xComp*max, yComp*max]
        else: 
            return [xComp*min, yComp*min]
            

# Runs Dijsktras from n1 to all other nodes on the network g
def path(g, n1):
    unvisited = g.nodes.copy() # Set all nodes to unvisited
    shortestPath = {}
    previous = {}
    maxVal = sys.maxsize
    for i in unvisited: # Set the shortestPath to all nodes to the max system size
        shortestPath[i] = maxVal
    shortestPath[n1] = 0 # Shortest path to the current node is 0

    # While some nodes are still unvisited 
    while unvisited: 
        currentMin = None
        # Find the node with the shortest current length
        for i in unvisited: 
            if currentMin == None:
                currentMin = i
            elif shortestPath[i] < shortestPath[currentMin]:                
                currentMin = i

        # Find all neighbors of that node
        neighbors = g.getOutEdges(currentMin.label)
        for i in neighbors:
            temp = shortestPath[currentMin] + i[1]
            if temp < shortestPath[i[0]]:
                shortestPath[i[0]] = temp
                previous[i[0]] = currentMin
        unvisited.remove(currentMin)
    return previous, shortestPath


# Evaluate the result of Dijkstras and return the node ordered path
def getResult(previous, shortest, start, target):
    path = []
    if len(previous) != len(env.network.nodes) - 2:
        raise Exception("Invalid path length")
    node = target
    while node != start:
        path.append(node)
        node = previous[node]
    path.append(start)
    return reversed(path), shortest[target]


# Calculates path from given node for a current location and goal location and add to path 
# runDijkstras(env, [bNum, [from, to]])  
def runDijkstras(environ, calledNodes):
    # Setup variables
    botNum = calledNodes[0]
    [curr, dest] = calledNodes[1]
    environ.botList[botNum].currGoal = environ.network.nodes[dest]
    # Set status variables
    if curr != dest:
        environ.botList[botNum].arrived = False
    else:
        environ.botList[botNum].arrived = True
    
    # Calcualte the shortest path from the current node to all others
    previous, shortestPath = path(environ.network, environ.network.nodes[curr])
    # Calculate the path from the current node to the destination. If you want the time taken return the length variable below
    path1, length = getResult(previous, shortestPath, environ.network.nodes[curr], environ.network.nodes[dest])
    # Add nodes needed to reach path to the robots path
    for i in path1:
        environ.botList[botNum].add(environ.network.nodes[i.label])


# Calculates current bot location
# Guesses node 0 if not at a node
def getCurrLocation(environ, botNum):
    for i in environ.network.nodes:
        if abs(environ.botList[botNum].xCord - i.x) < env.accuracy and abs(environ.botList[botNum].yCord - i.y) < env.accuracy:
            return i
    print("Help me Im lost")
    return environ.network.nodes[0]


# Run every time step in order to calculate how far and in what direction each robot moves 
def calcBotPos(environ):
    for i in environ.botList:
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
        if abs(xDist) > env.accuracy or abs(yDist) > env.accuracy: 
            speeds = calcSpeed(xDist, yDist, i.maxSpeed, i.minSpeed, env.RFID_Dist2Node)
            i.xCord += speeds[0]*environ.timeStep
            i.yCord += speeds[1]*environ.timeStep
        else:
            del(i.path[0]) 
            if i.path == []:
                i.arrived = True


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
    stop = {0: [23, 21, 1], 1: [21, 23, 1]}
    
    env = environment(file, bList, g, stop)
    env.updateBotMarker() 
    env.drawPaths()
    env.drawNodes()
    print("*******************")
    print("Network Initialized")
    print("*******************")
    
    # Nice little printy guys
    # for i in env.botList:
    #     print(i.botIndex)
    # for i in env.network.edges:
    #     print(i.label, ": (", i.n1.x, ", ", i.n1.y, "), (", i.n2.x, ", ", i.n2.y, ")")

    try:
        tS = time.monotonic_ns()
        while True:
            if time.monotonic_ns() - tS > 1000000 * env.timeStep:
                env.updateBotMarker()                   # Update map
                cv.imshow("Map", env.UIwBots)           # Show map
                cv.waitKey(int(env.timeStep*1000))      # Hold frame for one timestep
                calcBotPos(env)                         # Update each bots location
                tS = time.monotonic_ns()                # Wait till the next frame is ready. 
            
            # Once the bots reach their destination send them back to the origin
            for i in env.botList:
                if i.path == [] and len(env.stops[i]) != 1:
                    del(env.stops[i][0])
                    # Find where they are and calculate shortest route back to origin
                    t = getCurrLocation(env, i.botIndex)
                    runDijkstras(env, [i.botIndex, [t.label, env.stops[i][0]]])

    except KeyboardInterrupt: # If you want to stop the program press crtl + c
        # cv.imshow("Map", env.UIwBots)
        # cv.waitKey()
        print("Aww, you stopped it. Whats wrong with you?")

    