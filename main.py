from tkinter import filedialog
from tkinter import *
import sys, os
import pydicom
import matplotlib.pyplot as plt

from createPIFfile import *
from createImageCubeFile import *
from crop import *
from resize import *

class bcolors:
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def exitProgram():
    exit(1)

def printHelp():
    print(f"{bcolors.UNDERLINE}Use:{bcolors.ENDC}")
    print('main.py --m [mode] [parameterFile]')
    print(' Parameters:')
    print('   [mode]: gui or file ')
    print('   [parameterFile]: ONLY IF "file" mode selected: txt file including:')
    print('\t (1) Original segmentation image: path to file')
    print('\t (2) Threshold value (>) for data of interest in segmenation image')
    print('\t (3) Crop?: Yes or No')
    print('\t (4) Crop dimensions: dimX, dimY, dimZ (in pixels) - leave blank if no cropping')
    print('\t (5) Origin vextex for cropping: dimX, dimY, dimZ (in pixels) - leave blank if no cropping')
    print('\t (6) Resize?: Yes or No')
    print('\t (7) Resizing factor: +- 2,3,4... (>0 to reduce, <0 to increase resolution) - leave blank if no resizing')
    print('\t (8) Cluster pixels into cells?: Yes or No')
    print('\t (9) Cell volume: minumum and maximum number of pixels per cell. Input the two values separated by a comma - leave blank if no clustering')
    print('\t (10) Output cell type (e.g., neuron, vascular...)')
    print('\t (11) Output directory')
    exit(1)


global inFileName
def browse_file_button():
    global inFileName 
    filename = filedialog.askopenfilename()
    inFileName.set(filename)

def _quit():
    root.quit()
    root.destroy()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Mode selection
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
narg = len(sys.argv)
if narg == 1:
	print(f"{bcolors.ERROR}error: please select a valid mode{bcolors.ENDC}")
	printHelp()
	exitProgram()

for i in range(narg):
    option = sys.argv[i].lower()
    if '--' in option:
        if option == '--help' or option == '--h':
                printHelp()
        elif option == '--m':
                if sys.argv[i+1] == 'gui':
                    mode = 'gui'
                elif sys.argv[i+1] == 'file':
                    mode = 'file'
                    try:
                        inputFile = sys.argv[i+2]
                    except:
                    	print(f"{bcolors.ERROR}error: parameterFile is required in mode 'inputfile'{bcolors.ENDC}")
                    	printHelp()
                    	exitProgram()
                    try:
                        f = open(inputFile, "r")
                    except:
                        print(f"{bcolors.ERROR}error: file '%s' not found {bcolors.ENDC}" %inputFile)
                        exitProgram()
                    f.close()
                else: 
                    print(f"{bcolors.ERROR}error: please select a valid mode{bcolors.ENDC}")
                    printHelp()
                    exitProgram()
        else:
            print(f"{bcolors.ERROR}error: please select a valid mode{bcolors.ENDC}")
            printHelp()
            exitProgram() 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

