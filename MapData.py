import cv2 as cv
import time
import numpy as np

mapScale = 0.1 # 1 px = 1 mm
worldScale = 10
MAP = cv.imread("lib\Map.png") # Read in picture of the map. Will look into reading different files later
width = int(1152*worldScale*mapScale)
height = int(648*worldScale*mapScale)
dimensions = (width, height)
MAP = cv.resize(MAP, dimensions, interpolation = cv.INTER_LINEAR)

# Robot path points
p1 = (int(1), int(1))
p2 = (int(100), int(100))
p3 = (int(100), int(400))

# Initial Robot Position 
posRobx = 1000
posRoby = 1000
posRobt = 0


def robot2World(cords):
    x = posRobx + cords[0]*np.cos(posRobt) - cords[1]*np.sin(posRobt)
    y = posRoby + cords[0]*np.sin(posRobt) - cords[1]*np.cos(posRobt)

    return [x, y]

def robotTriangle():
    L = 14*2.54 * 5
    W = 11*2.54 * 5

    p1 = (-W/2, L/2)
    p2 = (W/2, L/2)
    p3 = (W/2, -L/2)
    p4 = (-W/2, -L/2)

    w1 = robot2World(p1)
    w2 = robot2World(p2)
    w3 = robot2World(p3)
    w4 = robot2World(p4)

    pts = np.array([(int(w1[0]*mapScale),height - int(w1[1]*mapScale)),(int(w2[0]*mapScale),height - int(w2[1]*mapScale)),(int(w3[0]*mapScale),height - int(w3[1]*mapScale)),(int(w4[0]*mapScale),height - int(w4[1]*mapScale))])
    #pts = np.array([int(w1[0]*mapScale, height - int(w1[1]*mapScale)), (int(w2[0]*mapScale), height - int(w2[1]*mapScale)), (int(w3[0]*mapScale), height - int(w3[1]*mapScale))])
    return pts

def updateMap():
    map = MAP.copy()
    pts = robotTriangle()
    cv.drawContours(map, [pts], 0, (255, 0, 0), 4)
    
    cv.imshow('Map', map)
    cv.waitKey(33)
    pass

def defineMap(paths):
    map = MAP.copy()                   
    cv.drawContours(map, [paths], 0, (255, 255, 255), 2)
    cv.imshow('Map', map)
    cv.waitKey(33)
    pass

if __name__ == '__main__':
    #defineMap([(p1, p2), (p2, p3)])
    pts = np.array([p1, p2, p3])
    # defineMap(pts)
    updateMap()
    print("Fuck1")
    time.sleep(1)
    try: 
        for i in range(100):
            updateMap()
            posRobx += 10
            posRoby += 10
    except KeyboardInterrupt:
        print("Darn")