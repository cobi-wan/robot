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


# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/UI')
# def UI():
#     return Response(updateMap(env), mimetype='multipart/x-mixed-replace;boundary=frame')

# @app.route('/api/v1/summon')
# def summon():
#     wc = request.args.get("wc")
#     env.addStop(int(wc))
#     return Response("{'a':'b'}", status=200, mimetype='application/json')


# def updateMap(environ):
#     size = 200
#     send_update("Arrived", environ.destination_list[environ.botList[0]][0], mqtt)
#     try: 
#         ts = time.monotonic_ns()
#         videoFeed = cv.VideoCapture(0)
#         while True:
#             if time.monotonic_ns() >= ts + environ.timeStep:
#                 ts = time.monotonic_ns()
#                 mapping(environ)

#                 # Capture frame from robot live feed

#                 # ret, liveFeedFrame = videoFeed.read()
                
#                 # Capture fram from user interface and resize

#                 UIFrame = environ.UIwBots
#                 # liveFeedFrame = cv.resize(UIFrame, (100,100))

#                 # Convert to grayscale and create mask

#                 # img2gray = cv.cvtColor(liveFeedFrame, cv.COLOR_BGR2GRAY)
#                 # ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)

#                 # I genuinely have no clue

#                 # roi = UIFrame[-size-325:-325, -size-550:-550]
#                 # roi[np.where(mask)] = 0

#                 # Image encoding and bitstream
#                 _, img_encoded = cv.imencode('.jpg', UIFrame)
#                 UIFrame = img_encoded.tobytes()
#                 yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + UIFrame + b'\r\n')
#     except KeyboardInterrupt:
#         print("Ok i guess you didnt like runnning my code. Whatever. Im not upset")


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


    # p = Process(target=updateMap, args=(env, ))
    # p.start()
    app = create_app(env, app)
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    # p.join()
