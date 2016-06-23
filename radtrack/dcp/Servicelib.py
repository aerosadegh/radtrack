# Timur Shaftan
# Library -- service functions

import numpy as np

def SDDSreshape(x,ColumnXAxis,ColumnPicked,NumPage):
    FlagOK=1
    if len(np.shape(x.columnData)) < 3:
        raise Exception('Empty SDDS File') 
    Npar=np.shape(x.parameterData)[0]
    Ncol=np.shape(x.columnData)[0]
    NElemCol=np.shape(x.columnData)[2]
    NPage=np.shape(x.columnData)[1]
    NcolPicked=len(ColumnPicked)

    for i in xrange(0,NcolPicked):
        if ColumnPicked[i] < Ncol and ColumnXAxis < Ncol and NumPage<NPage:
            FlagOK=1
        else:
            FlagOK=0
    if FlagOK==1: 
        if ColumnXAxis < 0:
            Xvec=range(NElemCol)
        else:
            Xvec=x.columnData[ColumnXAxis][NumPage][:]
        Yvec=[]
        YLab=[]
        for i in xrange(0,len(ColumnPicked)):
            Yvec.append(x.columnData[ColumnPicked[i]][NumPage][:])
            YLab.append(x.columnDefinition[ColumnPicked[i]])
        Xrvec=np.reshape(Xvec,-1,'C')
        Yrvec=np.reshape(Yvec,[len(ColumnPicked),NElemCol],'C')
    else:
        raise Exception("Input parameter exceeds the number of columns or pages")           

    return (Xrvec,Yrvec,YLab,Npar,Ncol,NcolPicked,NElemCol,NPage)
    
def SRWreshape(x,ColumnXAxis,ColumnPicked):
    Npar=np.shape(x.parameterData)[0]
    Ncol=np.shape(x.columnData)[0]
    NElemCol=np.shape(x.columnData)[1]
    NcolPicked=len(ColumnPicked)

    for i in xrange(0,len(ColumnPicked)):
        if ColumnPicked[i] < Ncol and ColumnXAxis < Ncol:
            FlagOK=1
        else:
            FlagOK=0
    if FlagOK==1: 
        if ColumnXAxis < 0:
            Xvec=range(NElemCol)
        else:
            Xvec=x.columnData[ColumnXAxis][:]
        Yvec=[]
        for i in xrange(0,len(ColumnPicked)):
            Yvec.append(x.columnData[ColumnPicked[i]][:])
    else:
        raise Exception("Input parameter exceeds the number of columns or pages")

    return (np.array(Xvec),np.array(Yvec),Npar,Ncol,NcolPicked,NElemCol)
    
def FFreshape(x,ColumnXAxis,ColumnPicked):
    Ncol=np.shape(x.columnData)[0]
    NElemCol=np.shape(x.columnData)[1]
    NcolPicked=len(ColumnPicked)

    for i in xrange(0,NcolPicked):
        if ColumnPicked[i] < Ncol and ColumnXAxis < Ncol:
            FlagOK=1
        else:
            FlagOK=0
    if FlagOK==1: 
        if ColumnXAxis < 0:
            Xvec=range(NElemCol)
        else:
            Xvec=x.columnData[ColumnXAxis][:]
        Yvec=[]
        for i in xrange(0,len(ColumnPicked)):
            Yvec.append(x.columnData[ColumnPicked[i]][:])
    else:
        raise Exception("Input parameter exceeds the number of columns or pages")

    return (Xvec,Yvec,Ncol,NcolPicked,NElemCol)

def column(matrix, i):  # separating column in a matrix
    return [row[i] for row in matrix]

def columnS(matrix, i,i1):  # separating columns in a matrix
    return [row[i:i1] for row in matrix]
