from cProfile import run
from logging import exception
from re import M
from turtle import update
import cv2 as cv
from cv2 import MARKER_SQUARE
import time
import numpy as np
import platform
import csv
from Classes import partRunner
from Classes import cart
from Classes import environment
from Classes import edge
from Classes import node
from Classes import graph
from pathPlanning import mapping
from communication import connect


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

if __name__ == "__main__":

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
    ts = time.monotonic_ns()
    mqtt = connect(env)
    mqtt.loop_start()

    try: 
        while True:
            # mqtt.publish("Test", payload="AAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHH")
            # time.sleep(2)
            pass
            # if time.monotonic_ns() >= ts + env.timeStep:
            #     mapping(env)
    except KeyboardInterrupt:
        print("Ok i guess you didnt like runnning my code. Whatever. Im not upset")

    