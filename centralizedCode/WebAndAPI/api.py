from flask import Flask, render_template, request, Response, Blueprint
import time
import cv2 as cv
from PathPlanning.pathPlanning import mapping
from WebAndAPI.request import Request

app = Flask(__name__)


# App instantiation function. Allows us to add the environ and client to the apps 
# configuration variables to be used later
def create_app(environ, ap, client):
    ap.config['Environ'] = environ
    ap.config['Client'] = client 
    return ap


# Main UI template. Currently includes a button that links to the create request form
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


# Form with drop down menus that allows the user to choose a workstation to connect out of the stations list
# Change to allow stations to be any valid stations in the environment 
@app.route('/createRequest', methods=['GET', 'POST'])
def createRequest():
    stations = app.config['Environ'].reachableWorkstations
    
    return render_template("requestForm.html", stations=stations)


# Result from the create request form. Should show UI and have a button that allows user to "Continue" 
# when bot arrives
@app.route('/api/v1/submitRequest', methods=['GET', 'POST'])
def result():
    pickupReq = None
    dropoffReq = None
    if request.method == 'POST':
        pickupWS = int(request.form.get("pickupStation"))
        dropoffWS = int(request.form.get("dropoffStation"))
        (pickupReq, dropoffReq) = app.config['Environ'].createRequest(pickupWS, dropoffWS)
    # return jsonify(msg) # When changing to paperless integration return a submittal message
    if pickupReq is None:
        arrived = False
        print("Here")
    else: 
        arrived = pickupReq.active
    return render_template('requestResult.html')

@app.route('/api/v1/sendFromPickupToDestination', methods=['GET', 'POST'])
def sendFromPickupToDestination():
    return {'A','b'}


# URL with UI shown in a box
@app.route('/UI', methods=['GET','POST'])
def UI():
    return Response(updateMap(app.config['Environ'], app.config['Client']), mimetype='multipart/x-mixed-replace;boundary=frame')


# Old api method that allowed user to add a stop. 
@app.route('/api/v1/summonBot')
def summonBot():
    query_parameters = request.args
    workCenter = query_parameters.get("wc")
    if app.config['Environ'].activeRequests[workCenter] == False:
        app.config['Environ'].activeRequests[workCenter] = True
        newReq = Request()
        workCenterRequests
        newReq.requestingStation = workCenter
    newReq.ETA = 0
    app.config['Environ'].addStop(workCenter)
    # app.config['Environ'].addStop(wcDest)
    return Response("{'a':'b'}", status=200, mimetype='application/json')


@app.route('/api/v1/HandleRequest')
def handleRequest():
    pass

@app.route('/api/v1/BotInfo', methods=['GET'])
def requestUpdate():
    query_parameters = request.args
    requestID = query_parameters.get('requestID')
    pass
    
def updateMap(environ, mqtt):
    # size = 200
    # send_update("Arrived", environ.destination_list[environ.botList[0]][0], mqtt)
    try: 
        ts = time.monotonic_ns()
        while True:
            if time.monotonic_ns() >= ts + environ.timeStep:
                ts = time.monotonic_ns()
                mapping(environ)
                
                UIFrame = environ.UIwBots
                _, img_encoded = cv.imencode('.jpg', UIFrame)
                UIFrame = img_encoded.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + UIFrame + b'\r\n')
    except KeyboardInterrupt:
        print("Ok i guess you didnt like runnning my code. Whatever. Im not upset")




        # Capture frame from robot live feed

                # ret, liveFeedFrame = videoFeed.read()
                
                # Capture fram from user interface and resize

                
                # liveFeedFrame = cv.resize(UIFrame, (100,100))

                # Convert to grayscale and create mask

                # img2gray = cv.cvtColor(liveFeedFrame, cv.COLOR_BGR2GRAY)
                # ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)

                # I genuinely have no clue

                # roi = UIFrame[-size-325:-325, -size-550:-550]
                # roi[np.where(mask)] = 0

                # Image encoding and bitstream