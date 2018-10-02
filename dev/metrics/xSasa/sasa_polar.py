#!/usr/bin/python

USAGE = "Calculates the accessible surface area  for the polar residues of a protein estructure (PDB)\n\
USAGE= sasa_polar.py <PDB file>"

import sys, os
import subprocess

###############################################################################
# Function to be called by a external program
###############################################################################
def eval (pdbFilename, workingDir="./"):
	output = subprocess.Popen (["freesasa", pdbFilename], cwd=workingDir, stdout=subprocess.PIPE).communicate()[0]
	outputLines = output.split("\n")

	value = -999999
	for line in outputLines:
		if  "Polar" in line:
			
			value = float (line.split (":")[1])
			break

	return (value)

###############################################################################
# MAIN
# call a external programm that returns a value running on "workingDir"
##################################################################
if __name__ == "__main__":

	if len (sys.argv) < 2: 
		print USAGE
		sys.exit (0)

	pdbFilename = sys.argv[1]
	outputDir = os.getcwd ()

	print (eval (pdbFilename, outputDir))

