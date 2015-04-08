# SDDS file loader for the files with particle phase spaces
import numpy as np
import sys

import sdds

WorkingDir="..\..\Codes\Elegant\laserHeater\\"
DirFileName="laserheat.out"
IFileName=WorkingDir+DirFileName

x = sdds.SDDS(0)
x.load(IFileName)

print np.shape(x.columnData)
if len(np.shape(x.columnData)) < 3:
    sys.exit("Empty SDDS File")

Npar=np.shape(x.parameterData)[0]
Ncol=np.shape(x.columnData)[0]
NElemCol=np.shape(x.columnData)[2]
NPage=np.shape(x.columnData)[1]

print "Npage=",NPage
print "Ncol=",Ncol
print "Nelem=",NElemCol

print x.columnName

for i in xrange(0,Ncol):
	if x.columnName[i]=='x':
		X=x.columnData[i][0][:]
		print 'x'
	elif x.columnName[i]=='xp':
		XP=x.columnData[i][0][:]
	elif x.columnName[i]=='y':
		Y=x.columnData[i][0][:]
	elif x.columnName[i]=='yp':
		YP=x.columnData[i][0][:]
	elif x.columnName[i]=='t':
		T=x.columnData[i][0][:]
	elif x.columnName[i]=='p':
		P=x.columnData[i][0][:]
	elif x.columnName[i]=='particleID':
		ID=x.columnData[i][0][:]
	else:
		sys.exit("Input parameter exceeds the number of columns or pages")
print X[1:10]
sys.exit("end")
