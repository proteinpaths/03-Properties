#!/usr/bin/python

USAGE  = "Calculate the structural similarity between structures using structural alphabets"
USAGE += "USAGE: structural.py <Target PDB >  <Reference PDB> [outputFilename]\n"

import os, sys

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
		if file[-1] == "/":
			os.system ("rmdir "+ file)
		else:	
			os.system ("rm " + file)
###############################################################################
## MAIN 
###############################################################################
alphabet = os.getenv ("EVAL_ALPHABET")
evalTmpDir = os.getenv ("EVAL_TMPDIR")

# CHECK ARGUMENTS 
if len (sys.argv) < 3:
	print USAGE
	sys.exit (0)
elif len (sys.argv) == 4:
	sys.stdout = open (sys.argv[3], "w")

pdbRef = sys.argv [1]
pdbTarget = sys.argv [2]

tmpDir = "%s/tmpSS_%s/" % (evalTmpDir, name (pdbTarget))
os.system ("mkdir %s" % tmpDir)

# Load the alphabet

# Process the reference 
outputRef = "%s/tmp-%s.output" % (tmpDir, name (pdbRef))
logRef = "%s/tmp-%s.log" % (tmpDir, name (pdbRef))

params = {"IN": pdbRef, "ALPHABET": alphabet, "OUT": outputRef, "LOG": logRef }
cmm2 =  "encoder -g -F %(IN)s -A %(ALPHABET)s -T l -O %(OUT)s &> %(LOG)s" % params
#print (cmm2)
os.system (cmm2)

# Process the target 
outputTarget = "%s/tmp-%s.output" % (tmpDir, name (pdbTarget))
logTarget = "%s/tmp-%s.log" % (tmpDir, name (pdbTarget))

params = {"IN": pdbTarget, "ALPHABET": alphabet, "OUT": outputTarget, "LOG": logTarget }
cmm1 =  "encoder -g -F %(IN)s -A %(ALPHABET)s -T l -O %(OUT)s &> %(LOG)s" % params
#print (cmm1)

os.system (cmm1)

# Get the outputs
encodeTarget = open (outputTarget).readlines()[2]
encodeRef = open (outputRef).readlines()[2]

# Evaluate the similarity
equals = len (filter (lambda x:x[0]==x[1], zip (encodeTarget, encodeRef)))
proportion = equals / float (len (encodeRef))

# Clean temporary files
clean ([outputTarget, outputRef, logTarget, logRef, tmpDir])
print proportion

