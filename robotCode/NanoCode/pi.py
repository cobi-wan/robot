import numpy as np
import cv2 as cv
import time
import serial
from pyzbar.pyzbar import decode

def motorEncode(direction=int, speed=int):
    concat = f'{direction},{speed}'
    bstring = concat.encode()
    return bstring

forwardStr = motorEncode(3,20)
leftStr = motorEncode(2,20)
rightStr = motorEncode(1,20)

# ser = serial.Serial('/dev/serial0', 115200, write_timeout=0)
flip = 0
dispW = 340
dispH = 240
camSet='nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

vid = cv.VideoCapture(camSet)

ser = serial.Serial(port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE)

time.sleep(1)

FRAME_WIDTH_PROPERTY = 3
FRAME_WIDTH = vid.get(cv.CAP_PROP_FRAME_WIDTH)

FRAME_HEIGHT_PROPERTY = 4
FRAME_HEIGHT = vid.get(cv.CAP_PROP_FRAME_HEIGHT)

vid.set(FRAME_WIDTH_PROPERTY, FRAME_WIDTH)
vid.set(FRAME_HEIGHT_PROPERTY,FRAME_HEIGHT)

while(True):
    ret, frame = vid.read()

    for barcode in decode(frame):
        myData = barcode.data.decode('utf-8')
        print(myData)
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv.polylines(frame, [pts], True, (255,0,255), 5)
        pts2 = barcode.rect
        cv.putText(frame, myData, (pts2[0],pts2[1]),cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,255),2)

    crop_img = frame
    gray = cv.cvtColor(crop_img,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0)
    ret, thresh = cv.threshold(blur,60,255,cv.THRESH_BINARY_INV)

    contours, hierarchy = cv.findContours(thresh.copy(),1,cv.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv.contourArea)
        M = cv.moments(c)

        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

        else:
            cx,cy = 0,0

        cv.line(crop_img, (cx,0), (cx,720), (255,0,0), 1)
        cv.line(crop_img, (0,cy), (720,cy), (255,0,0), 1)

        cv.drawContours(crop_img, contours, -1, (0,255,0), 1)

        if cx >= 120:
            print('left, turn right')
            #ser.write(rightStr)

        if cx < 120 and cx > 50:
            print('on track')
            #ser.write(forwardStr)

        if cx <= 50:
            print('right, turn left')
            #ser.write(leftStr)
        ser.write(str(cx).encode())

    else:
        print('no line')

    cv.imshow('frame', crop_img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break