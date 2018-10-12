#!/usr/bin/python

USAGE  = "Returns the proportion of amino acids in secondary structures of a PDB file.\n"
USAGE += "USAGE: python aminos_in_ss.py [-any|-correct] [reference pdb] <target pdb>\n"
"""
NOTES: Uses the DSSP program and processes its output 
	   It ASSUMES that always both amino and the structue will be in the positions 13, 16 respectivelly.
	   This assumption as it was impossible to split the line by a pattern as there are many empty values
"""
import os, sys
import subprocess
import uuid
TMPLABEL = "tmp_%s_" % str (uuid.uuid4 ())
##################################################################
# Delete temporal files created during the process
##################################################################
def clean (listOfFiles):
	for file in listOfFiles:
		os.system ("rm " + file)

###############################################################################
# Returns the stem BASENAME  of a relative or full name with some extension
###############################################################################
def name (namefile):
	baseName = os.path.basename (namefile)
	newNamefile = baseName.split(".") [0]

	return newNamefile

###############################################################################
# Return the stem name of a relative or full name with some extension
###############################################################################
#def name (namefile):
#	reverseNamefile = namefile [::-1]
#	pos = reverseNamefile.index (".")
#	newNamefile = reverseNamefile [pos+1:][::-1]

#	return newNamefile

###############################################################################
# Print a message to the error output stream
###############################################################################
def log (message):
	string=""
	for i in message:
		string += str (i) + " "
	
	sys.stderr.write (">>>> SecStr: " + string+"\n")

###############################################################################
# call a external programm that returns a value running on "workingDir"
###############################################################################
def calculateDssp (pdbFilename, workingDir):
	stemName = name (pdbFilename)
	dsspFilename = TMPLABEL + stemName + ".dssp"
	cmm = "dssp %s %s" % (pdbFilename, dsspFilename)
	out,err = subprocess.Popen (cmm.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=workingDir, ).communicate()

	return dsspFilename

###############################################################################
## 
###############################################################################
def processDSSP (dsspFilename):
	dsspFile = open (dsspFilename)

	# Skips header lines until reach the values of aminos and structures and others
	while "#" not in dsspFile.next():
		None

	# Starts to copy the amino and its corresponding structure. It ASSUMES that "always"
	# both amino and the structue will be in the positions 13, 16 respectivelly.
	seqAminos = ""
	seqStructures = ""
	seqAlphaBeta = ""

	for line in dsspFile:
		amino = line [13]
		seqAminos += amino

		structure = line [16]
		seqStructures += structure

		if structure in ["G", "H", "I"]:
			seqAlphaBeta += "A"
		elif structure in ["E", "B"]:
			seqAlphaBeta += "B"
		elif structure in ["T", "S"]:
			seqAlphaBeta += "O"
		else: 
			seqAlphaBeta += " "

	return seqAminos, seqStructures, seqAlphaBeta

###############################################################################
## 
###############################################################################
def getProportionAAinCorrectSS (referencePdbFilename, targetPdbFilename, workingDir):
	referenceDsspFilename = calculateDssp (referencePdbFilename, workingDir)
	targetDsspFilename = calculateDssp (targetPdbFilename, workingDir)

	refSeqAminos, refSeqStructures, refSeqAlphaBeta = processDSSP (referenceDsspFilename)
	trgSeqAminos, trgSeqStructures, trgSeqAlphaBeta = processDSSP (targetDsspFilename)

	numberOfCorrectSS = 0
	for pair in zip (refSeqAlphaBeta, trgSeqAlphaBeta):
		if pair [0] == pair [1] and pair [0] != " ":
			numberOfCorrectSS += 1

	allSS =  [x for x in refSeqAlphaBeta if x != " "]
	numberOfSS = len (allSS)

	proportionOfSS = numberOfCorrectSS / float (numberOfSS)

	clean ([referenceDsspFilename, targetDsspFilename])
	return proportionOfSS
	
###############################################################################
## 
###############################################################################
def getProportionAAinAnySS (targetPdbFilename, workingDir):
	targetDsspFilename = calculateDssp (targetPdbFilename, workingDir)

	trgSeqAminos, trgSeqStructures, trgSeqAlphaBeta = processDSSP (targetDsspFilename)

	numberOfAnySS = 0
	for aa in trgSeqAlphaBeta:
		if aa != " ":
			numberOfAnySS += 1

	allSS =  [x for x in trgSeqAlphaBeta if x != " "]
	numberOfSS = len (trgSeqAminos)

	proportionOfSS = numberOfAnySS / float (numberOfSS)

	clean ([targetDsspFilename])
	return proportionOfSS
	
###############################################################################
##
###############################################################################
if __name__ == "__main__": 
	try:
		referencePdbFilename, targetPdbFilename = "None", "None"
		if len (sys.argv) < 3:
			print USAGE
			sys.exit (0)
		
		proportion = -1
		workingDir = os.getcwd ()
		if sys.argv [1] == "-correct":
			referencePdbFilename = sys.argv [2]
			targetPdbFilename    = sys.argv [3]
			proportion = getProportionAAinCorrectSS (referencePdbFilename, targetPdbFilename, workingDir)
		elif sys.argv [1] == "-any":
			targetPdbFilename = sys.argv [2]
			proportion = getProportionAAinAnySS (targetPdbFilename, workingDir)

		print proportion
	except ZeroDivisionError:
		print 0
	except: 
		print ">>> Eval error in secondary_structures.py, parameters: ", referencePdbFilename, targetPdbFilename
		print e

