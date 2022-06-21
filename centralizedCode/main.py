from cProfile import run
from concurrent.futures import process
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
from flask import Flask, render_template, request, Response
from multiprocessing import Process

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/UI')
def UI():
    return Response(updateMap(env), mimetype='multipart/x-mixed-replace;boundary=frame')

def updateMap(environ, client):
        try: 
            ts = time.monotonic_ns()
            while True:
                if time.monotonic_ns() >= ts + environ.timeStep:
                    ts = time.monotonic_ns()
                    mapping(environ, client)
                    img = environ.UIwBots
                    _, img_encoded = cv.imencode('.jpg', img)
                    frame = img_encoded.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except KeyboardInterrupt:
            print("Ok i guess you didnt like runnning my code. Whatever. Im not upset")

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
    # b2 = partRunner(nodes[1].x, nodes[1].y, np.pi/2)
    # b3 = partRunner(nodes[1].x, nodes[1].y, np.pi)
    bList = np.array([b1])

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
    destinations = [2, 1]
    # destinations = {0: [23, 1, 5, 10]}
    # stop = None
    env = environment(file, bList, g, destinations)
    env.updateBotMarker() 
    env.drawPaths()
    env.drawNodes()
    print("*******************")
    print("Network Initialized")
    print("*******************")
    mqtt = connect(env)
    mqtt.loop_start()
    ts = time.monotonic_ns()

    arg_1 = (env, mqtt)
    p = Process(target=updateMap, args=(env, mqtt, ))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
    
