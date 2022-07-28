from flask import Flask, render_template, request, Response, Blueprint
import time
import cv2 as cv
from PathPlanning.pathPlanning import mapping

app = Flask(__name__)

def create_app(environ, ap):
    ap.config['Environ'] = environ 
    return ap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/UI')
def UI():
    return Response(updateMap(app.config['Environ']), mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/api/v1/summon')
def summon():
    wc = request.args.get("wc")
    return Response("{'a':'b'}", status=200, mimetype='application/json')


def updateMap(environ):
    size = 200
    # send_update("Arrived", environ.destination_list[environ.botList[0]][0], mqtt)
    try: 
        ts = time.monotonic_ns()
        videoFeed = cv.VideoCapture(0)
        while True:
            if time.monotonic_ns() >= ts + environ.timeStep:
                ts = time.monotonic_ns()
                mapping(environ)

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