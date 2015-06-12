# -*- coding: utf-8 -*-
# version where we do not check wiggler or undulator
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import copy

import numpy as np
import scipy.integrate
import scipy.special

def IDWaveLengthPhotonEnergy(lam_u,Bx,By,Gam):
    Ky=0.934*Bx*lam_u*100
    Kx=0.934*By*lam_u*100
    lam_r=lam_u/2/Gam/Gam*(1+Kx*Kx/2+Ky*Ky/2) #m
    e_ph=1.2407002E-6/lam_r #eV
    return Kx,Ky,lam_r,e_ph

def CriticalEnergyWiggler(Bx,By,Gam):
    E_c=665.0255*(Bx*Bx+By*By)*Gam*0.511E-3*Gam*0.511E-3 #eV
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

def multi_particle(params):
    """Perform multiparticle analytical calc.

    Args:
        params (dict): input

    Returns:
        dict: copy of `params` and results
    """
    res = copy.deepcopy(params)
    v = IDWaveLengthPhotonEnergy(
        params['Period Length'],
        #TODO(robnagler) Why is this not res['Bx']?
        0,
        params['Vertical Magnetic Field'],
        params['Relativistic Energy (gamma)'],
    )
    res.update(zip(('Kx', 'Ky', 'lam_rn', 'e_phn'), v))
    v = RadiatedPowerPlanarWiggler(
        params['Period Length'],
        #TODO(robnagler) Why is this not res['Bx']?
        params['Vertical Magnetic Field'],
        params['Number of Periods'],
        params['Relativistic Energy (gamma)'],
        params['Average Current'],
    )
    res.update(zip(('P_W', 'L_id'), v))
    res['E_c'] = CriticalEnergyWiggler(
        params['Vertical Magnetic Field'],
        params['Horizontal Magnetic Field'],
        params['Relativistic Energy (gamma)'],
    )
    res['P_Wdc'] = CentralPowerDensityPlanarWiggler(
        params['Vertical Magnetic Field'],
        params['Number of Periods'],
        params['Relativistic Energy (gamma)'],
        params['Average Current'],
    )
    v = UndulatorSourceSizeDivergence(
        res['lam_rn'],
        res['L_id'],
    )
    res.update(zip(('RadSpotSize', 'RadSpotDivergence'), v))
    res['SpectralFluxValue'] = SpectralFLux(
        params['Number of Periods'],
        params['Relativistic Energy (gamma)'],
        1,
        params['Average Current'],
        res['Kx'],
    )
    res['RadBrightness'] = SpectralCenBrightness(
        params['Number of Periods'],
        params['Relativistic Energy (gamma)'],
        params['Average Current'],
    )
    res['lam_rn_3'] = res['lam_rn'] / 3.0
    res['lam_rn_5'] = res['lam_rn'] / 5.0
    res['e_phn_3'] = res['e_phn'] / 3.0
    res['e_phn_5'] = res['e_phn'] / 5.0
    return res
