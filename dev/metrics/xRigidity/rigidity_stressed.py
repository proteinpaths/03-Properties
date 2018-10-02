#!/usr/bin/python

USAGE = "\
Calculates the Stressed Regions of a protein using FIRST rigity analysis program\n\
USAGE: rigidity_stressed.py <PDB structure>\n"

import os, sys
import subprocess

#sys.stderr = open ("errors.log", "w")
#sys.stdin = open ("errors.log", "w")
###############################################################################
# Function to be called by a external program
###############################################################################
def eval (pdbFilename, tmpDir=""):
	(path, filename) = os.path.split (pdbFilename)
	if (path==""): 
		pdbFilenameFull = "%s/%s" % (os.getcwd(), filename)
	else:
		pdbFilenameFull = pdbFilename

	if tmpDir == "":
		tmpDir = "tmp"+os.path.basename (pdbFilenameFull).split(".")[0]

	createDir (tmpDir)
	logFilename = tmpDir + "/" + name (pdbFilenameFull) + "_analysis.log"

	cmm = "proflex -nonf -h %s 2>&1 errors.log" % pdbFilenameFull
	[err, out]=subprocess.Popen (cmm.split(), cwd=tmpDir, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

	if not os.path.exists (logFilename):
		results = [-1,-1,-1]
	else:
		output = err.split ("\n")
		[degrees, clusters, stressed] = [-999999, -999999, -999999]
		for line in output:
			if "degrees" in line:
				degrees = float (line.split()[0])
			if "clusters" in line:
				clusters = float (line.split()[0])
			if "stress" in line:
				stressed = float (line.split()[0])

			results = [degrees, clusters, stressed]

	clean ([tmpDir])
	return (stressed)


#------------------------------------------------------------------
# Utility to create a directory safely.
# If it exists it is renamed as old-dir 
#------------------------------------------------------------------
def createDir (dir):
	if dir == ".": return

	def checkExistingDir (dir):
		if os.path.lexists (dir):
			headDir, tailDir = os.path.split (dir)
			oldDir = os.path.join (headDir, "old-" + tailDir)
			if os.path.lexists (oldDir):
					checkExistingDir (oldDir)

			os.rename (dir, oldDir)
	checkExistingDir (dir)
	os.system ("mkdir %s" % dir)

###############################################################################
# Print a message to the error output stream
###############################################################################
def log (message):
	string=">>> RdGy: "
	if (type (message) != list): 
		string +=  str (message)
	else: 
		for i in message: string += str (i) + " "
	
	sys.stderr.write (string+"\n")

###############################################################################
# Returns the stem BASENAME  of a relative or full name with some extension
###############################################################################
def name (namefile):
	baseName = os.path.basename (namefile)
	newNamefile = baseName.split(".") [0]

	return newNamefile

###############################################################################
# Remove temporal filenames used for calculations
###############################################################################
def clean (listOfTmpFiles):
	for tmpFile in listOfTmpFiles:
		os.system ("rm -r " + tmpFile)


##################################################################
# MAIN
##################################################################
if __name__ == "__main__":
	if len (sys.argv) < 2:
		print USAGE
		sys.exit (0)

	pdbFilename = sys.argv [1]

	print eval (pdbFilename)

