# importing the libraries
import cv2
import numpy as np

# Setup camera
cap = cv2.VideoCapture(1)

# Read logo and resize
logo = cv2.imread('Map.png')
size = 100
logo = cv2.resize(logo, (size, size))

# Create a mask of logo
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

while True:
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Region of Image (ROI), where we want to insert logo
	roi = frame[-size-100:-100, -size-100:-100]

	# Set an index of where the mask is
	roi[np.where(mask)] = 0
	roi += logo

	cv2.imshow('WebCam', frame)
	if cv2.waitKey(1) == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()