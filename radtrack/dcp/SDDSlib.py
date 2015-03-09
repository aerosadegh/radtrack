# Timur Shaftan
# Library -- input of SDDS files
import string 
import os

def SDDSconvert(IFileName, MaxNumParam, CFileName, PFileName):    
    Npar=0
    Ncol=0
    f=open(IFileName,"r",0) 
    for line in f.readlines(): # read into line.
        if string.find(line,"&column")>=0:
            Ncol=Ncol+1
        if string.find(line,"&parameter")>=0:
            Npar=Npar+1
#    print Npar
#    print Ncol
    f.seek(0)
    
    # read file info    
    Pname=["name", "symbol", "units", "description", "type"]
    i=0
    k=0
    NEMA=[[0 for x in xrange(5)] for x in xrange(MaxNumParam)] 
    for line in f.readlines():
        i=i+1
        if i>MaxNumParam-1:
            break
        if string.find(line,"&parameter")>=0:
            k=k+1
            for j in xrange(0,5):
                if string.find(line,Pname[j] +'=')>=0:
                    [U1,U2]=line.split(Pname[j] +'=')
                    [U4,U3]=U2.split(',',1)
                    NEMA[k][j]=U4            

    PmaxE=k
    PARS=[[0 for x in xrange(5)] for x in xrange(PmaxE)]
    PARS=NEMA[0:PmaxE][:]
    f.close()
    
    for k in xrange(0,PmaxE):
        print "%d %s " %(k, PARS[k][:])
    
    if Ncol>0:
        cmd="sddsprintout -spreadsheet=csv -spreadsheet=delimiter=% \
        -column=* " + IFileName + " " + CFileName
        os.system(cmd) 

    if Npar>0:
        cmd="sddsprintout -spreadsheet=csv -spreadsheet=delimiter=% \
        -parameters=* " + IFileName + " " + PFileName
        print "OK"
        os.system(cmd)
    return (Npar, Ncol)

def SDDSParRead(PFileName, Npar, MaxNumParam):    
    k=0
    kp=0
    f=open(PFileName,"r",0)
    parn=[[0 for x in xrange(Npar)] for x in xrange(1)] #allocate mem for column array
    if os.stat(PFileName).st_size==0: # check the file size
        words="no parameters"
    else:  
        for line in f.readlines(): # read into line.
            words = line.split("%")
            k=k+1
            if k>MaxNumParam: 
                break
            if kp==0: 
                parn[0][:]=words[:]
                kp=1
            else:
                parn.append([0 for x in xrange(2)])
                parn[kp][:]=words[:]
                kp=kp+1 
#            try:
#                print "%s %f" %(words[0],float(words[1]))
#            except ValueError:
#                print "%s %s" %(words[0],words[1]) 
    f.close()
    return (parn, kp)

def SDDSColRead(CFileName, Ncol, MaxNumColum):
    k=0 # this is the to do counter
    kc=0 # column counter
    coln=[[0 for x in xrange(Ncol)] for x in xrange(1)] #allocate mem for column array
    f=open(CFileName,"r",0) 
    for line in f.readlines(): # read into line.
        words = line.split("%")
        k=k+1
        if k>MaxNumColum: # limit the counter to max =1000
            break
        if len(words)==Ncol:
            if kc==0: # this is column input
                coln[0][:]=words[:]
#                print "%s %s %s %s" %(coln[0][0],coln[0][1],coln[0][2],coln[0][3])
                kc=1
            else:
                coln.append([0 for x in xrange(Ncol)])
                coln[kc][:]=words[:]
#                print "%s %s %s %s" %(coln[kc][0],coln[kc][1],coln[kc][2],coln[kc][3])
                kc=kc+1 
#    print kc # number of columns
    f.close()
    return (coln,kc)