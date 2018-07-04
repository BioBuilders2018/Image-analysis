#!/user/bin/python3

import numpy as np
import argparse
import cv2
import os
from skimage import measure
from imutils import contours
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-c", "--circlesize", required = True, help = "Size of circle", type=int)
# ap.add_argument("-m", "--medium", required = True, help = "PDA or MEA?", type=str, choices = ['PDA', 'MEA'])
ap.add_argument("-i", "--image", required = True, help = "path to image", type = str)

args = vars(ap.parse_args())
print(args)

wd = os.getcwd()

if 'mnt' in wd:
	pictureDir = "/mnt/c/Users/hmmar/Google Drev (hannahmariemartiny@gmail.com)/iGEM 2018/Wet lab/Pictures of plates/"
else:
	pictureDir = "C:\\Users\\hmmar\\Google Drev (hannahmariemartiny@gmail.com)\\iGEM 2018\\Wet lab\\Pictures of plates\\"

dateDirs = os.listdir(pictureDir)
dateDirs = [x for x in dateDirs if x.endswith("plates")] # only work with correct picture folders

## CODE INSPIRATION
# http://www.sixthresearcher.com/counting-blue-and-white-bacteria-colonies-with-python-and-opencv/

# load the image
image_orig = cv2.imread(args["image"])
height_orig, width_orig = image_orig.shape[:2]

# output the image with contours
image_contours = image_orig.copy()

# color bounds (INVERTED COLORS)
lower = np.array([30, 30, 60])
upper = np.array([100, 120, 80])

# copy of original image
image_to_process = image_orig.copy()

image_to_process = (255-image_to_process)

# find the colors within the specified boundaries
image_mask = cv2.inRange(image_to_process, lower, upper)
# apply the mask
image_res = cv2.bitwise_and(image_to_process, image_to_process, mask = image_mask)

## load the image, convert it to grayscale, and blur it slightly
image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
image_gray = cv2.GaussianBlur(image_gray, (5, 5), 0)

# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
image_edged = cv2.Canny(image_gray, 50, 100)
image_edged = cv2.dilate(image_edged, None, iterations=1)
image_edged = cv2.erode(image_edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours individually
for c in cnts:
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) < 10000:
		continue

	# compute the Convex Hull of the contour
	hull = cv2.convexHull(c)
	# prints contours in red color
	cv2.drawContours(image_contours,[hull],0,(1,0,255),5)

# Writes the output image
# cv2.imwrite(args["output"],image_contours)

# show image
# cv2.imshow('detected Edge',img1)
# cv2.imshow('contours',np.hstack([image_orig, image_to_process]))
# cv2.waitKey(0)
cv2.imshow('contours',np.hstack([image_orig, image_contours]))
cv2.waitKey(0)
cv2.imwrite('test.png', np.hstack([image_orig, image_contours]))
