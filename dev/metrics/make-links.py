#!/usr/bin/python

"""
Create links in the dev\bin directory using
the bin sources in each program dir
"""

import os

programLstLibs = []
programLstLibs.append ("freesasa/bin/freesasa")
programLstLibs.append ("hbplus/hbplus")
programLstLibs.append ("proflex/prog/first/bin/proflex")
programLstLibs.append ("dssp/dssp")
programLstLibs.append ("avp/avp")
programLstLibs.append ("encoder/encoder")

programLstUser = []
programLstUser.append ("xHydrogenBonds/hydrogen_bonds.py")
programLstUser.append ("xRadiusGyration/radius_gyration.pl")
programLstUser.append ("xSasa/sasa_polar.py")
programLstUser.append ("xSasa/sasa_nonpolar.py")
programLstUser.append ("xRigidity/rigidity_analysis.py")
programLstUser.append ("xRigidity/rigidity_degrees.py")
programLstUser.append ("xRigidity/rigidity_clusters.py")
programLstUser.append ("xRigidity/rigidity_stressed.py")
programLstUser.append ("xVoids/voids.py")
programLstUser.append ("xContactOrder/contact_order.pl")

programLstUser.append ("xRmsd/rmsd.pl")
programLstUser.append ("xLocalRmsd/local_rmsd.py")
programLstUser.append ("xNativeContacts/native_contacts.R")
programLstUser.append ("xSecondaryStructures/secondary_structures.py")
programLstUser.append ("xSecondaryStructures/secondary_structures_any.py")
programLstUser.append ("xSecondaryStructures/secondary_structures_correct.py")

programLstUser.append ("xStructuralSimilarity/structural_similarity.py")


currentDir = os.getcwd()

# Links for libs with original names
cmmPre="ln -fs %s/%s ../bin/%s" 
print ("Libs's program links")
for program in programLstLibs:
	cmm = cmmPre % (currentDir, program, os.path.basename (program))
	print (cmm)
	os.system (cmm)

print ("User's program links")
# Links for User programs modified without extensions
for program in programLstUser:
	shortname = program.split (".")[0]
	cmm = cmmPre % (currentDir, program, os.path.basename (shortname))
	print (cmm)
	os.system (cmm)
