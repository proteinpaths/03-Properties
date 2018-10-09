#! /usr/bin/python 

import os, sys, subprocess
import uuid

"""
LOG:
	2016/12/16:  Added handle of stderr messages
"""

USAGE = "\
GOAL:   Calculates the local RMSD of a reference PDB vs. query PDB (Average of SS).\n\
INPUT:  Reference PDB and query PDB.\n\
OUTPUT: Average RMSD of secondary structures. \n\
USAGE:  local_rmsd.py <reference PDB> <query PDB> [workingDir] \n"


#-------------------------------------------------------------
# Main 
#-------------------------------------------------------------
def main (args):
	if len (args) < 3:
		print USAGE
		sys.exit (0)
	elif len (args) == 4:
		workingDir = args [3]
	else:
		workingDir = "."

	referencePDB = args [1]
	targetPDB    = args [2]

	localRmsdValue = localRmsd (referencePDB, targetPDB, workingDir)
	print localRmsdValue

#-------------------------------------------------------------
# Calculate the local RMSD
#-------------------------------------------------------------
def localRmsd (refPDB, targetPDB, workingDir):
	#matchPdb = matchResidueNumbering (targetPDB, refPDB)
	refInfo = getAminoStructureInfo (refPDB, workingDir)
	refStructures = getLocalStructures (refInfo["aminoStructure"], refInfo["startResidueNumber"])
	localRmsdValue = calculateAverageRmsd (refPDB, targetPDB, refStructures)

	#clean ([matchPdb])
	return localRmsdValue


###############################################################################
# Call external rmsd 
###############################################################################
def rmsd (refPDB, targetPDB, start, end):
	#cmm = "rmsd.R %s %s %s %s" % (targetPDB, refPDB, start, end)
	cmm = "rmsd -l %s:%s %s %s" % (start, end, refPDB, targetPDB)
	value = runProgram (cmm, ".")
	return float (value)

###############################################################################
# Call external dssp 
###############################################################################
def calculateDssp (pdbFilename, workingDir):
	TMPLABEL = "tmp_LR_%s_" % str (uuid.uuid4())
	TMPLABEL    += extractName (pdbFilename) + "_"

	stemName = name (pdbFilename)
	dsspFilename = TMPLABEL + stemName + ".dssp"
	cmm = "dssp %s %s" % (pdbFilename, dsspFilename)
	out,err = subprocess.Popen (cmm.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=workingDir, ).communicate()

	return dsspFilename

###############################################################################
# Calculate the DSSP of "PDB" structure and get from it information:
# sequence A+B, start residue number, end residue number and size of the sequence
###############################################################################
def getAminoStructureInfo (PDB, workingDir):
	dsspName = calculateDssp (PDB, workingDir)
	dsspFile = open (dsspName)
	# Skips header lines until reach the values of aminos and structures and others
	while "#" not in dsspFile.next():
		None

	# Starts to copy the amino and its corresponding structure. It ASSUMES that "always"
	# both amino and the structue will be in the positions 13, 16 respectivelly.
	sequenceOfAlphaBeta = ""
	start = ""
	for line in dsspFile:
		if start == "":
			start = line.split ()[1]

		structure = line [16]

		if structure in ['H','G','I']:
			sequenceOfAlphaBeta += 'H'
		elif structure in ['B','E']:
			sequenceOfAlphaBeta += 'B'
		else:
			sequenceOfAlphaBeta += 'C'
	
	end = line.split ()[1]

	info = {}
	info ["aminoStructure"] = sequenceOfAlphaBeta
	info ["startResidueNumber"] = int (start)
	info ["endResidueNumber"] = int (end)
	info ["ziseOfSequence"] = len (sequenceOfAlphaBeta)

	clean ([dsspName])
	return info

###############################################################################
# Get a substructure from a sequence "seq" that starts in the position "pos"
###############################################################################
def getSubStructure (struct, pos, seq, lstStructs, startResidueNumber):
	start = pos 
	pos += 1
	nextStruct = seq [pos]
	size = len (seq)
	while pos < size  and nextStruct == struct: 
		pos += 1
		nextStruct = seq [pos]

	end = pos + 1
	pos -= 1
	lstStructs.append ((start+startResidueNumber-1, end+startResidueNumber-1))

	return pos

###############################################################################
# Get local structures from "aminoStructure" sequence starting in a "startResidueNumber"
# When it detects a starting SS, it calls the getSubStructure 
###############################################################################
def getLocalStructures (aminoStructure, startResidueNumber):
	position=0
	structure=""
	listOfStructures = []
	sizeStructure = len (aminoStructure)
	while position < sizeStructure:
		structure = aminoStructure [position]

		if structure in ["H", "B"]:
			position = getSubStructure (structure, position, aminoStructure, listOfStructures, startResidueNumber)

		position += 1

	return listOfStructures

###############################################################################
# Match the residue numbering of a reference PDB to a query PDB
###############################################################################
def matchResidueNumbering (targetPDB, refPDB):
	matchPdb = "%s_%s_%s_%s" % (TMPLABEL,extractName(targetPDB),extractName(refPDB),"_match.pdb")
	cmm = "convpdb.pl -match %s %s > %s" % (targetPDB, refPDB, matchPdb)
	os.system (cmm)

	return matchPdb
	
###############################################################################
# 
###############################################################################
def calculateAverageRmsd (refPdb, matchPdb, listOfStructures):
	listOfRmsds =[]

	sumRmsd = 0
	sumSizes = 0.0001
	for s in listOfStructures:
		start = int (s[0])
		end = int (s[1])
		sizeStructure = end - start + 1

		rmsdValue = rmsd (refPdb, matchPdb, start, end) * sizeStructure

		sumRmsd += rmsdValue
		sumSizes += sizeStructure

	if sumSizes == 0:
		totalRmsd = 9999
	else:
		totalRmsd = sumRmsd / float (sumSizes)

	return totalRmsd

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
	
###############################################################################
# Print a message to the error output stream
###############################################################################
def log (message):
	string=">>> LRMSD: "
	if type (message) != list:
		string +=  str (message)
	else:
		for i in message: string += str (i) + " "
	
	sys.stderr.write (string+"\n")

#------------------------------------------------------------
# Extract only the name without path and extension
#------------------------------------------------------------
def extractName (fullName):
	return os.path.splitext (os.path.basename (fullName))[0]

#-------------------------------------------------------------
# Define the  output for errors and log messages
#-------------------------------------------------------------
def defineMessagesOutput ():
	stderr = os.getenv ("EVAL_STDERR")
	if stderr == None:
		sys.stderr = sys.stdout
	else:
		sys.stderr = open (stderr, "a")

###############################################################################
# call a external programm that returns a value running on "workingDir"
###############################################################################
def runProgram (command, workingDir):
	commandLst = command.split()
	(out, err) = subprocess.Popen (commandLst, cwd=workingDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	return out

###############################################################################
# Main
###############################################################################
if __name__ == "__main__":
	defineMessagesOutput ()
	main (sys.argv)


