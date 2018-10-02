#!/usr/bin/python
import sasa_polar
import sasa_nonpolar

print (sasa_polar.eval ("native-2JOF.pdb"))
print (sasa_nonpolar.eval ("native-2JOF.pdb"))
