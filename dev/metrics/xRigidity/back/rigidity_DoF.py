#!/usr/bin/python

USAGE = "\
Calculates the Degrees of Freedom of a protein using FIRST rigity analysis program\n\
USAGE: rigidity_degrees_freedom.py <PDB structure>\n"
import os, sys
import subprocess

#sys.stderr = open ("errors.log", "w")
#sys.stdin = open ("errors.log", "w")
#sys.stdout = open ("out.log", "w")
###############################################################################
# Function to be called by a external program
###############################################################################
def eval (pdbFilename, tmpDir="."):

	createDir (tmpDir)
	logFilename = tmpDir + "/" + name (pdbFilename) + "_analysis.log"

	cmm = "proflex -nonf -h %s 2>&1 errors.log" % pdbFilename
	out=subprocess.Popen (cmm.split(), cwd=tmpDir, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

	results = open (logFilename).readlines()
	value = -999999
	for line in results:
		if "degrees" in line:
			value = float (line.split()[0])

	#clean ([logFilename])
	return (value)

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

	print eval (pdbFilename, "test")

