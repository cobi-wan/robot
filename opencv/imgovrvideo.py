import cv2
import numpy as np

# Setup camera
liveFeed = cv2.VideoCapture(0)

# Read UI and resize
UI = cv2.imread('Map.png')
size = 100
UI = cv2.resize(UI, (size, size))

# Create a mask of UI
img2gray = cv2.cvtColor(UI, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

while True:
	ret, frame = liveFeed.read()

	# Region of Image (ROI), where we want to insert UI
	roi = frame[-size-100:-100, -size-100:-100]

	# Set an index of where the mask is
	roi[np.where(mask)] = 0
	roi += UI

	cv2.imshow('WebCam', frame)
	if cv2.waitKey(1) == ord('q'):
		break

liveFeed.release()
cv2.destroyAllWindows()