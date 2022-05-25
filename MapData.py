from turtle import update
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

    b1 = partRunner(nodes[0].x, nodes[0].y, 0)
    b2 = partRunner(nodes[0].x, nodes[0].y, np.pi/2)
    bList = np.array([b1, b2])

    return bList, g

def updateRobPrediction(botNum, Env):
    while Env.botList[botNum].path != []:
        while Env.botList[botNum].xCord != Env.botList[botNum].path[0].x and Env.botList[botNum].yCord != Env.botList[botNum].path[0].y:
            if Env.botList[botNum].xCord - Env.botList[botNum].path[0].x > 0:
                Env.botList[botNum].tCord = np.arcsin((Env.botList[botNum].yCord - Env.botList[botNum].path[0].y)/(Env.botList[botNum].xCord - Env.botList[botNum].path[0].x)) - np.pi/2
            xSpd = np.sin(Env.botList[botNum].tCord)*Env.botList[botNum].maxSpeed
            ySpd = np.cos(Env.botList[botNum].tCord)*Env.botList[botNum].maxSpeed
            Env.botList[botNum].xCord += xSpd/env.timeStep
            Env.botList[botNum].yCord += ySpd/env.timeStep
            print(xSpd, ySpd)
        del(Env.botList[botNum].path[0])

if __name__ == '__main__':
    cv.destroyAllWindows()
    bList, g = startUp()
    env = environment("ImageFiles\BlankMap.png", bList, g)
    env.updateBotPos() 
    env.drawPaths()
    env.drawNodes()
    env.botList[0].add(env.network.nodes[0])
    env.botList[0].add(env.network.nodes[1])
    env.botList[0].add(env.network.nodes[3])
    # for i in env.botList:
    #     print(i.botIndex)
    # for i in env.network.edges:
    #     print(i.label, ": (", i.n1.x, ", ", i.n1.y, "), (", i.n2.x, ", ", i.n2.y, ")")
    try:
        while True:
            env.botList[0].xCord += 10
            env.botList[1].yCord += 10
            # updateRobPrediction(0, env)
            env.updateBotPos()
            cv.imshow("Map", env.UIwBots)
            cv.waitKey(int(env.timeStep*1000))
    except KeyboardInterrupt: # If you want to stop the program press crtl + c
        cv.destroyAllWindows
        print("Aww, you stopped it. Whats wrong with you?")

    