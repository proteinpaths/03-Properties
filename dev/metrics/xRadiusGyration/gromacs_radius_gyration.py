#!/usr/bin/python

USAGE = "\
Returns the radius of gyration for a protein using the gromacs g_gyrate (opt. 1)\n\
USAGE: radiusg.py <PDB structure>\n"

import os, sys

##################################################################
# RUN
##################################################################
def run (pdbFilename):
	PDBStructure = pdbFilename
	xvgFilename = name (pdbFilename) + "-rg-tmp.xvg"

	command = "echo 1 | gmx gyrate -f %s -s %s -o %s > /dev/null 2>&1 " % (PDBStructure, PDBStructure, xvgFilename)
	os.system (command)

	results = open (xvgFilename).readlines()
	radiusOfGyration = -1

	lastLine = results [-1]
	values = lastLine.split()

	radiusOfGyration = float (values [1])

	clean ([xvgFilename])
	return radiusOfGyration

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
		os.system ("rm " + tmpFile)


##################################################################
# MAIN
##################################################################
if __name__ == "__main__":
	if len (sys.argv) < 2:
		print USAGE
		sys.exit (0)

	pdbFilename = sys.argv [1]

	print run (pdbFilename)

