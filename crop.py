import numpy as np
import pydicom
from nibabel.testing import data_path
import nibabel as nib

class bcolors:
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def crop2D(data,cropDimensions,cropOrigin,threshold):
	
	dataDim = np.shape(data)

	cropLowerLimits = cropOrigin
	cropSize 		= cropDimensions
	
	cropUpperLimits = [cropLowerLimits[0]+cropSize[0], \
				   		cropLowerLimits[1]+cropSize[1]]

	if cropUpperLimits[0] > dataDim[0] or cropUpperLimits[1] > dataDim[1]:
		print(f"{bcolors.ERROR}error: the crop limit is out of bounds from the original image{bcolors.ENDC}")
		exit(1)

	newData = data[cropLowerLimits[0]:cropUpperLimits[0],cropLowerLimits[1]:cropUpperLimits[1]]

	lattice = np.full((cropSize[0],cropSize[1]), 0.0)

	for i in range(cropSize[0]):
		for j in range(cropSize[1]):
			if newData[i,j] > threshold:
				lattice[i,j] = newData[i,j]

	return lattice, cropLowerLimits, cropUpperLimits

def crop3D(data,cropDimensions,cropOrigin,threshold):
	
	dataDim = np.shape(data)

	cropLowerLimits = cropOrigin
	cropSize 		= cropDimensions
	
	cropUpperLimits = [cropLowerLimits[0]+cropSize[0], \
				   		cropLowerLimits[1]+cropSize[1], \
				   		cropLowerLimits[2]+cropSize[2]]

	if cropUpperLimits[0] > dataDim[0] or cropUpperLimits[1] > dataDim[1] or cropUpperLimits[2] > dataDim[2]:
		print(f"{bcolors.ERROR}error: the crop limit is out of bounds from the original image{bcolors.ENDC}")
		exit(1)

	newData = data[cropLowerLimits[0]:cropUpperLimits[0],cropLowerLimits[1]:cropUpperLimits[1],cropLowerLimits[2]:cropUpperLimits[2]]

	lattice = np.full((cropSize[0],cropSize[1],cropSize[2]), 0.0)

	for i in range(cropSize[0]):
		for j in range(cropSize[1]):
			for k in range(cropSize[2]):
				if newData[i,j,k] > threshold:
					lattice[i,j,k] = newData[i,j,k]

	return lattice, cropLowerLimits, cropUpperLimits

