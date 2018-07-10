#!/user/bin/python3

import os
from shutil import copyfile
import datetime
import numpy as np
import re

wd = os.getcwd()

if 'mnt' in wd:
	pictureDir = "/mnt/c/Users/hmmar/Google Drev (hannahmariemartiny@gmail.com)/iGEM 2018/Wet lab/Pictures of plates/"
else:
	pictureDir = "C:\\Users\\hmmar\\Google Drev (hannahmariemartiny@gmail.com)\\iGEM 2018\\Wet lab\\Pictures of plates\\"

dateDirs = os.listdir(pictureDir)
# dateDirs = [x for x in dateDirs if x.endswith("plates")] # only work with correct picture folders
dateDirs = ["2018-07-10_plates"]
## RENAMING SCHEME
# temp media growths
# 'media_concentration_species_duplicate.jpg'
# date: YYYY-MM-DD
# media: string, e.g. MEA
# concentration: use dot to indicate decimal, e.g. 47.5
# species: write full species name, e.g. Sc becomes S.commune. Full rules can be found below
# duplicate: #1 or #2

# light growths
# species_temperature_lightsource_duplicate.jpg
# species: write full species name, e.g. Sc becomes S.commune. Full rules can be found below
# temperature:
# light source: either light or dark
# duplicate: #1 or #2


speciesVariations = {
	'Sc': 'S.commune', 'S.Commune': 'S.commune', 'Scomwt': 'S.commune',
	'ScDeltaSC3': 'S.commune.DSC3', 'SComSC3': 'S.commune.DSC3',  'S.communeDSC3':  'S.commune.DSC3', 'S.communeSC3':  'S.commune.DSC3',
	'Po': 'P.ostreatus', 'P.Ostreatus': 'P.ostreatus', 'Post': 'P.ostreatus', 'P.Ostreatus': 'P.ostreatus',
	'A.Oryzae': 'A.oryzae', 'Aory': 'A.oryzae'
}

# MOVE PICTURES
for dateDir in dateDirs:
	try:
		date = datetime.datetime.strptime(dateDir.split(' ')[0], '%d-%m-%Y').strftime('%Y-%m-%d')
	except:
		date = dateDir.split('_')[0]
	print(date)

	destDir = wd + '/data/pic/'

	if not os.path.exists(destDir):
	    os.makedirs(destDir)

	pictureFiles = os.listdir(pictureDir + dateDir)
	pictureFiles = [x for x in pictureFiles if x.endswith('.jpg')]

	for pictureFile in pictureFiles:

		pictureFileOld = pictureFile

		if 'liight' in pictureFile:
			pictureFile = pictureFile.replace('liight', 'light')

		pictureFile = pictureFile.replace(' ', '_')
		pictureSplit =  pictureFile.split('_')

		if 'dark' in pictureFile.lower() or 'light' in pictureFile.lower():
			if '#' in pictureFile:
				dupl = pictureSplit[-1].strip('.jpg')
				light = pictureSplit[-2]
				temp = pictureSplit[-3].strip('C')

				species = "".join(pictureSplit[:-3])

				if species in speciesVariations:
					species = speciesVariations[species]
			if "Dark" in pictureFile:
				dupl = pictureSplit[-1].strip('.jpg')

				temp = pictureSplit[-3].strip('C')
				light = pictureSplit[-2].lower()

				species = "".join(pictureSplit[:-2])
				if species in speciesVariations:
					species = speciesVariations[species]

			else:

				if '#' in pictureFile:
					light = pictureSplit[-2]
					temp = pictureSplit[-3]
					dupl = pictureSplit[-1].strip('.jpg')
					species = "".join(pictureSplit[:-3])
				else:
					light = pictureSplit[-1].strip('.jpg')
					temp = pictureSplit[-2].strip('C')
					dupl = "#1"

					species = "".join(pictureSplit[:-2])

				if species in speciesVariations:
					species = speciesVariations[species]

			newFileName = "{1}_{2}_{3}_{4}.jpg".format(date, species, temp, light, dupl)
		else:
			if "YPD" in pictureFile:
				media = pictureSplit[0]

				if '#' in pictureFile:
					# duplicate number
					dupl = pictureSplit[-1].strip('.jpg')

					# extract specie name
					species = "".join(pictureSplit[1:-1])
				else:
					dupl = "#1"
					species = "".join(pictureSplit[1::]).strip('.jpg')

				if species in speciesVariations:
					species = speciesVariations[species]

				conc = np.nan # unknown

				# media_concentration_species_duplicate.jpg
			else:
				media =pictureSplit[0]
				conc = pictureSplit[1].replace(',', '.')
				dupl = pictureSplit[-1].strip('.jpg')

				species = "".join(pictureSplit[2:-1])
				if species in speciesVariations:
					species = speciesVariations[species]

			newFileName = "{1}_{2}_{3}_{4}.jpg".format(date, media, conc, species, dupl)

		try:
			os.rename(pictureDir + dateDir +'/' + pictureFileOld, pictureDir + dateDir +'/' + newFileName)
			copyfile(pictureDir + dateDir +'/' + pictureFileOld,  destDir + date + '_' + newFileName)
		except:
			pass

	os.rename(pictureDir + dateDir, pictureDir + date + '_plates')
