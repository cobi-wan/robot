from time import sleep
import cv2 as cv
import numpy as np

# Objects
feed = cv.VideoCapture(0)
qrCodeDetector = cv.QRCodeDetector()

# Variables
points = None

# Image processing
while True:
    # Read frame by frame from webcam
    check, frame = feed.read()
    cv.imshow('QR Detection', frame)
    
    key = cv.waitKey(20)

    if key == ord('q'):
        break

    decodedText, points, _ = qrCodeDetector.detectAndDecode(frame)

    # Check if QR is in frame
    if decodedText:
        print('QR Detected...')
        print(decodedText)
        break

    else:
        print('QR Not Detected')

feed.release()
cv.destroyAllWindows