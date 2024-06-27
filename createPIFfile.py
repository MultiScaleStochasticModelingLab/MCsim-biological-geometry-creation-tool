import numpy as np


def createPIFfile2D(data,filename,segmentationThreshold,cellName):

	dataDim = np.shape(data)

	PIFfile = open(filename+".pif",'w')
	cellID = 0

	for i in range(dataDim[0]):
		for j in range(dataDim[1]):
			if data[i,j] > segmentationThreshold:
				PIFfile.write("%s 	"%(cellID))
				PIFfile.write("%s 	"%cellName)
				PIFfile.write("%s 	%s 	%s 	%s 	%s 	%s\n"%(i,i,j,j,0,0))
				cellID += 1

	PIFfile.close()

def createPIFfile3D(data,filename,segmentationThreshold,cellName):

	dataDim = np.shape(data)

	PIFfile = open(filename+".pif",'w')
	cellID = 0

	for i in range(dataDim[0]):
		for j in range(dataDim[1]):
			for k in range(dataDim[2]):
				if data[i,j,k] > segmentationThreshold:
					PIFfile.write("%s 	"%(cellID))
					PIFfile.write("%s 	"%cellName)
					PIFfile.write("%s 	%s 	%s 	%s 	%s 	%s\n"%(i,i,j,j,k,k))
					cellID += 1

	PIFfile.close()