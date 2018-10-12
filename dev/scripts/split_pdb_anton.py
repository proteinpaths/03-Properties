#!/usr/bin/python

# Given a multi pdb file (from anton) it splits in multiple files
# INPUT: 1. multi pdb filename 
#        2. prefix for each new filename
# OUTPUT: "pdbs" directory with the individual pdb files

import os, sys


def main ():
	print ("USAGE: prog.py <pdbFilename> <prefixFilename> <outDir>\n")
	args = sys.argv
	pdbFilename    = args [1]
	prefixFilename = args [2]
	outDir        = args [3]
	checkExistingDir (outDir)

	pdbsString = open (args [1]).read()
	pdbs = pdbsString.split ("END\n")
	print (pdbs[0])

	n = len (pdbs)
	nStr = len (str (n))+1

	for k, pdb in enumerate (pdbs):
		strCount = str (k+1)
		nameFull = "%s/%s%s.pdb" % (outDir, prefixFilename, strCount.zfill (nStr))
		pdbOut = open (nameFull, "w")
		pdbOut.write (pdbs [k])
		pdbOut.close ()

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
# MAIN
#------------------------------------------------------------

if __name__ == "__main__":
	main ()
