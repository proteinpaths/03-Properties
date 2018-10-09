#!/usr/bin/python

"LOG: updated oct 02/2018"

import os, sys
import tarfile       # For extractTrajectory function
import subprocess    # For runProgram function
from multiprocessing import Pool # For MultiProcessing Class For Multiprocessing

"""
Evaluate diferent metrics (as scripts) to a single pathway or
a directory of pathways
"""
USAGE = "eval01_main.py <-f|-d> <single pathway|dir of pathways> <output dir> <nCpus>"
TMPDIR    = os.environ ["EVAL_TMPDIR"]
LOGFILE   = os.environ ["EVAL_LOGFILE"]
ERRFILE   = os.environ ["EVAL_ERRFILE"]

#-----------------------------------------------------------
#-----------------------------------------------------------
def main (args):
	if len (args) < 3:
		print ">", USAGE
		sys.exit (0)
		
	if args [1] == "-f":
		fullPathwayName = args [2]
		print "Single path", fullPathwayName
		outputDir = args [3]
		nCpus     = int (args [4])
		evalSinglePathway (fullPathwayName, outputDir, nCpus)
	elif args [1] == "-d":
		inputDirPathways = args [2]
		outputDir   = args [3]
		nCpus       = int (args [4])
		evalDirPathways (inputDirPathways, outputDir, nCpus)

#-----------------------------------------------------------
# Evaluates the 11 properties to a single pathway (.tgz)
#-----------------------------------------------------------
def evalSinglePathway_Start (args):
	evalSinglePathway (*args)

def evalSinglePathway (fullPathwayName, outputDir, nCpus=1):
	print ">>> Evaluating properties on %s ..." % fullPathwayName
	#headersOutputFile  = "PDB NC CO RG HB SP SN RM LR SC SA RD RC RS" 
	headersOutputFile  = "PDB NC CO RG HB SP RM LR SC SA SS RD" 
	#headersOutputFile = "PDB NC CO RG HB AS RM LR RC RA DF SS"

	#tmpDir, refPdbFullpath = extractTrajectoryFromTgz (fullPathwayName, outputDir)
	tmpDir, refPdbFullpath, inputFiles = extractTrajectoryFromDir (fullPathwayName, outputDir)

	params = zip (inputFiles, [refPdbFullpath]*len (inputFiles))

	pool = Pool (processes=nCpus)
	results = pool.map (evalSinglePdbFile_Star, params)

	# Write to file
	resultsFilename = "%s/%s.values" % (outputDir, extractName (fullPathwayName))
	resultsFile = open (resultsFilename, "w")
	resultsFile.write ("\t".join (headersOutputFile.split()) + "\n")

	for row in results:
		resultsFile.write (row + "\n")
	resultsFile.close ()

	#os.system ("rm -rf %s &" % tmpDir)
#-----------------------------------------------------------
#-----------------------------------------------------------
def evalSinglePdbFile_Star (args):
	return evalSinglePdbFile (*args)

def evalSinglePdbFile (pdbFileFullpath, refPdbFullpath):
	valuesList = [extractName (pdbFileFullpath)]

	cmm = 'native_contacts %s %s' % (refPdbFullpath, pdbFileFullpath)
	valuesList.append (executeCommand (cmm))
	cmm = "contact_order %s" % pdbFileFullpath
	valuesList.append (executeCommand (cmm))
	cmm = "radius_gyration %s" % pdbFileFullpath
	valuesList.append (executeCommand (cmm))
	cmm = "hydrogen_bonds %s %s" % (pdbFileFullpath, TMPDIR)
	valuesList.append (executeCommand (cmm))
	cmm = "sasa_polar %s" % pdbFileFullpath
	valuesList.append (executeCommand (cmm))
	#cmm = "sasa_nonpolar %s" % pdbFileFullpath
	#valuesList.append (executeCommand (cmm))
	cmm = 'rmsd %s %s' % (refPdbFullpath, pdbFileFullpath)
	valuesList.append (executeCommand (cmm))
	cmm = 'local_rmsd %s %s' % (refPdbFullpath, pdbFileFullpath)
	valuesList.append (executeCommand (cmm))
	cmm = 'secondary_structures_correct %s %s' % (pdbFileFullpath, refPdbFullpath)
	valuesList.append (executeCommand (cmm))
	cmm = 'secondary_structures_any %s' % (pdbFileFullpath)
	valuesList.append (executeCommand (cmm))
	cmm = 'structural_similarity %s %s' % (refPdbFullpath, pdbFileFullpath, )
	valuesList.append (executeCommand (cmm))
	cmm = 'rigidity_degrees %s' % (pdbFileFullpath)
	valuesList.append (executeCommand (cmm))
	#cmm = 'rigidity_clusters %s' % (pdbFileFullpath)
	#valuesList.append (executeCommand (cmm))
	#cmm = 'rigidity_stressed %s' % (pdbFileFullpath)
	#valuesList.append (executeCommand (cmm))
	#cmm = 'voids %s' % (pdbFileFullpath)
	#valuesList.append (executeCommand (cmm))

	return "\t".join (valuesList)

