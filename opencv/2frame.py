import numpy as np
import cv2
import Motion_det2frame

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
# function for combined two frames.
def Fram_connect(frame0, frame2, Video_w, Video_h,  Video_w2, Video_h2):
  frame2 = cv2.resize(frame2, (int(Video_w2), int(Video_h)), interpolation = cv2.INTER_AREA)
  BG = cv2.resize(frame0, (int(Video_w + Video_w2), int(Video_h)), interpolation = cv2.INTER_AREA)
  BG[0:int(Video_h),0:int(Video_w)] = frame0
  BG[0:int(Video_h),int(Video_w):int(Video_w+ Video_w2)] = frame2
  return (BG)

video_capture_0 = cv2.VideoCapture(0)
video_capture_1 = cv2.VideoCapture(1)

#seting the video 1 as the default size and fps

fps_c = video_capture_0 .get(cv2.CAP_PROP_FPS)
Video_h =video_capture_0 .get(cv2.CAP_PROP_FRAME_HEIGHT)
Video_w = video_capture_0 .get(cv2.CAP_PROP_FRAME_WIDTH)

fps_c2 = video_capture_1.get(cv2.CAP_PROP_FPS)
Video_h2 = video_capture_1.get(cv2.CAP_PROP_FRAME_HEIGHT)
Video_w2 = video_capture_1.get(cv2.CAP_PROP_FRAME_WIDTH)

#args for the video output
fps = fps_c

if Window == None:
  size = (int(Video_w+Video_w2), int(Video_h))
else:
    size = (int(Window.split("x")[0]), int(Window.split("x")[1]))

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
videowriter = cv2.VideoWriter(OUTPUT + ".avi",fourcc,fps,size)

while True:
    # Capture frame-by-frame
    ret0, frame0 = video_capture_0.read()
    ret1, frame1 = video_capture_1.read()
   # connect the videos into a single frame
    img = Fram_connect(frame0, frame1, Video_w, Video_h,  Video_w2, Video_h2)
    img_1 = cv2.resize(img, size, interpolation = cv2.INTER_AREA)
   # write and save video as avi fromat
    videowriter.write(img_1)
    # show both the frames
    cv2.imshow('comb',img_1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture_0.release()
video_capture_1.release()
cv2.destroyAllWindows()
