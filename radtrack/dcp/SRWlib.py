# Timur Shaftan
# Library -- input of SRW files

class SRW:
    """This class implements SRW datasets."""
    def __init__(self, IFileName, MaxNumParam):
        #initialize data storage variables
        self.description = [""]
        self.parameterName = []
        self.columnName = []
        self.parameterDefinition = []
        self.columnDefinition = []
        self.parameterData = []
        self.columnData = []

        with open(IFileName,"r",0) as f:
            for k, line in enumerate(f): # read into line.
                if k == 0:
                    self.columnName = line.split(':')[0].split(',')       

                if line.find("#") == 0: 
                    if line.find("#",1,MaxNumParam) <= 0: #check if srw or not  
                        self.Description=line
                    elif line.find("#",1,MaxNumParam) >= 0: 
                        self.parameterData.append(float(line[1:line.find("#",1,MaxNumParam)]))
                        self.parameterName.append(line[line.find("#",1,MaxNumParam)+1:MaxNumParam])
                else:
                    self.columnData.append([float(value) for value in line.split()])
            self.columnData=zip(*self.columnData)
