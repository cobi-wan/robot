from urllib import response
import cv2 as cv
import time
from cv2 import imencode
import numpy as np
import sys       

# Runs Dijsktras from n1 to all other nodes on the network g
def getShortestPaths(g, n1):
    unvisited = g.nodes.copy() # Set all nodes to unvisited
    shortestPath = {}
    previousNodes = {}
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
                previousNodes[i[0]] = currentMin
        unvisited.remove(currentMin)
    return previousNodes, shortestPath


# Evaluate the result of Dijkstras and return the node ordered path
def getResult(previous, shortest, start, target, env):
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
    previousNodes, shortestPaths = getShortestPaths(environ.network, environ.network.nodes[curr])

    # Calculate the path from the current node to the destination. If you want the time taken return the length variable below
    path = []
    if len(previousNodes) != len(env.network.nodes) - 2:
        raise Exception("Invalid path length")
    currentNode = environ.network.nodes[dest]
    while currentNode != environ.network.nodes[curr]:
        path.append(currentNode)
        currentNode = previousNodes[currentNode]
    path.append(environ.network.nodes[curr])
    # return reversed(path), shortest[target]
    # , length = getResult(previous, shortestPaths, environ.network.nodes[curr], environ.network.nodes[dest], environ)

    # Add nodes needed to reach path to the robots path
    for i in reversed(path):
        environ.botList[botNum].add(environ.network.nodes[i.label])
    return shortestPaths(environ.network.nodes[dest])


# Calculates current bot location
# Guesses node 0 if not at a node
def getCurrLocation(environ, botNum):
    for i in environ.network.nodes:
        if abs(environ.botList[botNum].xCord - i.x) < environ.accuracy and abs(environ.botList[botNum].yCord - i.y) < environ.accuracy:
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
        if abs(xDist) > environ.accuracy or abs(yDist) > environ.accuracy: 
            speeds = calcSpeed(xDist, yDist, i.maxSpeed, i.minSpeed, environ.RFID_Dist2Node)
            i.xCord += speeds[0]*environ.timeStep
            i.yCord += speeds[1]*environ.timeStep
        else:
            del(i.path[0]) 
            if i.path == []:
                i.arrived = True

# Calculate the speed the robot should be moving
def calcSpeed(xDist, yDist, max, min, RFID_Dist):
        dist = np.sqrt(xDist**2 + yDist**2)
        xComp = xDist/dist
        yComp = yDist/dist
        if dist > RFID_Dist:
            return [xComp*max, yComp*max]
        else: 
            return [xComp*min, yComp*min]

def mapping(environ):
 
    environ.updateBotMarker()                   # Update map
    # cv.imshow("Map", environ.UIwBots)           # Show map
    cv.waitKey(int(environ.timeStep*1000))      # Hold frame for one timestep
    calcBotPos(environ)                         # Update each bots location

    for i in environ.botList:
        if i.path == [] and len(environ.destination_list[i]) != 1:

            #send_update("Arrived", environ.destination_list[i][0], client)
            del(environ.destination_list[i][0])
            # Find where they are and calculate shortest route back to origin
            currNode = getCurrLocation(environ, i.botIndex)
            runDijkstras(environ, [i.botIndex, [currNode.label, environ.destination_list[i][0]]])

    return environ