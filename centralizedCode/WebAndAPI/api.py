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
    botList = app.config['Environ'].botList

    if request.method == 'POST':
        if request.form.get('summon bot') == 'summon':
            print("Button pressed")
            (bNum, node) = app.config['Environ'].addStop(1005)
            # print("Bot: ", bNum, "Going to stop: ", node)
            for bot in botList:
                if bot.activated:
                    app.config['Client'].publish("Bot:"+str(bot.MAC),payload="go",qos=1)
    return render_template('index.html')

@app.route('/UI', methods=['GET','POST'])
def UI():
    return Response(updateMap(app.config['Environ']), mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/api/v1/summonBot')
def summonBot():
    wc = request.args.get("wc")
    if app.config['Environ'].activeRequests[wc] == False:
        app.config['Environ'].activeRequests[wc] = True
        newReq = Request()
        newReq.requestingStation = wc
    newReq.ETA = 0
    app.config['Environ'].addStop(wc)
    # app.config['Environ'].addStop(wcDest)
    return Response("{'a':'b'}", status=200, mimetype='application/json')

@app.route('/api/v1/sendBot', methods=['GET'])
def sendBot():
    workStations = ['Quality Lab', 'Deburring', 'Shipping']
    return render_template('index.html', workStations=workStations)

def updateMap(environ):
    size = 200
    # send_update("Arrived", environ.destination_list[environ.botList[0]][0], mqtt)
    try: 
        ts = time.monotonic_ns()
        while True:
            if time.monotonic_ns() >= ts + environ.timeStep:
                ts = time.monotonic_ns()
                mapping(environ)
                for i in environ.botList:
                    if i.activated:
                        pass
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