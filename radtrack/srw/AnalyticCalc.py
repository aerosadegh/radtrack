# -*- coding: utf-8 -*-
# version where we do not check wiggler or undulator
import numpy as np
import scipy.integrate
import scipy.special

#cd radtrack
#git pull
#it will look for the git directory

#C:\d from old\RadiaBeam\RadSoft\radtrack>python radtrack\radtrack_gui.py


def IDWaveLengthPhotonEnergy(lam_u,Bx,By,Gam):	
    Ky=0.934*Bx*lam_u*100
    Kx=0.934*By*lam_u*100
    lam_r=lam_u/2/Gam/Gam*(1+Kx*Kx/2+Ky*Ky/2) #m
    e_ph=1.2407002E-6/lam_r #eV
    return (Kx,Ky,lam_r,e_ph) 
	
def CriticalEnergyWiggler(Bx,By,Gam):		
    E_c=665.0255*(Bx*Bx+By*By)*Gam*0.511E-3*Gam*0.511E-3 #eV
#    print Bx
    return (E_c) 

def RadiatedPowerPlanarWiggler(lam_u,Bx,N_u,Gam,I_b):
    #This only works for the case of a planar ID
    L_id=N_u*lam_u
    P_W=1265.382/2*L_id*I_b*(Gam*0.511E-3)*(Gam*0.511E-3)*Bx*Bx #Watts
    return (P_W, L_id) 
	
def CentralPowerDensityPlanarWiggler(Bx,N_u,Gam,I_b):
    #This only works for the case of a planar ID and zero emittance
    P_Wdc=10.85*N_u*I_b*(Gam*0.511E-3)*(Gam*0.511E-3)*Bx #W/mrad2
    return (P_Wdc)

def UndulatorSourceSizeDivergence(lam_rn,L_id):
    #This only works for the case of a planar ID
    sig_r=np.sqrt(lam_rn*L_id/2)/2/3.1415 #m
    sig_rp=np.sqrt(lam_rn/L_id/2)  #rad
    return (sig_r,sig_rp)

def integrand(o, x):
    return kv(o, x)
	
def SpectralFLux(N_u,Gam,EEc,I_b,Kx):
    #This only works for the case of a planar ID
    modBes=scipy.integrate.quad(lambda x: scipy.special.kv(5.0/3.0, x),EEc,np.Inf)
    I_s=2.458E10*2*N_u*I_b*Gam*0.511*EEc*modBes[0] #I[phot/(sec mrad 0.1% BW)]
    return (I_s)

def SpectralCenBrightness(N_u,Gam,I_b):
    #This only works for the case of a planar ID	
    I_s=1.325E10*2*N_u*I_b*1E-3*Gam*0.511E0*Gam*0.511E0*1.45 #I[phot/(sec mrad2 0.1% BW)]
    return (I_s)
