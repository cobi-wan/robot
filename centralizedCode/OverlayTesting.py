import cv2 as cv
import time
import numpy as np
import platform


if platform.system() == 'Windows':
    file = "ImageFiles\BlankMap.png"
else: 
    file = "ImageFiles/BlankMap.png"

img = cv.imread(file)

mapScale = 0.1 
worldScale = 5
width = int(2873*worldScale*mapScale)
height = int(1615*worldScale*mapScale)
dimensions = (width, height)
img = cv.resize(img, dimensions, interpolation = cv.INTER_LINEAR)
size = 200
timestep = 0.5

print("Loading")
videoFeed = cv.VideoCapture(0)
if videoFeed.isOpened():
    rval, frame = videoFeed.read()
    print("Good to go")
else:
    rval = False
    print("This aint workin out")

    
while rval:
    # if time.monotonic_ns() >= ts + timestep:
    ret, liveFeedFrame = videoFeed.read()
    liveFeedFrame = cv.resize(liveFeedFrame, (size, size), interpolation = cv.INTER_LINEAR)

    img2gray = cv.cvtColor(src=liveFeedFrame, code=cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)

    roi = img[-size-325:-325, -size-550:-550]
    # print(np.size(liveFeedFrame))
    # print(np.size(np.where(mask)))
    roi[np.where(mask)] = img2gray
    cv.imshow('Fuck', roi)
    key = cv.waitKey(20)
    if key == 27:
        break
    ts = time.monotonic_ns()

videoFeed.release()
cv.destroyAllWindows()

