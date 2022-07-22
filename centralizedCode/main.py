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
from Classes import button
from pathPlanning import mapping
from communication import connect
from communication import send_update

from flask import Flask, render_template, request, Response
from multiprocessing import Process

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/UI')
def UI():
    return Response(updateMap(env), mimetype='multipart/x-mixed-replace;boundary=frame')

def getFrames(environ):
    ts = time.monotonic_ns()
    while True:
        if time.monotonic_ns() >= ts + environ.timestep:
            ts = time.monotonic_ns()
            img = environ.UIwBots
            _, img_encoded = cv.imencode('.jpg', img)
            frame = img_encoded.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def updateMap(environ):
    size = 200
    send_update("Arrived", environ.destination_list[environ.botList[0]][0], mqtt)
    try: 
        ts = time.monotonic_ns()
        videoFeed = cv.VideoCapture(0)
        while True:
            if time.monotonic_ns() >= ts + environ.timeStep:
                ts = time.monotonic_ns()
                mapping(environ)

                # Capture frame from robot live feed

                ret, liveFeedFrame = videoFeed.read()
                
                # Capture fram from user interface and resize

                UIFrame = environ.UIwBots
                liveFeedFrame = cv.resize(UIFrame, (100,100))

                # Convert to grayscale and create mask

                img2gray = cv.cvtColor(liveFeedFrame, cv.COLOR_BGR2GRAY)
                ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)

                # I genuinely have no clue

                roi = UIFrame[-size-325:-325, -size-550:-550]
                roi[np.where(mask)] = 0

                # Image encoding and bitstream
                _, img_encoded = cv.imencode('.jpg', UIFrame)
                UIFrame = img_encoded.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + UIFrame + b'\r\n')
    except KeyboardInterrupt:
        print("Ok i guess you didnt like runnning my code. Whatever. Im not upset")

# Reads in mapping file that specifies node locations and paths
def startUp():

    print("*******************")
    print("System Initialization:")
    print("*******************")
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
            nodes.append(node(int(row[1]), int(row[2]), row[3]))
            for i in row[4:]:
                if i != '':
                    edges.append(edge(nodes[int(i)], nodes[int(row[0])]))

    g = graph(nodes, edges)

    botFile = "botBooting.csv"
    botList = []
    buttonList = []

    with open(botFile, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        for row in csvreader:
            if int(row[0]) == 1:
                print("Bot at MAC:", str(row[5]), "at:", str(row[2]), ", ", str(row[3]))
                botList.append(partRunner(int(row[1]), int(row[2]), int(row[3]), int(row[4]), str(row[5]).encode()))
            else:
                print("Button at MAC:", row[5])
                buttonList.append(button(int(row[1]), int(row[3]), str(row[2].encode())))
    valid = input("Hit enter if the above information looks correct. Enter 0 to exit and edit conf files: ")
    if valid != "":
        exit()

    return botList, g, buttonList

if __name__ == "__main__":

    # Initial running stuff
    cv.destroyAllWindows()

    # Run startup procedure to read in nodes and create network 
    bList, g, buttonList= startUp()

    # Load in blank image in given folder. Allow for Windows and Mac OS
    if platform.system() == 'Windows':
        file = "ImageFiles\BlankMap.png"
    else: 
        file = "ImageFiles/BlankMap.png"
    
    # Create environment and draw items given in setup
    destinations = [2, 3, 4, 5, 6, 21, 20, 23, 1]
    # destinations = {0: [23, 1, 5, 10]}
    # stop = None
    env = environment(file, bList, g, buttonList, destinations)
    env.updateBotMarker() 
    env.drawPaths()
    env.drawNodes()
    print("*******************")
    print("Network Initialized")
    print("*******************")
    mqtt = connect(env)
    mqtt.loop_start()
    ts = time.monotonic_ns()

    # for i in env.network.nodes:
    #     print(i.tag)


    p = Process(target=updateMap, args=(env, ))
    p.start()
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    p.join()