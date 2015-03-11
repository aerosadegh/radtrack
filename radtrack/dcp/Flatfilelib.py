# Timur Shaftan
# Library -- Input of flat files
# Separator = space between numbers in FF
# It can be space, "#", ",",... 

import numpy as np
from radtrack.dcp.Servicelib import is_number

class FF:
     """This class implements Flat File datasets."""
     def __init__(self):
          self.columnData = []
          self.description = [""]
          self.parameterName = []
          self.columnName = []
          self.parameterDefinition = []
          self.columnDefinition = []
          self.parameterData = []

def FFColRead(self,FFileName, MaxNumColum):
    IFileTypeName="ff"
    with open(FFileName,"r",0) as f:
        for line in f: # read into line.
            self.columnData.append(line.split())
        self.columnData=zip(*self.columnData)
        NEcol=np.shape(self.columnData)[0]
        Ncol=np.shape(self.columnData)[1]
        for i in xrange(0,NEcol):
            for j in xrange(0,Ncol):
                a=self.columnData[i][j]
                if not is_number(a):
                    print "not a Flat File"
                    IFileTypeName="nf"
                    break
    return (self, IFileTypeName)
    
def FFColRead1(FFileName, MaxNumColum):
    f=open(FFileName,"r") 
    for line in f.readlines(): # read into line.
        words = line.split()
    print np.shape(words)[0]
    Ncol=np.shape(words)
    NEcol=np.shape(words)
    coln=1
    f.close()
    return (coln,Ncol,NEcol)
    
