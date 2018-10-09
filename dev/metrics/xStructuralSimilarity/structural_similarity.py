#!/usr/bin/python

USAGE  = "Calculate the structural similarity between structures using structural alphabets"
USAGE += "USAGE: structural.py <Target PDB >  <Reference PDB> [outputFilename]\n"

import os, sys, subprocess

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

params = {"IN": pdbRef, "ALPHABET": alphabet, "OUT": outputRef}
cmm =  "encoder -g -F %(IN)s -A %(ALPHABET)s -T l -O %(OUT)s" % params
out1,err1 = subprocess.Popen (cmm.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=tmpDir).communicate()

# Process the target 
outputTarget = "%s/tmp-%s.output" % (tmpDir, name (pdbTarget))
logTarget = "%s/tmp-%s.log" % (tmpDir, name (pdbTarget))

params = {"IN": pdbTarget, "ALPHABET": alphabet, "OUT": outputTarget}
cmm =  "encoder -g -F %(IN)s -A %(ALPHABET)s -T l -O %(OUT)s" % params
out2,err2 = subprocess.Popen (cmm.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=tmpDir).communicate()

# Get the outputs
encodeTarget = open (outputTarget).readlines()[2]
encodeRef = open (outputRef).readlines()[2]

# Evaluate the similarity
equals = len (filter (lambda x:x[0]==x[1], zip (encodeTarget, encodeRef)))
proportion = equals / float (len (encodeRef))

# Clean temporary files
clean ([outputTarget, outputRef, tmpDir])
print proportion

