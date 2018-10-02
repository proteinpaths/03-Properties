#!/usr/bin/python

"""
Return the total void volume in a protein. It uses the 'avp' program.
It uses a default probe of 0.5 Angstrom

AUTHOR: Luis Garreta
DATE: Dic 06/2010

"""
USAGE  = "Return the total void volume in a protein. It uses the 'avp' program\n"
USAGE += "USAGE	:  voids-avp.py <pdb filename>\n"
USAGE += "INPUT	:  the pdb filename\n"
USAGE += "OUTPUT: The total void volume of the protein"

import sys, os
import subprocess
###############################################################################
# Print a message to the error output stream
###############################################################################
def log (message):
	string=">>> Voids: "
	for i in message:
		string += str (i) + " "
	
	sys.stderr.write (string+"\n")

###############################################################################
# Returns the stem BASENAME  of a relative or full name with some extension
###############################################################################
def name (namefile):
	baseName = os.path.basename (namefile)
	newNamefile = baseName.split(".") [0]

	return newNamefile

##################################################################
# Delete temporal files created during the process
##################################################################
def clean (listOfFiles):
	for file in listOfFiles:
		os.system ("rm " + file)

###############################################################################
# Main function executing, processing and returning the command result
###############################################################################
def eval (pdbFilename, tmpDir=""):
	
	(path, filename) = os.path.split (pdbFilename)
	pdbFilenameFull = pdbFilename
	if (path==""): 
		pdbFilenameFull = "%s/%s" % (os.getcwd(), filename)

	if tmpDir == "":
		tmpDir = "./"
		#tmpDir = "tmp"+os.path.basename (pdbFilenameFull).split(".")[0]

	cmm = "avp -q -r %s" % pdbFilenameFull
	[out, err]=subprocess.Popen (cmm.split(), cwd=tmpDir, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

	listOfLines = out.split("\n")
	totalValues = listOfLines [-3].split ()
	totalVoids = totalValues [-1]

	#clean ([outFilename, logFilename])

	return totalVoids

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

##################################################################
# MAIN
##################################################################
if __name__ == "__main__":

	if len (sys.argv) < 2: 
		print USAGE
		sys.exit (0)

	pdbFilename = sys.argv[1]

	out = eval (pdbFilename)
	print out 

