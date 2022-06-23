import cv2 as cv
import numpy as np

scaleX = 0.1
scaleY = 0.1

base = cv.imread('image1.jpg')
# scale_percent = 20  # percent of original size
# width = int(img.shape[1] * scale_percent / 100)
# height = int(img.shape[0] * scale_percent / 100)
# dim = (width, height)
# base = cv.resize(img, dim, interpolation = cv.INTER_AREA)
base = cv.resize(base, None, fx= scaleX, fy= scaleY, interpolation= cv.INTER_LINEAR)

test1 =  cv.imread('image2.jpg')
# scale_percent = 20  # percent of original size
# width = int(test1.shape[1] * scale_percent / 100)
# height = int(test1.shape[0] * scale_percent / 100)
# dim = (width, height)
# test1 = cv.resize(test1, dim, interpolation = cv.INTER_AREA)
test1 = cv.resize(test1, None, fx= scaleX, fy= scaleY, interpolation= cv.INTER_LINEAR)

test = cv.imread('test.jpg')
# scale_percent = 20  # percent of original size
# width = int(test.shape[1] * scale_percent / 100)
# height = int(test.shape[0] * scale_percent / 100)
# dim = (width, height)
# test = cv.resize(test, dim, interpolation = cv.INTER_AREA)
test = cv.resize(test, None, fx= scaleX, fy= scaleY, interpolation= cv.INTER_LINEAR)

hsv_base = cv.cvtColor(base, cv.COLOR_BGR2HSV)
hsv_test = cv.cvtColor(test, cv.COLOR_BGR2HSV)
hsv_test1 = cv.cvtColor(test1, cv.COLOR_BGR2HSV)

h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]
h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges
channels = [0, 1]

hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
hist_test = cv.calcHist([hsv_test], channels, None, histSize, ranges, accumulate=False)
cv.normalize(hist_test, hist_test, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
hist_test1 = cv.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

compare_method = cv.HISTCMP_CORREL

base_base = cv.compareHist(hist_base, hist_base, compare_method)
base_test = cv.compareHist(hist_base, hist_test, compare_method)
base_test1 = cv.compareHist(hist_base, hist_test1, compare_method)
print('base_base Similarity = ', base_base)
print('base_test1 Similarity = ', base_test1)
print('base_test Similarity = ', base_test)

cv.imshow('base',base)
cv.imshow('test',test) 
cv.imshow('test1',test1)
cv.waitKey(0)
