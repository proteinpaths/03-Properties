#!/usr/bin/python

USAGE  = "Calculate the number of hydrogen bonds using the hbpluss tool\n"
USAGE += "USAGE: hbonds.py <PDB structure> [outputFilename]\n"

import os, sys
import subprocess

###############################################################################
# Function to be called by a external program
###############################################################################
def eval (pdbFilename, workingDir="./"):
	output = subprocess.Popen (["hbplus", pdbFilename], cwd=workingDir, stdout=subprocess.PIPE).communicate()[0]
	outputLines = output.split("\n")

	strValue = outputLines[-2].split ()[0]
        value = float (strValue)

	return (value)

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

	if len (sys.argv) < 2: 
		print USAGE
		sys.exit (0)

	pdbFilename = sys.argv[1]
	outputDir = os.getcwd ()

	print (eval (pdbFilename, outputDir))