doCrop = False
doResize = False
doCluster = False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# FILE mode
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if mode == 'file':
	print("\n Working in file mode...")
	correctInputData = True
	inputInfo = open(inputFile,'r').read().split('\n')
    #inputInfo = list(filter(None, inputInfo)) # filter empty lines
	requiredArg = 11
	if len(inputInfo) != requiredArg:
		print(f"{bcolors.ERROR} %s arguments found in input file. %s arguments required {bcolors.ENDC}" %(len(inputInfo)),requiredArg)
		printHelp()
		exitProgram()
    
	segmentationFile	= inputInfo[0]
	cropping			= inputInfo[2].lower()
	resizing			= inputInfo[5].lower()
	clustering			= inputInfo[7].lower()
	outCellName			= inputInfo[9]
	outDirectory		= inputInfo[10]
	if cropping == "yes": doCrop = True
	elif cropping == "no": doCrop = False
	else: correctInputData = False
	if resizing == "yes": doResize = True
	elif resizing == "no": doResize = False
	else: correctInputData = False
	if clustering == "yes": doCluster = True
	elif clustering == "no": doCluster = False
	else: correctInputData = False
	try: 
		segmentationThreshold = float(inputInfo[1])
		cropDimensionsTemp	= inputInfo[3].split(',')
		cropOriginTemp		= inputInfo[4].split(',')
		cropDimensions 		= np.array([eval(i) for i in cropDimensionsTemp])
		cropOrigin	 		= np.array([eval(i) for i in cropOriginTemp])
		resizeFactor 		= float(inputInfo[6])
		inputCellVolume = list(inputInfo[8].split(","))
		#exit(1)
		if inputCellVolume == "": 
			maxCellVolume = float('inf')
			minCellVolume = 2
		else: 
			minCellVolume = int(inputCellVolume[0])
			maxCellVolume = int(inputCellVolume[1])
	except:
		correctInputData = False
    
	if correctInputData == False:
		print(f"{bcolors.ERROR} Incorrect data format in '%s;{bcolors.ENDC}" %inputFile)
		printHelp()
		exitProgram()
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# GUI mode
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if mode == 'gui':
	print("\n Working in GUI mode...")
	root = Tk()

	################
	i = 1
	label1=StringVar()
	label1.set('Original segmentation file')
	lbl1 = Label(master=root, textvariable=label1) 
	lbl1.grid(row=i, column=1)
	button1 = Button(text="Browse", command=browse_file_button)
	button1.grid(row=i, column=2)
 
	inFileName = StringVar()
	inFileName.set('')
	lbl1 = Label(master=root, textvariable=inFileName)
	lbl1.grid(row=i+1, column=1)
	################
	i += 2
	label2=StringVar()
	label2.set('Threshold value (>) for segmentation')
	lbl2 = Label(master=root, textvariable=label2)
	lbl2.grid(row=i, column=1)
	threshold = StringVar()
	threshold.set(0.0)
	thresholdEntry = Entry(master=root, textvariable=threshold)
	thresholdEntry.grid(row=i, column=2)

	lbl2 = Label()
	lbl2.grid(row=i+1, column=1)
	################
	i += 2
	label3=StringVar()
	label3.set("Crop?")
	lbl3 = Label(master=root, textvariable=label3)
	lbl3.grid(row=i, column=1)
	crop = StringVar()
	crop.set('select')
	options = ["Yes", "No"]
	cropEntry = OptionMenu(root , crop , *options)
	cropEntry.grid(row=i, column=2)

	lbl3 = Label()
	lbl3.grid(row=i+1, column=1)
	################
	i += 2
	label4=StringVar()
	label4.set('\t Crop dimensions (x,y,z in pixels)')
	lbl4 = Label(master=root, textvariable=label4)
	lbl4.grid(row=i, column=1)
	cropDim = StringVar()
	cropDim.set('1,1,1')
	cropDimEntry = Entry(master=root, textvariable=cropDim)
	cropDimEntry.grid(row=i, column=2)

	lbl5 = Label()
	lbl5.grid(row=i+1, column=1)
	################
	i += 2
	label5=StringVar()
	label5.set('\t Crop origin (x,y,z in pixels)')
	lbl5 = Label(master=root, textvariable=label5)
	lbl5.grid(row=i, column=1)
	cropOri = StringVar()
	cropOri.set('0,0,0')
	cropOriEntry = Entry(master=root, textvariable=cropOri)
	cropOriEntry.grid(row=i, column=2)

	lbl5 = Label()
	lbl5.grid(row=i+1, column=1)
	################
	i += 2
	label6=StringVar()
	label6.set("Resize?")
	lbl6 = Label(master=root, textvariable=label6)
	lbl6.grid(row=i, column=1)
	resize = StringVar()
	resize.set('select')
	options = ["Yes", "No"]
	resizeEntry = OptionMenu(root , resize , *options)
	resizeEntry.grid(row=i, column=2)

	lbl6 = Label()
	lbl6.grid(row=i+1, column=1)
	################
	i += 2
	label7=StringVar()
	label7.set('Resize factor (integer) \n positive/negative to reduce/increase resolution')
	lbl7 = Label(master=root, textvariable=label7)
	lbl7.grid(row=i, column=1)
	resizeFact = StringVar()
	resizeFact.set(1)
	resizeFactEntry = Entry(master=root, textvariable=resizeFact)
	resizeFactEntry.grid(row=i, column=2)

	lbl7 = Label()
	lbl7.grid(row=i+1, column=1)
	################
	i += 2
	label8=StringVar()
	label8.set("Clustering?")
	lbl8 = Label(master=root, textvariable=label8)
	lbl8.grid(row=i, column=1)
	cluster = StringVar()
	cluster.set('select')
	options = ["Yes", "No"]
	clusterEntry = OptionMenu(root , cluster , *options)
	clusterEntry.grid(row=i, column=2)

	lbl8 = Label()
	lbl8.grid(row=i+1, column=1)
	################
	i += 2
	label9=StringVar()
	label9.set('Maximum, minimum cluster volume (in pixels)')
	lbl9 = Label(master=root, textvariable=label9)
	lbl9.grid(row=i, column=1)
	cellSize = StringVar()
	cellSize.set('2,10000')
	cellSizeEntry = Entry(master=root, textvariable=cellSize)
	cellSizeEntry.grid(row=i, column=2)

	lbl9 = Label()
	lbl9.grid(row=i+1, column=1)
	################
	i += 2
	label10=StringVar()
	label10.set('Cell name')
	lbl10 = Label(master=root, textvariable=label10)
	lbl10.grid(row=i, column=1)
	outCell = StringVar()
	outCell.set("CellType1")
	outCellEntry = Entry(master=root, textvariable=outCell)
	outCellEntry.grid(row=i, column=2)

	lbl10 = Label()
	lbl10.grid(row=i+1, column=1)
	################
	i += 2
	label11=StringVar()
	label11.set('Output directory')
	lbl11 = Label(master=root, textvariable=label11)
	lbl11.grid(row=i, column=1)
	outDir = StringVar()
	outDir.set("")
	outDirEntry = Entry(master=root, textvariable=outDir)
	outDirEntry.grid(row=i, column=2)

	lbl11 = Label()
	lbl11.grid(row=i+1, column=1)
	################
	i += 2
	exitButton = Button(text="Run", command=_quit)
	exitButton.grid(row=i, column=1)
	lbl10 = Label()
	lbl10.grid(row=i+1, column=1)
    ################
	i += 0
	abortButton = Button(text="Exit", command=exitProgram)
	abortButton.grid(row=i, column=2)
	lbl11 = Label()
	lbl11.grid(row=i+1, column=2)
    ################
	mainloop()

	segmentationFile = inFileName.get()
	try: segmentationThreshold = float(threshold.get())
	except:
		print(f"{bcolors.ERROR} Incorrect 'Segmentation threshold' {bcolors.ENDC}")
		exitProgram()
	doCrop = crop.get().lower()
	if doCrop == "yes": 
		doCrop = True
		try: 
			cropDimensions = (list(cropDim.get().split(",")))
			cropDimensions = [int(i) for i in cropDimensions]
		except:
			print(f"{bcolors.ERROR} Incorrect 'Crop dimensions' {bcolors.ENDC}")
			exitProgram()
		try: 
			cropOrigin = list(cropOri.get().split(","))
			cropOrigin = [int(i) for i in cropOrigin]
		except:
			print(f"{bcolors.ERROR} Incorrect 'Crop origin' {bcolors.ENDC}")
			exitProgram()
	elif doCrop == "no": doCrop = False
	else: doCrop = False
	
	doResize = resize.get().lower()
	if doResize == "yes": 
		doResize = True
		try: resizeFactor = int(resizeFact.get())
		except:
			print(f"{bcolors.ERROR} Incorrect 'Resize factor' {bcolors.ENDC}")
			exitProgram()
	elif doResize == "no": doResize = False
	else: doResize = False
	
	doCluster = cluster.get().lower()
	if doCluster == "yes": 
		doCluster = True
		cellVolume = list(cellSize.get().split(","))
		cellVolume = [int(i) for i in cellVolume]
		try: 
			maxCellVolume = abs(int(cellVolume[1]))
			minCellVolume = abs(int(cellVolume[0]))
		except:
			print(f"{bcolors.ERROR} Incorrect 'Cell volume' {bcolors.ENDC}")
			exitProgram()
	elif doCluster == "no": doCluster = False
	else: doCluster = False
	outCellName = outCell.get()
	outDirectory = outDir.get()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if outCellName == "": 
	outCellName = "CellType1"
