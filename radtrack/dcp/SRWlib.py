# Timur Shaftan
# Library -- input of SRW files

class SRW:
     """This class implements SRW datasets."""
     def __init__(self):
          #initialize data storage variables
          self.description = [""]
          self.parameterName = []
          self.columnName = []
          self.parameterDefinition = []
          self.columnDefinition = []
          self.parameterData = []
          self.columnData = []

def SRWFileRead1(self,IFileName,MaxNumParam):
    Npar=0
    Ncol=0
    k=0
    f=open(IFileName,"r",0) 
    for line in f.readlines(): # read into line.
        if k == 0:
            self.columnName = line.split(':')[0].split(',')       
        k+=1
#        print "%d %s" %(k,line)
        if line.find("#") == 0: 
            if line.find("#",1,MaxNumParam) <= 0: #check if srw or not  
                self.Description=line
#                print "legend"
            elif line.find("#",1,MaxNumParam) >= 0: 
#                print "parameter"
                Npar=Npar+1
#                print "%d %s" %(k,line)                
                self.parameterData.append(float(line[1:line.find("#",1,MaxNumParam)]))
                self.parameterName.append(line[line.find("#",1,MaxNumParam)+1:MaxNumParam])
        else:
#            print "value"
            Ncol=Ncol+1
            self.columnData.append([value for value in line.split()])
    self.columnData=zip(*self.columnData)
    return self
    f.close()

def SRWFileRead(IFileName,MaxNumParam):
    Npar=0
    Ncol=0
    k=0
    coln=[]
    parn=[[] for x in xrange(2)]
    f=open(IFileName,"r",0) 
    for line in f.readlines(): # read into line.       
        k=k+1
#        print "%d %s" %(k,line)
        if line.find("#") == 0: 
            if line.find("#",1,MaxNumParam) <= 0: #check if srw or not  
                Legend=line
#                print "legend"
            elif line.find("#",1,MaxNumParam) >= 0: 
#                print "parameter"
                Npar=Npar+1
#                print "%d %s" %(k,line)                
                parn[0].append(float(line[1:line.find("#",1,MaxNumParam)]))
                parn[1].append(line[line.find("#",1,MaxNumParam)+1:MaxNumParam])
#                parn.append()
        else:
#            print "value"
            Ncol=Ncol+1
#            coln.append(float(line))
            coln.append([value for value in line.split()])
#            coln.append([0 for x in xrange(Ncol)])
#            coln[kc][:]=words[:]
#        if k>20:
#            break
    return (Npar,Ncol,parn,coln,Legend)
    f.close()