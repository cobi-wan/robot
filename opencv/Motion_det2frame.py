# Python program to implement
# Webcam Motion Detector

# importing OpenCV, time and Pandas library
import cv2, time, pandas
# importing datetime class from datetime library
from datetime import datetime
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input',nargs='+',
                    help='Input vedio file') 
parser.add_argument('-o','-U','--output', default = "combine_result",
                    help='Output vedio file, default as "combine_result"')     
parser.add_argument('-f','-F','--FPS', type = int,
                    help='Start from X second. default is the same as the first video')     
parser.add_argument('-w','-W','--window', nargs='?',
                    help='1920x1080 default is the combined size of two vedio')     

args = parser.parse_args()
File = args.input
OUTPUT = args.output
Window = args.window
fps = args.FPS

# Read logo and resize
logo = cv2.imread('Map.png')
#Ssize = 100
#logo = cv2.resize(logo, (size, size))

# Create a mask of logo
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
check, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

# function for combined two frames.
def Fram_connect(frame0, frame2, Video_w, Video_h,  Video_w2, Video_h2):
  frame2 = cv2.resize(frame2, (int(Video_w2), int(Video_h)), interpolation = cv2.INTER_AREA)
  BG = cv2.resize(frame0, (int(Video_w + Video_w2), int(Video_h)), interpolation = cv2.INTER_AREA)
  BG[0:int(Video_h),0:int(Video_w)] = frame0
  BG[0:int(Video_h),int(Video_w):int(Video_w+ Video_w2)] = frame2
  return (BG)

# Assigning our static_back to None
static_back = None
static_back2 = None
# List when any moving object appear
motion_list = [ None, None ]
motion_list2 = [ None, None ]
# Time of movement
time = []
time2 = []
# Initializing DataFrame, one column is start
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])   

# Capturing video
video = cv2.VideoCapture(0)
video2 = cv2.VideoCapture(1)

# The video 1 set the video 1 as the default size and fps

fps_c = video.get(cv2.CAP_PROP_FPS)
Video_h =video.get(cv2.CAP_PROP_FRAME_HEIGHT)
Video_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)

fps_c2 = video2.get(cv2.CAP_PROP_FPS)
Video_h2 = video2.get(cv2.CAP_PROP_FRAME_HEIGHT)
Video_w2 = video2.get(cv2.CAP_PROP_FRAME_WIDTH)

# args for the video output
fps = fps_c

if Window == None:
  size = (int(Video_w+Video_w2), int(Video_h))
else:
    size = (int(Window.split("x")[0]), int(Window.split("x")[1]))

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
videowriter = cv2.VideoWriter(OUTPUT + ".avi",fourcc,fps,size)

# Infinite while loop to treat stack of image as video
while True:
	# Reading frame(image) from video
	check, frame = video.read()
	# Region of Image (ROI), where we want to insert logo
	roi = frame[10:100, 10:100]
	# Set an index of where the mask is
	roi[np.where(mask)] = 0
	roi += logo

	check2, frame2 = video2.read()

	# Initializing motion = 0(no motion)
	motion = 0
	motion2 = 0

	# Converting color image to gray_scale image
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

	# Converting gray scale image to GaussianBlur
	# so that change can be find easily
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

	# In first iteration we assign the value
 	# of static_back to our first frame
	if static_back is None:
		static_back = gray
		continue
	
	if static_back2 is None:
		static_back2 = gray2
		continue
	# Difference between static background
	# and current frame(which is GaussianBlur)
	diff_frame = cv2.absdiff(static_back, gray)
	diff_frame2 = cv2.absdiff(static_back2, gray2)
	# If change in between static background and
	# current frame is greater than 30 it will show white color(255)
	thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

	thresh_frame2 = cv2.threshold(diff_frame2, 30, 255, cv2.THRESH_BINARY)[1]
	thresh_frame2 = cv2.dilate(thresh_frame2, None, iterations = 2)

	# Finding contour of moving object
	cnts,_ = cv2.findContours(thresh_frame.copy(),
					cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for contour in cnts:
		if cv2.contourArea(contour) < 10000:
			continue
		motion = 1
		(x, y, w, h) = cv2.boundingRect(contour)
		#if cv2.contourArea(contour)>700 and (x <= 840) and (y >= 150 and y <=350) and cv2.contourArea(contour) < 10000: 
	
		
		# making green rectangle around the moving object
		
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

		continue

	cnts2,_ = cv2.findContours(thresh_frame2.copy(),
					cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for contour2 in cnts2:
		if cv2.contourArea(contour2) < 10000:
			continue
		motion2 = 1
		(x2, y2, w2, h2) = cv2.boundingRect(contour2)
		#if cv2.contourArea(contour)>700 and (x <= 840) and (y >= 150 and y <=350) and cv2.contourArea(contour) < 10000: 
		# making green rectangle around the moving object
		cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 3)
		continue

	# Appending status of motion
	motion_list.append(motion)

	motion_list = motion_list[-2:]

	# Appending Start time of motion
	if motion_list[-1] == 1 and motion_list[-2] == 0:
		time.append(datetime.now())

	# Appending End time of motion
	if motion_list[-1] == 0 and motion_list[-2] == 1:
		time.append(datetime.now())
	

	cv2.imshow("Color Frame", frame)


	# Appending status of motion
	motion_list2.append(motion2)

	motion_list2 = motion_list2[-2:]

	# Appending Start time of motion
	if motion_list2[-1] == 1 and motion_list2[-2] == 0:
		time2.append(datetime.now())

	# Appending End time of motion
	if motion_list2[-1] == 0 and motion_list2[-2] == 1:
		time2.append(datetime.now())

	img = Fram_connect(frame, frame2, Video_w, Video_h,  Video_w2, Video_h2)
	img_1 = cv2.resize(img, size, interpolation = cv2.INTER_AREA)
	videowriter.write(img_1)
	cv2.imshow('comb',img_1)

	key = cv2.waitKey(1)
	# if q entered whole process will stop
	if key == ord('q'):
		# if something is movingthen it append the end time of movement
		if motion == 1:
			time.append(datetime.now())
		if motion2 == 1:
			time2.append(datetime.now())
		break


video.release()
video2.release()
# Destroying all the windows
cv2.destroyAllWindows()