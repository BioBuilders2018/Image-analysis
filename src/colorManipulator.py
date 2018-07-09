#!/user/bin/python3

import numpy as np
import argparse
import cv2
import os
from skimage import measure
from imutils import contours
import imutils
from colorSettings import *

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-c", "--circlesize", required = True, help = "Size of circle", type=int)
# ap.add_argument("-m", "--medium", required = True, help = "PDA or MEA?", type=str, choices = ['PDA', 'MEA'])
ap.add_argument("-i", "--image", required = True, help = "path to image", type = str)
ap.add_argument("-f", "--firstday", help = "Picture from first day of experiment", action = 'store_true')

args = vars(ap.parse_args())
print(args)

# wd = os.getcwd()
#
# if 'mnt' in wd:
# 	pictureDir = "/mnt/c/Users/hmmar/Google Drev (hannahmariemartiny@gmail.com)/iGEM 2018/Wet lab/Pictures of plates/"
# else:
# 	pictureDir = "C:\\Users\\hmmar\\Google Drev (hannahmariemartiny@gmail.com)\\iGEM 2018\\Wet lab\\Pictures of plates\\"
#
# dateDirs = os.listdir(pictureDir)
# dateDirs = [x for x in dateDirs if x.endswith("plates")] # only work with correct picture folders

## CODE INSPIRATION
# http://www.sixthresearcher.com/counting-blue-and-white-bacteria-colonies-with-python-and-opencv/

# load the image
image_orig = cv2.imread(args["image"])
height_orig, width_orig = image_orig.shape[:2]

# center of image
img_center = (int(height_orig/2), int(width_orig / 2))

# output the image with contours
image_contours = image_orig.copy()

# color bounds (INVERTED COLORS) and output dfs
medium = args["image"].split('/')[-1].split('_')[0].strip(' ')

if "Sc" in args["image"]:
	# if os.path.exists('data/Sc.pkl'):
	lower, upper, contourLimit = ScSettings(medium=medium)
	# else:
		# lower, upper, contourLimit = ScSettings(medium=medium, firstday = True)
elif "Po" in args["image"]:
	# if os.path.exists('data/Po.pkl'):
		# df = pd.read_pickle('data/Po.pkl')
	lower, upper, contourLimit = PoSettings(medium=medium)
	# else:
		# lower, upper, contourLimit = PoSettings(medium=medium, firstday = True)
elif "Sc_Delta" in args["image"]:
	# if os.path.exists('data/ScDelta.pkl'):
		# df = pd.read_pickle('data/ScDelta.pkl')
	lower, upper, contourLimit = ScDeltaSettings(medium=medium)
	# else:
		# lower, upper, contourLimit = ScDeltaSettings(medium=medium, firstday = True)
elif "oryzae" in args["image"]:
	# if os.path.exists('data/ScDelta.pkl'):
		# df = pd.read_pickle('data/ScDelta.pkl')
	lower, upper, contourLimit = AoSettings(medium=medium)
	# else:
		# lower, upper, contourLimit = AoSettings(medium=medium, firstday = True)

# copy of original image
image_to_process = image_orig.copy()

image_to_process = (255-image_to_process)

# find the colors within the specified boundaries
image_mask = cv2.inRange(image_to_process, lower, upper)
# apply the mask
image_res = cv2.bitwise_and(image_to_process, image_to_process, mask = image_mask)

## load the image, convert it to grayscale, and blur it slightly
image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
image_gray = cv2.GaussianBlur(image_gray, (1, 1), 0)

# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
image_edged = cv2.Canny(image_gray, 50, 100)
image_edged = cv2.dilate(image_edged, None, iterations=1)
image_edged = cv2.erode(image_edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

circles = []
circleCenters = []

def drawCircle(c, drawImage, contourArea, color):

	# compute the Convex Hull of the contour
	hull = cv2.convexHull(c)

	# prints contours in red color
	cv2.drawContours(drawImage,[hull],0, color ,5)

	((x, y), radius) = cv2.minEnclosingCircle(c)
	center = (int(x), int(y))

	cv2.putText(drawImage, str(area), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)

	# cv2.circle(drawImage, center, int(radius), color, 2)

	return center

def findCenters(circlecenters, image_center, color, noCol, drawImage):
	ClosestPoints = []

	for i in range(noCol):
		closest = min(circlecenters, key=lambda c:  (c[0]- (image_center[0] + 100))**2 + (c[1]-(image_center[1] + 100))**2)
		ClosestPoints += [closest]
		circlecenters.pop(circleCenters2.index(closest))

		cv2.circle(drawImage, closest, 5, color, -1)

	return ClosestPoints

# loop over the contours individually
for c in cnts:
	area = cv2.contourArea(c)
	# if the contour is not sufficiently large, ignore it
	if area < contourLimit:
		continue
	# print(area)

	# if area < 2000 :#and area < 3500: # avsoid petris dish circle
		# print("area:", area)

		# center = drawCircle(c=c, drawImage=image_contours, contourArea=area, color = (0, 0, 255))
		# circleCenters += [center]

	if area > 5000 and area < 40000:
		print("area:", area)

		center = drawCircle(c=c, drawImage=image_contours, contourArea=area, color = (0, 0, 255))
		circleCenters += [center]

		# cv2.circle(image_contours, center, int(radius), (0, 255, 255), 2)
		# cv2.circle(image_contours, center, 5, (255, 0, 0), -1)

circleCenters2 = circleCenters.copy()

try:
	ClosestPoints = findCenters(circlecenters=circleCenters.copy(), image_center=img_center, color = (255, 255, 0), noCol=3, drawImage=image_contours)
# print(cnts)
	print(ClosestPoints)
except:
	pass

# show image
# cv2.imshow('detected Edge',img1)
# cv2.imshow('contours',np.hstack([image_orig, image_to_process]))
# cv2.waitKey(0)
# cv2.imshow('contours',np.hstack([image_orig, image_contours]))
# cv2.waitKey(0)
cv2.imwrite('{0}_invert.png'.format(args["image"].replace('.png', '')), np.hstack([image_orig, image_to_process]))
cv2.imwrite('{0}_output.png'.format(args["image"].replace('.png', '')), np.hstack([image_orig, image_contours]))
