# -*- coding: utf-8 -*-
import numpy as np
import scipy.integrate
import scipy.special

def IDWaveLengthPhotonEnergy(nh,lam_u,Bx,By,Gam):	
	Ky=0.934*Bx*lam_u*100
	Kx=0.934*By*lam_u*100
	if (Kx<=2) or (Ky<=2):
		lam_r1=lam_u/2/Gam/Gam*(1+Kx*Kx/2+Ky*Ky/2) #m
		lam_rn=lam_r1/nh
		e_phn=1.2407002E-6/lam_r1/nh #eV
		w_or_id='yes'
	else:
		lam_rn=0
		e_phn=0
		w_or_id='no'
	return (Kx,Ky,lam_rn,e_phn,w_or_id) #w_or_id='yes' if K<2
	
def CriticalEnergyWiggler(Bx,Gam,Kx):
	#This only works for the case of a planar ID
	if (Kx>=2):		
		E_c=665.0255*Bx*Gam*0.511E9*Gam*0.511E9 #eV
		w_or_id='yes'
	else:
		E_c=0
                w_or_id='no'	
	return (E_c,w_or_id) #w_or_id='yes' if K>2

def RadiatedPowerPlanarWiggler(lam_u,Bx,N_u,Gam,I_b):
	#This only works for the case of a planar ID
	L_id=N_u*lam_u
	P_W=1265.382/2*L_id*I_b*(Gam*0.511E-3)*(Gam*0.511E-3)*Bx*Bx #Watts
	return (P_W, L_id) #w_or_id='yes' if K<>2
	
def CentralPowerDensityPlanarWiggler(Bx,N_u,Gam,I_b):
	#This only works for the case of a planar ID and zero emittance
	P_Wdc=10.85*N_u*I_b*(Gam/0.511E9)*(Gam*0.511E9)*Bx #W/mrad2
	return (P_Wdc) #w_or_id='yes' if K<>2

def UndulatorSourceSizeDivergence(lam_rn,L_id):
	#This only works for the case of a planar ID
	sig_r=1/4/3.1415*np.sqrt(lam_rn*L_id) #m
	sig_rp=np.sqrt(lam_rn/L_id)  #rad
	return (sig_r,sig_rp) #w_or_id='yes' if K<>2

def integrand(o, x):
	return kv(o, x)
	
def SpectralFLux(N_u,Gam,EEc,I_b,Kx):
	#This only works for the case of a planar ID
	if (Kx>=2):	
		modBes=scipy.integrate.quad(lambda x: scipy.special.kv(5.0/3.0, x),EEc,np.Inf)
#	print modBes
		I_s=2.458E10*2*N_u*I_b*Gam*0.511*EEc*modBes[0] #I[phot:=(sec mrad 0.1% BW)]
		w_or_id='yes'
	else:
		I_s=0
		w_or_id='no'
	return (I_s,w_or_id)