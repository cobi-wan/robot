import numpy as np
import cv2 as cv
import time
from pyzbar.pyzbar import decode 
from config import display_videofeed, display_barcode_bounding_box, display_contour_bounds, display_crosshair, video_multiplier

def camera_initialization():
    flip = 0
    dispW = 340*video_multiplier
    dispH = 240*video_multiplier

    # Play with this line to test framerates and resolutions. 
    # Check to see if width, height and dispW, dispH affect actual resolution. 
    # Test framerate with display and without display to see if video encoding for preview reduces framerate (likely)
    camSet = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    video_stream = cv.VideoCapture(camSet)

    time.sleep(0.5)

    FRAME_WIDTH_PROPERTY = 3
    FRAME_WIDTH = video_stream.get(cv.CAP_PROP_FRAME_WIDTH)

    FRAME_HEIGHT_PROPERTY = 4
    FRAME_HEIGHT = video_stream.get(cv.CAP_PROP_FRAME_HEIGHT)

    video_stream.set(FRAME_WIDTH_PROPERTY, FRAME_WIDTH)
    video_stream.set(FRAME_HEIGHT_PROPERTY, FRAME_HEIGHT) 

    return video_stream, video_multiplier, FRAME_WIDTH

# Call continuously. Processes video feed and returns the location of the line (cx, cy)
def process_frame(video_stream):
    ret, frame = video_stream.read()

    for barcode in decode(frame):
        value = barcode.data.decode('utf-8')
        print("Barcode reading:"+str(value))
        if display_barcode_bounding_box:
            points = np.array([barcode.polygon], np.int32)
            points = points.reshape((-1, 1, 2))
            cv.polylines(frame, points, True, (255, 0, 255), 5)
            points = barcode.rect
            cv.putText(frame, value, (points[0], points[1]), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

    cropped_image = frame
    gray = cv.cvtColor(cropped_image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    ret, threshold = cv.threshold(blur, 60, 255, cv.THRESH_BINARY_INV)

    contours, hierarchy = cv.findContours(threshold.copy(), 1, cv.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        biggest_contour = max(contours, key=cv.contourArea)
        moment = cv.moments(biggest_contour)

        if moment['m00'] != 0:
            cx = int(moment['m10']/moment['m00'])
            cy = int(moment['m01']/moment['m00'])
        else: 
            cx, cy = 0, 0

        if display_crosshair:
            cv.line(cropped_image, (cx, 0), (cx, 720), (255, 0, 0), 1)
            cv.line(cropped_image, (0, cy), (720, cy), (255, 0, 0), 1)

        if display_contour_bounds:
            cv.drawContours(cropped_image, contours, -1, (0, 255, 0), 1)
    else: 
        print("Line not found")
        cx, cy = None, None
        # Turn on line not found LED     

    if display_videofeed:
        cv.imshow('frame', cropped_image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            return None, None

    return cx, cy





