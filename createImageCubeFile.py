import numpy as np

def createTOPASFiles(inFileName,outFileName,dimensions):

	DimX = dimensions[0]; DimY = dimensions[1]; DimZ = dimensions[2]

	cells = np.genfromtxt("%s" %inFileName,dtype='i,U25,i,i,i,i,i,i')
	cellID = []
	for cell in cells: 
		if cell[0] in cellID: continue
		cellID.append(cell[0])

	TOPASSocorerFile = open("TOPASScorerFile.txt",'w')
	
	TOPASSocorerFile.write('# scorers for each cell \n')
	TOPASSocorerFile.write('####################### \n')
	TOPASSocorerFile.write('# WARNING - replace "REPLACE_BY_Quantity" by a scoring quantity supported by TOPAS, e.g., "DoseToMedium" \n')
	TOPASSocorerFile.write('####################### \n')
	TOPASSocorerFile.write('s:Quantity_for_scoring = "REPLACE_BY_Quantity" \n')
	for cell in cellID:
		TOPASSocorerFile.write('s:Sc/Scorer_for_Cell_%s/Quantity = Quantity_for_scoring \n' %(cell))
		TOPASSocorerFile.write('s:Sc/Scorer_for_Cell_%s/Component = "Cell_lattice" \n' %(cell))
		TOPASSocorerFile.write('s:Sc/Scorer_for_Cell_%s/OutputType = "Binary" # replace by preferred file format \n' %(cell))
		TOPASSocorerFile.write('s:Sc/Scorer_for_Cell_%s/OutputFile = "Output_for_Cell_%s" \n' %(cell,cell))
		TOPASSocorerFile.write('s:Sc/Scorer_for_Cell_%s/IfOutputFileAlreadyExists = "Overwrite" \n' %(cell))
		TOPASSocorerFile.write('sv:Sc/Scorer_for_Cell_%s/OnlyIncludeIfInMaterial = 1 "Cell_%s" \n\n' %(cell,cell))

	TOPASSocorerFile.close()
	TOPASGeometryFile = open("TOPASGeometryFile.txt",'w')

	TOPASGeometryFile.write('# scorers for each cell \n')
	TOPASGeometryFile.write('####################### \n')
	TOPASGeometryFile.write('# WARNING - replace "REPLACE_BY_Directory" by the path where your ImageCube file is stored in your system" \n')
	TOPASGeometryFile.write('# WARNING - replace REPLACE_BY_pixel_size REPLACE_BY_unit by the pixel dimension and its units in your image" \n')
	TOPASGeometryFile.write('####################### \n')

	TOPASGeometryFile.write('s:Ge/Cell_lattice/Type = "TsImageCube" \n')
	TOPASGeometryFile.write('s:Ge/Cell_lattice/Parent = "World" \n')
	TOPASGeometryFile.write('s:Ge/Cell_lattice/ImagingToMaterialConverter = "MaterialTagNumber" \n')
	TOPASGeometryFile.write('s:Ge/Cell_lattice/InputDirectory = "REPLACE_BY_Directory" \n')
	TOPASGeometryFile.write('s:Ge/Cell_lattice/InputFile = "%s" \n' %(outFileName+".int16.bin")) 
	TOPASGeometryFile.write('i:Ge/Cell_lattice/NumberOfVoxelsX = %s \n' %(DimZ))
	TOPASGeometryFile.write('i:Ge/Cell_lattice/NumberOfVoxelsY = %s \n' %(DimY))
	TOPASGeometryFile.write('i:Ge/Cell_lattice/NumberOfVoxelsZ = %s \n' %(DimX))
	TOPASGeometryFile.write('d:Ge/Cell_lattice/VoxelSizeX = REPLACE_BY_pixel_size REPLACE_BY_unit \n')
	TOPASGeometryFile.write('d:Ge/Cell_lattice/VoxelSizeY = REPLACE_BY_pixel_size REPLACE_BY_unit \n')
	TOPASGeometryFile.write('d:Ge/Cell_lattice/VoxelSizeZ = REPLACE_BY_pixel_size REPLACE_BY_unit \n\n')
	
	TOPASGeometryFile.write('iv:Ge/Cell_lattice/MaterialTagNumbers = %s 0 ' %(len(cellID)+1))
	for cell in cellID:
		TOPASGeometryFile.write('%s ' %(cell))
	TOPASGeometryFile.write('\n\n')
	TOPASGeometryFile.write('sv:Ge/Cell_lattice/MaterialNames = %s "G4_WATER" ' %(len(cellID)+1))
	for cell in cellID:
		TOPASGeometryFile.write('"Cell_%s" ' %(cell))
	TOPASGeometryFile.write('\n\n')

	TOPASGeometryFile.write('\n')
	TOPASGeometryFile.write('# materials for each cell \n')
	TOPASGeometryFile.write('####################### \n')
	TOPASGeometryFile.write('# WARNING - it assumes all cells are water \n')
	TOPASGeometryFile.write('####################### \n')
	TOPASGeometryFile.write('sv:Ma/Cell_%s/Components = 2 "Hydrogen" "Oxygen" \n' %(cellID[0]))
	TOPASGeometryFile.write('uv:Ma/Cell_%s/Fractions  = 2 0.111894 0.888106 \n' %(cellID[0]))
	TOPASGeometryFile.write('d:Ma/Cell_%s/Density  = 1.0 g/cm3 \n' %(cellID[0]))
	TOPASGeometryFile.write('d:Ma/Cell_%s/MeanExcitationEnergy  = 78 eV \n' %(cellID[0]))
	TOPASGeometryFile.write('s:Ma/Cell_%s/DefaultColor = "lightblue" \n\n' %(cellID[0]))
	for cell in cellID[1:]:
		TOPASGeometryFile.write('b:Ma/Cell_%s/BuildFromMaterials = "True" \n' %(cell))
		TOPASGeometryFile.write('sv:Ma/Cell_%s/Components = 1 "G4_WATER"  \n' %(cell))
		TOPASGeometryFile.write('uv:Ma/Cell_%s/Fractions = 1 1.0  \n' %(cell))
		TOPASGeometryFile.write('d:Ma/Cell_%s/Density = Ma/Cell_%s/Density g/cm3 \n' %(cell,cellID[0]))
		TOPASGeometryFile.write('s:Ma/Cell_%s/DefaultColor = Ma/Cell_%s/DefaultColor \n\n' %(cell,cellID[0]))
	
	TOPASGeometryFile.close()
	
	cellLattice = np.zeros([DimZ, DimY, DimX])
	for cell in cells:
		cellLattice[cell[6],cell[4],cell[2]] = cell[0]
	cellLattice.astype('int16').tofile(outFileName+'.int16.bin')
