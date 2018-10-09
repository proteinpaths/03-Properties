#!/usr/bin/python

USAGE  = "Calculate the number of hydrogen bonds using the hbpluss tool\n"
USAGE += "USAGE: hbonds.py <PDB structure> [outputFilename]\n"

import os, sys
import subprocess

###############################################################################
# Function to be called by a external program
###############################################################################
def eval (pdbFilename, workingDir=r"/dev/shm/tmp"):
	
	tmpDir = "%s/tmp_%s" % (workingDir,  os.path.basename (pdbFilename).split(".")[0])
	createDir (tmpDir)

	out, err = subprocess.Popen (["hbplus", pdbFilename], cwd=tmpDir, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
	outputLines = out.split("\n")

	strValue = outputLines[-2].split ()[0]
	value = float (strValue)

	clean ([tmpDir])
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
# Remove temporal filenames used for calculations
###############################################################################
def clean (listOfTmpFiles):
	for tmpFile in listOfTmpFiles:
		os.system ("rm -r " + tmpFile)

#-------------------------------------------------------------
# Print a message to the error output stream
#-------------------------------------------------------------
def log (message):
	string=">>> HBonds: "
	if type (message) != list:
		string +=  str (message)
	else:
		for i in message: string += str (i) + " "
	
	sys.stderr.write (string+"\n")

#-------------------------------------------------------------
# MAIN
# call a external programm that returns a value running on "workingDir"
#-------------------------------------------------------------
if __name__ == "__main__":

	workingDir = ""
	if len (sys.argv) < 2: 
		print USAGE
		sys.exit (0)
	elif len (sys.argv) == 3:
		workingDir  = sys.argv[2]
	else:
		workingDir = os.getcwd ()

	pdbFilename = sys.argv[1]

	print (eval (pdbFilename, workingDir))

