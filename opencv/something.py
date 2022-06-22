#import the required libraries including OpenCV
import cv2
#image processing utility functions
#install by running - pip install imutils
import imutils
#Grab the images you want to compare.
original = cv2.imread("image1.jpg")
new = cv2.imread("image2.jpg")
#resize the images to make them smaller. Bigger image may take a significantly
#more computing power and time
original = imutils.resize(original, height = 600)
new = imutils.resize(new, height = 600)
#make a copy of original image so that we can store the
#difference of 2 images in the same
diff = original.copy()
cv2.absdiff(original, new, diff)
#converting the difference into grascale
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
 
#increasing the size of differences so we can capture them all
for i in range(0, 3):
    dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)
#threshold the gray image to binarise it. Anything pixel that has
#value more than 3 we are converting to white
#(remember 0 is black and 255 is absolute white)
#the image is called binarised as any value less than 3 will be 0 and
# all values equal to and more than 3 will be 255
(T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
 
# now we need to find contours in the binarised image
cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
for c in cnts:
    # fit a bounding box to the contour
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
#uncomment below 2 lines if you want to
#view the image press any key to continue
#write the identified changes to disk
cv2.imwrite("changes.png", new)
cv2.imshow("changes.png", new)