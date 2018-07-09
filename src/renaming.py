#!/user/bin/python3

import os
from shutil import copyfile
import datetime

wd = os.getcwd()

if 'mnt' in wd:
	pictureDir = "/mnt/c/Users/hmmar/Google Drev (hannahmariemartiny@gmail.com)/iGEM 2018/Wet lab/Pictures of plates/"
else:
	pictureDir = "C:\\Users\\hmmar\\Google Drev (hannahmariemartiny@gmail.com)\\iGEM 2018\\Wet lab\\Pictures of plates\\"

dateDirs = os.listdir(pictureDir)
dateDirs = [x for x in dateDirs if x.endswith("plates")] # only work with correct picture folders

# MOVE PICTURES
for dateDir in dateDirs:
	date = datetime.datetime.strptime(dateDir.split(' ')[0], '%d-%m-%Y').strftime('%Y-%m-%d')

	destDir = wd + '/data/pic/'

	if not os.path.exists(destDir):
	    os.makedirs(destDir)

	pictureFiles = os.listdir(pictureDir + dateDir)

	pictureFiles = [x for x in pictureFiles if x.endswith('.jpg')]

	for pictureFile in pictureFiles:
		print(pictureFile)

		copyfile(pictureDir + dateDir +'/' + pictureFile,  destDir + date + '_' + pictureFile.replace(' ', '_'))
