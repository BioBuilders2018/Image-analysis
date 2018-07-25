#!/user/bin/python3
import pandas as pd
import numpy as np

def PolyArea(x,y):
	return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
def CircleArea(r):
	return np.pi*np.square(r)
def EllipseArea(rx, ry):
	return np.pi * rx * ry

# ANNOTATIONS MADE BY PROGRAM VIA
# http://www.robots.ox.ac.uk/~vgg/software/via/
org_df = pd.read_csv('data/annotations.csv', sep = ",", index_col = None)

# can drop file size, file attributes
org_df = org_df.drop(['file_size', 'file_attributes', 'region_attributes'], axis = 1)

mediaDict = []
tempLightDict = []

for i, row in org_df.iterrows():
	fileSplit =  row["filename"].split('_')
	date = fileSplit[0]
	try:
		attr = eval(row["region_shape_attributes"].replace('.', ','))
		area = CircleArea(attr['r'])
	except SyntaxError:
		attr = eval(row["region_shape_attributes"].replace('.', ','))
		area = CircleArea(attr['r'])
	except KeyError:
		if len(attr) == 0:
			attr = eval(row['region_id'].replace('.', ','))
			if "ellipse" in attr["name"]:
				area = EllipseArea(attr["rx"], attr["ry"])
			elif "circle" in attr["name"]:
				area = CircleArea(attr['r'])
		elif "polygon" in attr["name"]:
			x = np.asarray(attr["all_points_x"])
			y = np.asarray(attr["all_points_y"])
			area = PolyArea(x, y)

	if 'dark' in row["filename"] or 'light' in row["filename"]:
		species = "".join(fileSplit[1])
		temp = fileSplit[2].strip('C')
		light = fileSplit[3].strip('.jpg')
		dupl = 1

		tempLightDict.append({'species': species, 'temperature': temp, 'light_source': light, 'date': date, 'dupl': dupl, 'area': area, 'medium': 'PDA', 'concentration': 58.5})

	else:
		try:
			medium = fileSplit[1]
			conc = fileSplit[2]
			species = "".join(fileSplit[3])
			dupl = fileSplit[4].replace('.jpg', '').replace('#', '')
		except IndexError:
			conc = None
			species = "".join(fileSplit[2]).replace('.jpg', '')
			dupl = 1

		mediaDict.append({'species': species, 'medium': medium, 'concentration': conc, 'date': date, 'dupl': dupl, 'area': area, 'temperature': 30, 'light_source': 'dark'})

df1 = pd.DataFrame(mediaDict)
df1.to_csv('data/medium_growths.csv', sep = ",", index = False)

df2 = pd.DataFrame(tempLightDict)
df2.to_csv('data/tempLight_growths.csv', sep = ",", index = False)

df3 = pd.merge(df1, df2, how = 'outer')
df3.to_csv('data/merged_data.csv', sep = ",", index = False)
