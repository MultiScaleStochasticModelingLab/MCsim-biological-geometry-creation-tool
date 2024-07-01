import numpy as np
from scipy.ndimage import zoom
from scipy.signal import resample_poly

def resize2D(data,resizeFactor,segmentationThreshold):

	resizeFactor = int(resizeFactor)

	originalData = np.where(data > segmentationThreshold,1.0,0.0) # filled (1) or not filled (0)
	originalDataDim = np.shape(originalData)
	dimensions = len(originalDataDim)

	filledPixelsOriginal = np.count_nonzero(originalData > 0)
	
	#print("------------------- OLD:", filledPixelsOriginal/(originalDataDim[0]*originalDataDim[1]))


	if resizeFactor > 0: #downsampling
		resizeFactors = [(1, resizeFactor), (1, resizeFactor)]
	#if resizeFactor < 0: #oversampling
	#	resizeFactors = [(resizeFactor, 1), (resizeFactor, 1), (resizeFactor, 1)]


	tempData = originalData
	for k in range(dimensions):
		tempData = resample_poly(tempData, resizeFactors[k][0], resizeFactors[k][1], axis=k)

	newData = tempData
	newDataDim = np.shape(newData)

	resizeThreshold = 1 - 1/resizeFactor
	resizeThreshold = 1/resizeFactor
	resizeThreshold = 0.5

	print(resizeThreshold)

	for i in range(newDataDim[0]):
		for j in range(newDataDim[1]):
			if newData[i,j] > resizeThreshold:
				newData[i,j] = 1
			else:
				newData[i,j] = 0

	filledPixelsOriginalResized = np.count_nonzero(newData > 0)


	#print("------------------- NEW:", filledPixelsOriginalResized/(newDataDim[0]*newDataDim[1]))

	return newData


def resize3D(data,resizeFactor,segmentationThreshold):

	resizeFactor = int(resizeFactor)

	originalData = np.where(data > segmentationThreshold,1.0,0.0) # filled (1) or not filled (0)
	originalDataDim = np.shape(originalData)
	dimensions = len(originalDataDim)

	filledPixelsOriginal = np.count_nonzero(originalData > 0)
	
	print("------------------- OLD:", filledPixelsOriginal/(originalDataDim[0]*originalDataDim[1]*originalDataDim[2]))


	if resizeFactor > 0: #downsampling
		resizeFactors = [(1, resizeFactor), (1, resizeFactor), (1, resizeFactor)]
	#if resizeFactor < 0: #oversampling
	#	resizeFactors = [(resizeFactor, 1), (resizeFactor, 1), (resizeFactor, 1)]

	tempData = originalData
	for k in range(dimensions):
		tempData = resample_poly(tempData, resizeFactors[k][0], resizeFactors[k][1], axis=k)

	newData = tempData
	newDataDim = np.shape(newData)

	resizeThreshold = 1 - 1/resizeFactor
	resizeThreshold = 1/resizeFactor
	resizeThreshold = 0.5

	print(resizeThreshold)

	for i in range(newDataDim[0]):
		for j in range(newDataDim[1]):
			for k in range(newDataDim[2]):
				if newData[i,j,k] > resizeThreshold:
					newData[i,j,k] = 1
				else:
					newData[i,j,k] = 0

	filledPixelsOriginalResized = np.count_nonzero(newData > 0)


	print("------------------- NEW:", filledPixelsOriginalResized/(newDataDim[0]*newDataDim[1]*newDataDim[2]))

	return newData
















