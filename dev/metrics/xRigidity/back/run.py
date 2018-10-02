import os, sys

files = ["in20000/"+x for x in os.listdir ("in20000")]

for f in files:
	cmm = "rigidity_analysis.py $PWD/%s" % f
	os.system (cmm)