if outDirectory == "": 
	outDirectory = "."
else: os.system("mkdir ./%s" %outDirectory)

extension = segmentationFile.split(".")[-1]
if extension.lower() == "dcm":
	dataFileType = "dcm"
elif extension.lower() == "nii":
	dataFileType = "nii"
elif extension.lower() == "tif" or extension.lower() == "tiff":
	dataFileType = "tif"
else:
	print(f"{bcolors.ERROR}error: unsuported image format. Please input .dcm or .nii files{bcolors.ENDC}")
	exitProgram()


print("Correct input data:")

print("\nReading the image file")
if dataFileType == "nii":
	image = nib.load(segmentationFile)
	data = image.get_fdata()
if dataFileType == "tif":
	data = plt.imread(segmentationFile)
if dataFileType == "dcm":
	image = pydicom.dcmread(segmentationFile)
	data = image.pixel_array
print("done\n")

hmDim = len(np.shape(data))
if hmDim > 3: hmDim = 3
cropDimensions = cropDimensions[0:hmDim]
cropOrigin = cropOrigin[0:hmDim]

if doCrop:
	print("Cropping will be perfomed")
	print("\t Crop dimensions in x, y, z = %s" %cropDimensions)
	print("\t Crop origin in x, y, z = %s" %cropOrigin)
