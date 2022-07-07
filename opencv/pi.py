import numpy as np
import cv2 as cv
import serial

def motorEncode(direction=int, speed=int):
    concat = f'{direction},{speed}'
    bstring = concat.encode()
    return bstring

forwardStr = motorEncode(3,20)
leftStr = motorEncode(2,20)
rightStr = motorEncode(1,20)

# ser = serial.Serial('/dev/serial0', 115200, write_timeout=0)

vid = cv.VideoCapture(0)
vid.set(3,160)
vid.set(4,120)

while(True):
    ret, frame = vid.read()
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

        if 50 < cx < 120:
            print('on track')
            #ser.write(forwardStr)

        if cx <= 50:
            print('right, turn left')
            #ser.write(leftStr)

    else:
        print('no line')

    cv.imshow('frame', crop_img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break