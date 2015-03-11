# Timur Shaftan
# input of the SDDS beam parameters through RadTrack interface

import string 
import os

class BP:
    def __init__(self):
        self.ex=0       #emittance, m rad
        self.enx=0      #norm emittance, m rad
        self.betax=0    #Twiss beta, m
        self.alphax=0   #Twiss alpha
        self.etax=0     #Dispersion, m
        self.etaxp=0    #Dispersion derivative
        self.ey=0       
        self.eny=0
        self.betay=0
        self.alphay=0
        self.etay=0
        self.etayp=0
        self.Sx=0       #rms beam sizes, length, spread
        self.Sxp=0
        self.Sy=0
        self.Syp=0
        self.St=0
        self.Sdelta=0
        self.pAverage=0 #Average mopmentum, eV/c?
        self.el=0
        self.ecx=0      #corrected emittance with dispersion substracted
        self.ecnx=0     #and corresponding Twiss parameters
        self.betacx=0
        self.alphacx=0
        self.ecy=0
        self.ecny=0
        self.betacy=0
        self.alphacy=0
        self.Cx=0       #Centroid positions in all 6D
        self.Cxp=0
        self.Cy=0
        self.Cyp=0
        self.Ct=0
        self.Cdelta=0
        self.pCentral=0
        self.Charge=0   #Charge, C
        self.Particles=0 # Num of particles
        self.gamma = 1
        self.current = 0

def BPsdds2srw(IFileName, PFileName,BPN):
    TempFile="6Dtxt.txt"
    if os.path.isfile(TempFile):
        os.remove(TempFile)
    try:        # convert output file to txt format
        os.system("sddsprintout -spreadsheet=csv -column=* " + IFileName + " "+TempFile)
        Key6D=1
    except ValueError: ## if sdds barks: could not make this work yet!!!
        Key6D=0
        words=[]
        print "not 6D phase space file"            
    if Key6D & os.path.isfile(TempFile): # if this is really 6D sdds file:
        cont=[[0 for x in xrange(7)] for x in xrange(1)] 
        f=open(TempFile,"r",0)
        if os.stat(TempFile).st_size==0: # check the file size
            words="zero-length file"
            sys.exit("zero-length file") 
        else:
            try:
                for line in f.readlines(): # read into line.
                    words = line.split(" ")
                    cont[0][:]=words[:]
            except ValueError:
                sys.exit("not 6D phase space file") 
 #      print words[0][:]
        f.close()       
        #file is proven to be output sdds file with non-0 volume of sdds data
        #now ready to sddsanalyze
        os.system("sddsanalyzebeam " + IFileName + " " + TempFile) 
        #now convert beam parameter file from sdds to txt
        os.system("sddsprintout -spreadsheet=csv -column=* " +TempFile+ " " + PFileName)
        
        # and read it
        ff=open(PFileName,"r",0)
        BP=[[0 for x in xrange(60)] for x in xrange(2)] 
        k=0
        for bline in ff.readlines():  
            bplines = bline.split(",")
#            print bplines
#            print "!"
            k=k+1
            if k==1:
                BP[0]=bplines
            else:
                BP[1]=bplines
        
        #filling out the beam parameter array defined as a class BP
        BPN.ex=BP[1][1]        #emittance, m rad
        BPN.enx=BP[1][2]      #norm emittance, m rad
        BPN.betax=BP[1][3]    #Twiss beta, m
        BPN.alphax=BP[1][4]   #Twiss alpha
        BPN.etax=BP[1][5]     #Dispersion, m
        BPN.etaxp=BP[1][6]    #Dispersion derivative
        BPN.ey=BP[1][7]       
        BPN.eny=BP[1][8]
        BPN.betay=BP[1][9]
        BPN.alphay=BP[1][10]
        BPN.etay=BP[1][11]
        BPN.etayp=BP[1][12]
        BPN.Sx=BP[1][13]       #rms beam sizes, length, spread
        BPN.Sxp=BP[1][14]
        BPN.Sy=BP[1][15]
        BPN.Syp=BP[1][16]
        BPN.St=BP[1][17]
        BPN.Sdelta=BP[1][18]
        BPN.pAverage=BP[1][19] #Average mopmentum, eV/c?
        BPN.el=BP[1][20]
        BPN.ecx=BP[1][21]      #corrected emittance with dispersion substracted
        BPN.ecnx=BP[1][22]     #and corresponding Twiss parameters
        BPN.betacx=BP[1][23]
        BPN.alphacx=BP[1][24]
        BPN.ecy=BP[1][25]
        BPN.ecny=BP[1][26]
        BPN.betacy=BP[1][27]
        BPN.alphacy=BP[1][28]
        BPN.Cx=BP[1][29]       #Centroid positions in all 6D
        BPN.Cxp=BP[1][31]
        BPN.Cy=BP[1][34]
        BPN.Cyp=BP[1][38]
        BPN.Ct=BP[1][43]
        BPN.Cdelta=BP[1][49]
        BPN.pCentral=BP[1][57]
        BPN.Charge=BP[1][58]   #Charge, C
        BPN.Particles=BP[1][59] # Num of particles
        ff.close()
    else:
        words=["Not a valid SDDS 6D phase space input"]
    if os.path.isfile(TempFile):
        os.remove(TempFile)
    return (words)

#main portion of the code
#x = BP()        #assign x as container for BP class
# prior calculation in DCP left 6D phas space saved into sdds file atto.out
#words=BPsdds2srw("atto.out", "BP.txt",x)        #fill out variable x
#print x.pCentral        #check that the data has been transmitted into variable x
