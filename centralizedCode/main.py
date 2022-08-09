from cProfile import run
from concurrent.futures import process
from logging import exception
from re import M
import cv2 as cv
from cv2 import MARKER_SQUARE
import time
import numpy as np
import platform
import csv

from Classes.Graph.graph import graph
from Classes.Graph.node import node
from Classes.Graph.edge import edge
from Classes.environment import environment
from Classes.RobotClasses.partRunner import partRunner
from Classes.RobotClasses.cart import cart
from PathPlanning.pathPlanning import mapping
from WifiCommunication.communication import connect, send_update
from startUp import startUp
from WebAndAPI.api import app, create_app

from flask import Flask, render_template, request, Response
from multiprocessing import Process


def mainLoop(environ):
    ts = time.monotonic_ns()
    while True: 
        if time.monotonic_ns() >= ts + environ.timeStep:
            mapping(environ)
            for i in environ.botList:
                if i.activated:
                    print(i.path)

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

    env = environment(file, bList, g)
    env.updateBotMarker() 
    env.drawPaths()
    env.drawNodes()
    print("*******************")
    print("Network Initialized")
    print("*******************")
    mqtt = connect(env)
    mqtt.loop_start()
    
    app = create_app(env, app, mqtt)
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    

    