#-----------------------------------------------------------
#-----------------------------------------------------------
def evalDirPathways (inputDirPathways, outputDir, nCpus=1):
	checkExistingDir (outputDir)
	os.mkdir (outputDir)

	inputFiles = sorted ([x for x in os.listdir (inputDirPathways) if ".tgz" in x])
	inputFilesFullPath = ["%s/%s" % (inputDirPathways, x) for x in inputFiles]

	for fullPath in inputFilesFullPath:
		evalSinglePathway (fullPath, outputDir, nCpus)

	"""
	params = zip (inputFilesFullPath, [outputDir]*len (inputFiles))
	pool = Pool (processes=nCpus)
	pool.map (evalSinglePathway_Start, params)
	pool.close ()
	pool.join ()
	"""


#-----------------------------------------------------------
# Get the native protein filename and the dir of PDBs
# Then make limks of the PDBs to a temporal dir
# Returns the temporal dir and the native names
#-----------------------------------------------------------
def extractTrajectoryFromDir (fullPathwayName, outputDir):
	pathwayName = extractName (fullPathwayName)
	tmpDir = "%s/tmp_pdbs_%s" % (outputDir, pathwayName)
	pdbsDir, nativeProtein, inputFiles = "", "", []
	nativeProtein = ""

	# Create outputDir
	checkExistingDir (tmpDir)

	# Make links of pdbs in a temporal Dir
	# There are only 2 files in dir: native and pdbs
	pdbFiles = os.listdir (fullPathwayName)
	pdbFiles.sort()
	nativeProtein = pdbFiles.pop()

	inputFile = []
	for pdb in pdbFiles:
		source = "%s/%s" % (fullPathwayName, pdb)
		dest   = "%s/%s" % (tmpDir, pdb)
		os.symlink (source, dest)
		inputFiles.append (dest)

	refPdbFullpath = "%s/%s" % (fullPathwayName, nativeProtein )

	return tmpDir, refPdbFullpath, inputFiles
#-----------------------------------------------------------
# Extract the conformations (Pdbs) of the trajectory and
# get the starting and reference (ending) pdbs.
# NOTE: Assumes that pathway is preprocessed (parasol or antom)
#-----------------------------------------------------------
def extractTrajectoryFromTgz (fullPathwayName, outputDir):
	pathwayName = extractName (fullPathwayName)
	tmpDir = "%s/tmp_pdbs_%s" % (outputDir, pathwayName)

	tar = tarfile.open (fullPathwayName, "r|gz")
	tar.extractall (path=tmpDir)

	refPdbFullpath = "%s/%s" % (tmpDir, tar.getnames ()[-1])

	return tmpDir, refPdbFullpath


#------------------------------------------------------------
# call a external programm that returns a value running on "workingDir"
#------------------------------------------------------------
def executeCommand (cmm, workingDir="./"):
	print ">>> %s" % cmm
	#try:
	value = subprocess.Popen (cmm.split (), cwd=workingDir, stdout=subprocess.PIPE).communicate()[0]
	print ">>>>", value
	formatedValue = "%1.4f" % float (value.strip()) 
	return formatedValue
	#except:
	#	log(["runProgram Error:"] + cmm.split())

#-------------------------------------------------------------
# Print a message to the error output stream
#-------------------------------------------------------------
def log (message):
	string=">>> PropEval: "
	if (type (message) != list): 
		string +=  str (message)
	else: 
		for i in message: string += str (i) + " "
	
	sys.stderr.write (string+"\n")

#----------------------------------------------------------------------
# Move dir to old-dir. Used when a directory exists.
#----------------------------------------------------------------------
def checkExistingDir (dir):
	if os.path.lexists (dir):
		headDir, tailDir = os.path.split (dir)
		oldDir = os.path.join (headDir, "old-" + tailDir)
		if os.path.lexists (oldDir):
			checkExistingDir (oldDir)

		os.rename (dir, oldDir)
	os.mkdir (dir)
#------------------------------------------------------------
# Extract only the name without path and extension
#------------------------------------------------------------
def extractName (fullName):
	return os.path.splitext (os.path.basename (fullName))[0]

#------------------------------------------------------------
# MAIN
#------------------------------------------------------------

if __name__ == "__main__":
	main (sys.argv)