else:
	print("Cropping will not be perfomed")
	
if doResize:
	print("Resizing will be perfomed")
	print("\t Resize factor = %s" %resizeFactor)
else:
	print("Resizing will not be perfomed")
if doCluster:
	print("Clustering will be perfomed")
else:
	print("Clustering will not be perfomed")
if maxCellVolume == float('inf'): print("\t No limit")
else: print("\t Cell volume = %s to %s pixels" %(minCellVolume,maxCellVolume))
print("Output cell name = %s " %outCellName)
print("Output directory = %s " %outDirectory)


#outFileName = segmentationFile + "original"
#createPIFfile(data,outFileName)
outFileName = segmentationFile.split("/")[-1]

if doCrop == False and doResize == False:
	if hmDim == 2: createPIFfile2D(data,outDirectory + "/" + outFileName,segmentationThreshold,outCellName) # original segmentation data
	if hmDim == 3: createPIFfile3D(data,outDirectory + "/" + outFileName,segmentationThreshold,outCellName) # original segmentation data


if doCrop:
	print("\nPerforming cropping...")
	
	if hmDim == 2:
		data, cropLowerLimits, cropUpperLimits = crop2D(data,cropDimensions,cropOrigin,segmentationThreshold)
		outFileName = outFileName + "_croped_from_" + str(cropLowerLimits[0]) + "-" + str(cropLowerLimits[1]) \
					+ "_to_" + str(cropUpperLimits[0]) + "-" + str(cropUpperLimits[1])
		createPIFfile2D(data,outDirectory + "/" + outFileName,segmentationThreshold,outCellName) # original segmentation data

	if hmDim == 3:
		data, cropLowerLimits, cropUpperLimits = crop3D(data,cropDimensions,cropOrigin,segmentationThreshold)
		outFileName = outFileName + "_croped_from_" + str(cropLowerLimits[0]) + "-" + str(cropLowerLimits[1]) + "-" + str(cropLowerLimits[2]) \
					+ "_to_" + str(cropUpperLimits[0]) + "-" + str(cropUpperLimits[1]) + "-" + str(cropUpperLimits[2])
		createPIFfile3D(data,outDirectory + "/" + outFileName,segmentationThreshold,outCellName) # original segmentation data
	
	print("\t done!")

if doResize:
	print("\nPerforming resizing...")
	outFileName = outFileName + "_resized_a_factor_" + str(round(1/resizeFactor,1))
	if hmDim == 2:
		data = resize2D(data,resizeFactor)
		createPIFfile2D(data,outDirectory + "/" + outFileName,0,outCellName) # data normalized to 1 or 0
	if hmDim == 3:
		data = resize3D(data,resizeFactor)
		createPIFfile3D(data,outDirectory + "/" + outFileName,0,outCellName) # data normalized to 1 or 0
	print("\t done!")

 
if doCluster:
	print("\nCreating cell lattice...")
	inputFileName = outFileName + ".pif"
	outFileName = outFileName + "_clustered_" + str(maxCellVolume) + ".pif"


	#replace cell type (string) to int to be read by cluster.cpp
	os.system("sed 's/%s/%s/g' %s > %s" %(outCellName,"1",outDirectory + "\/" + inputFileName,"pifToCluster.pif"))

	if maxCellVolume == float('inf'): maxCellVolume = "INT_MAX"
	os.system("sed 's/fMAXCLUSTERSIZE/%s/g' cluster.cpp > deleteme1.cpp" %(maxCellVolume))

	os.system("sed 's/fFILENAME/%s/g' deleteme1.cpp > deleteme2.cpp" %("pifToCluster.pif"))

	os.system("sed 's/fCELLNAME/%s/g' deleteme2.cpp > deleteme3.cpp" %(outCellName))

	os.system("sed 's/fMINCLUSTSIZE/%s/g' deleteme3.cpp > deleteme4.cpp" %(minCellVolume))

	#print(outDirectory + "\/" + outFileName)
	os.system("sed 's/fOUTFILENAME/%s/g' deleteme4.cpp > runCluster.cpp" %(outDirectory + "\/" + outFileName))
	os.system("rm deleteme*")

	os.system("g++ -o runCluster runCluster.cpp")
	os.system("./runCluster")
	os.system("rm pifToCluster.pif")

	print("\t done!")


# create files for TOPAS simulation (Geometry, Scoring) and ImageCube file with the cell lattice
inFileName = outDirectory + "/" + outFileName
outFileName = inFileName[:-4]
dimensions = np.shape(data)
if hmDim == 2: dimensions = [np.shape(data)[0],np.shape(data)[1],1]

createTOPASFiles(inFileName,outFileName,dimensions)
