import numpy as np

# Sc settings
def ScSettings(medium, firstday = False):
	"""Set the correct settings for the S. commune growth plates"""

	lower = np.array([0, 0, 0])

	if medium == "PDA":
		upper = np.array([60, 70, 80])

	elif medium == "MEA":
		upper = np.array([90, 90, 120])

	elif medium == "YPD":
		upper = np.array([65, 65, 65])
	else:
		# error
		print("Please provide a vaild medium that the fungus has grown on")
		raise()

	if firstday:
		contourLimit = 100
	else:
		contourLimit = 400

	return lower, upper, contourLimit

def ScDeltaSettings(medium, firstday = False):
	"""Set the correct settings for the S. commune deltaSc3 growth plates"""

	if medium == "PDA":
		lower = np.array([4, 20, 80])
		upper = np.array([80, 90, 140])

	elif medium == "MEA":
		lower = np.array([4, 20, 80])
		upper = np.array([70, 80, 90])

	elif medium == "YPD":
		lower = np.array([0, 0, 0])
		upper = np.array([80, 80, 80])
	else:
		# error
		print("Please provide a vaild medium that the fungus has grown on")
		raise()

	if firstday:
		contourLimit = 50
	else:
		contourLimit = 400

	return lower, upper, contourLimit

def PoSettings(medium, firstday = False):
	"""Set the correct settings for the P. ostreatus growth plates"""

	if medium == "PDA":
		lower = np.array([0, 0, 0])
		upper = np.array([25, 90, 170])

	elif medium == "YPD":
		lower = np.array([0, 0, 10])
		upper = np.array([23, 100, 230])
	else:
		# error
		print("Please provide a vaild medium that the fungus has grown on")
		raise()

	if firstday:
		contourLimit = 100
	else:
		contourLimit = 400




	return lower, upper, contourLimit

def AoSettings(medium, firstday = False):
	if medium == "PDA":
		lower = np.array([0, 0, 5])
		upper = np.array([150, 150, 110])

	elif medium == "MEA":
		lower = np.array([0, 0, 0])
		upper = np.array([125, 140, 160])

	elif medium == "YPD":
		lower = np.array([0, 0, 0])
		upper = np.array([140, 140, 140])
	else:
		# error
		print("Please provide a vaild medium that the fungus has grown on")
		raise()

	if firstday:
		contourLimit = 100
	else:
		contourLimit = 400

	return lower, upper, contourLimit
