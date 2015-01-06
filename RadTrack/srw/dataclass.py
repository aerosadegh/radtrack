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

class laser:
    def __init__(self):
        laser.lambda0 = None
        laser.w0 = None
        laser.w0z = None
        laser.zR = None

class UP:
     def __init__(self): #index?? in precis too??
        UP.numPer = []
	UP.undPer = []
	UP.Bx = []
	UP.By = []
	UP.phBx = []
	UP.phBy = []
	UP.sBx = []
	UP.sBy = []
	UP.xcID = []
	UP.ycID = []
	UP.zcID = []

class Precis:

     def __init__(self):
        Precis.meth = [] 
        Precis.relPrec = [] 
        Precis.zStartInteg = [] 
        Precis.zEndInteg = [] 
        Precis.npTraj = [] 
        Precis.useTermin = [] 
        Precis.sampFactNxNyForProp = []
