#!/usr/bin/python
"""
It reconstruct a set of pdb files using "pulchra"
INPUT: 1. input dirname
       2. output dirname
OUTPUT: a new dir with the new reconstructed pdbs
"""

import os, sys
import subprocess

USAGE = "Reconstruct proteins with only CAs using pulchra\n"
USAGE+= "USAGE: prog.py <inputDir> <outputDir>\n"

def main ():
	args = sys.argv
	if (len (args) < 3):
		print USAGE
		quit()

	inDir    = args [1]
	outDir   = args [2]

	checkExistingDir (outDir)

	cmmStr = "pulchra %s/%s"
	files = ["%s/%s" % (inDir,x) for x in os.listdir (inDir) if ".pdb" in x]

	for pdb in files:
		cmm = cmmStr % (os.getcwd(), pdb)
		print (cmm)
		[err, out]=subprocess.Popen (cmm.split(), cwd=outDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		print (err)

		name = os.path.basename (pdb).split (".")[0]
		rebuildName = "%s/%s.rebuilt.pdb" % (inDir, name) 
		newName = "%s/%sr.pdb" % (outDir, name)

		print ("rename %s %s" % (rebuildName,  newName))
		os.rename (rebuildName, newName)

	

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
