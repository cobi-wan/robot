from flask import Flask, render_template, request, Response, Blueprint
import time
import cv2 as cv
from PathPlanning.pathPlanning import mapping
from WebAndAPI.request import Request

app = Flask(__name__)

def create_app(environ, ap, client):
    ap.config['Environ'] = environ
    ap.config['Client'] = client 
    return ap

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form.get('summon to node1') == 'node1':
            (bNum, node) = app.config['Environ'].addStop(9998)
        elif request.form.get('summon to node2') == 'node2':
            (bNum, node) = app.config['Environ'].addStop(9999)
            # for bot in app.config['Environ'].botList:
            #     if bot.activated:
            #         app.config['Client'].publish(str(bot.MAC)+":Halt",payload="Continue",qos=1)
    return render_template('index.html')

@app.route('/UI', methods=['GET','POST'])
def UI():
    return Response(updateMap(app.config['Environ'], app.config['Client']), mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/api/v1/summonBot')
def summonBot():
    query_parameters = request.args
    workCenter = query_parameters.get("wc")
    if app.config['Environ'].activeRequests[workCenter] == False:
        app.config['Environ'].activeRequests[workCenter] = True
        newReq = Request()
        newReq.requestingStation = workCenter
    newReq.ETA = 0
    app.config['Environ'].addStop(workCenter)
    # app.config['Environ'].addStop(wcDest)
    return Response("{'a':'b'}", status=200, mimetype='application/json')

@app.route('/api/v1/sendBot', methods=['GET'])
def sendBot():
    workStations = ['Quality Lab', 'Deburring', 'Shipping']
    return render_template('index.html', workStations=workStations)

@app.route('api/v1/HandleRequest')
def handleRequest():
    pass

@app.route('/api/v1/BotInfo', methods=['GET'])
def requestUpdate():
    query_parameters = request.args
    requestID = query_parameters.get('requestID')
    pass
    
def updateMap(environ, mqtt):
    size = 200
    # send_update("Arrived", environ.destination_list[environ.botList[0]][0], mqtt)
    try: 
        ts = time.monotonic_ns()
        while True:
            if time.monotonic_ns() >= ts + environ.timeStep:
                ts = time.monotonic_ns()
                mapping(environ, mqtt)
                # for i in environ.botList:
                #     if i.activated:
                #         pass
                        # print("Bot: " + str(i.botIndex) + " Destination List: " + ", ".join(str(k) for k in environ.destination_list[i]) + " Path: " + ", ".join(str(j.label) for j in i.path) )

                # Capture frame from robot live feed

                # ret, liveFeedFrame = videoFeed.read()
                
                # Capture fram from user interface and resize

                UIFrame = environ.UIwBots
                # liveFeedFrame = cv.resize(UIFrame, (100,100))

                # Convert to grayscale and create mask

                # img2gray = cv.cvtColor(liveFeedFrame, cv.COLOR_BGR2GRAY)
                # ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)

                # I genuinely have no clue

                # roi = UIFrame[-size-325:-325, -size-550:-550]
                # roi[np.where(mask)] = 0

                # Image encoding and bitstream
                _, img_encoded = cv.imencode('.jpg', UIFrame)
                UIFrame = img_encoded.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + UIFrame + b'\r\n')
    except KeyboardInterrupt:
        print("Ok i guess you didnt like runnning my code. Whatever. Im not upset")