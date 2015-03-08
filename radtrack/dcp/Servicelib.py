# Timur Shaftan
# Library -- service functions

import string, sys 
import numpy as np

def IFileTypeCheck(IFileName):
    with open(IFileName,"r",0) as f:
        line = f.readline()
        if string.find(line,"SDDS1") == 0:
            return "sdds"
        elif string.find(line,"#") == 0:
            return "srw"
        elif is_number(line.split()[0]):
            return "ff"
        else:
            return "unknown"

def SDDSreshape(x,ColumnXAxis,ColumnPicked,NumPage):
    print np.shape(x.columnData)
    if len(np.shape(x.columnData)) < 3:
        sys.exit("Empty SDDS File")
    Npar=np.shape(x.parameterData)[0]
    Ncol=np.shape(x.columnData)[0]
    NElemCol=np.shape(x.columnData)[2]
    NPage=np.shape(x.columnData)[1]
    NcolPicked=len(ColumnPicked)
#    print x.columnData[1][0:2][0:10]
#    cmd="sddsprintout -spreadsheet=csv -spreadsheet=delimiter=#  \
#    -column=* " + IFileName + " " + CFileName
#    os.system(cmd) 
    for i in xrange(0,NcolPicked):
        if ColumnPicked[i] < Ncol and ColumnXAxis < Ncol and NumPage<NPage:
            FlagOK=1
        else:
            FlagOK=0
    if FlagOK==1: 
        if ColumnXAxis < 0:
            Xvec=[i for i in range(NElemCol)]
        else:
            Xvec=x.columnData[ColumnXAxis][NumPage][:]
        Yvec=[]
        YLab=[]
        for i in xrange(0,len(ColumnPicked)):
            Yvec.append(x.columnData[ColumnPicked[i]][NumPage][:])
            YLab.append(x.columnDefinition[ColumnPicked[i]])
        print np.shape(x.columnData)
        Xrvec=np.reshape(Xvec,-1,'C')
        Yrvec=np.reshape(Yvec,[len(ColumnPicked),NElemCol],'C')
    else:
        sys.exit("Input parameter exceeds the number of columns or pages")           
    return (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,NPage)
    
def SRWreshape(x,ColumnXAxis,ColumnPicked):
    print np.shape(x.columnData)
    Npar=np.shape(x.parameterData)[0]
    Ncol=np.shape(x.columnData)[0]
    NElemCol=np.shape(x.columnData)[1]
    NcolPicked=len(ColumnPicked)
    #print Npar
    #print Ncol
    #print NcolPicked
    for i in xrange(0,len(ColumnPicked)):
        if ColumnPicked[i] < Ncol and ColumnXAxis < Ncol:
            FlagOK=1
        else:
            FlagOK=0
    if FlagOK==1: 
        if ColumnXAxis < 0:
            Xvec=[i for i in range(NElemCol)]
        else:
            Xvec=x.columnData[ColumnXAxis][:]
        Yvec=[]
        for i in xrange(0,len(ColumnPicked)):
            Yvec.append(x.columnData[ColumnPicked[i]][:])
        print np.shape(Yvec)
    else:
        sys.exit("Input parameter exceeds the number of columns")
    return (Xvec,Yvec,Npar,Ncol,NcolPicked,NElemCol)
    
def FFreshape(x,ColumnXAxis,ColumnPicked):
    #print np.shape(x.columnData)
    Ncol=np.shape(x.columnData)[0]
    NElemCol=np.shape(x.columnData)[1]
    NcolPicked=len(ColumnPicked)
    #print Ncol
    #print NcolPicked
    for i in xrange(0,NcolPicked):
        if ColumnPicked[i] < Ncol and ColumnXAxis < Ncol:
            FlagOK=1
        else:
            FlagOK=0
    if FlagOK==1: 
        if ColumnXAxis < 0:
            Xvec=[i for i in range(NElemCol)]
        else:
            Xvec=x.columnData[ColumnXAxis][:]
        Yvec=[]
        for i in xrange(0,len(ColumnPicked)):
            Yvec.append(x.columnData[ColumnPicked[i]][:])
        print np.shape(Yvec)
    else:
        sys.exit("Input parameter exceeds the number of columns")
    return (Xvec,Yvec,Ncol,NcolPicked,NElemCol)

def column(matrix, i):  # separating column in a matrix
    return [row[i] for row in matrix]

def columnS(matrix, i,i1):  # separating columns in a matrix
    return [row[i:i1] for row in matrix]
        
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        print "Not a number"
        return False
