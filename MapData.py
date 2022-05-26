from turtle import update
import cv2 as cv
from cv2 import MARKER_SQUARE
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

    b1 = partRunner(nodes[0].x, nodes[0].y, 0)
    b2 = partRunner(nodes[0].x, nodes[0].y, np.pi/2)
    b3 = partRunner(nodes[0].x, nodes[0].y, np.pi)
    bList = np.array([b1, b2, b3])

    return bList, g

if __name__ == '__main__':

    # Initial running stuff
    cv.destroyAllWindows()
    bList, g = startUp()
    env = environment("ImageFiles\BlankMap.png", bList, g)
    env.updateBotMarker() 
    env.drawPaths()
    env.drawNodes()
    
    # Temporary setup stuff. Delete Later 
    env.botList[0].add(env.network.nodes[1])
    env.botList[0].add(env.network.nodes[3])
    env.botList[1].add(env.network.nodes[10])
    
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
                        i.tCord = np.arcsin((i.yCord - i.path[0].y)/(i.xCord - i.path[0].x))
                    else:
                        if (i.yCord - i.path[0].y) > 0:
                            i.tCord = -np.pi/2
                        else:
                            i.tCord = np.pi/2
                    # print("Bot #:", i.botIndex, "is should be moving at an angle", i.tCord*180/np.pi)
                    # print("Its goal point is at (", i.path[0].x, ",", i.path[0].y, ")")
                    # if abs(i.xCord - i.path[0].x) > 5: 
                    #     i.xCord += i.maxSpeed / env.timeStep

                        
                tS = time.monotonic_ns()


    except KeyboardInterrupt: # If you want to stop the program press crtl + c
        cv.destroyAllWindows
        print("Aww, you stopped it. Whats wrong with you?")

    