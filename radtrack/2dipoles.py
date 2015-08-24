# -*- coding: utf-8 -*-
"""Simulation of SR from 2 dipole edges

"""
from __future__ import absolute_import, division, print_function

from pykern.pkdebug import pkdc, pkdp
from pykern import pkarray

# Must be after srw_params import
import srwlib
from array import array
import uti_plot

# Initial coordinates of particle trajectory through the ID
part = srwlib.SRWLParticle()
part.x = 0.0 #beam.partStatMom1.x
part.y = 0.0 #beam.partStatMom1.y
part.xp = 0.0 #beam.partStatMom1.xp
part.yp = 0.0 #beam.partStatMom1.yp
part.gamma = 0.060/0.51099890221e-03 #Relative Energy beam.partStatMom1.gamma #
part.z = 0.0 #zcID #- 0.5*magFldCnt.MagFld[0].rz
part.relE0 = 1 #Electron Rest Mass
part.nq = -1 #Electron Charge
    
L_bend=0.3
L_drift=0.5
bend1=srwlib.SRWLMagFldM(_G=1.0, _m=1, _n_or_s='n', _Leff=L_bend, _Ledge=0.1)
drift1 = srwlib.SRWLMagFldM(_G=0.01,_m=1, _n_or_s='n', _Leff=L_drift) #Drift
"""
       :param _G: field parameter [T] for dipole, [T/m] for quadrupole (negative means defocusing for x), [T/m^2] for sextupole, [T/m^3] for octupole
        :param _m: multipole order 1 for dipole, 2 for quadrupoole, 3 for sextupole, 4 for octupole
        :param _n_or_s: normal ('n') or skew ('s')
        :param _Leff: effective length [m]
        :param _Ledge: "soft" edge length for field variation from 10% to 90% [m]; G/(1 + ((z-zc)/d)^2)^2 fringe field dependence is assumed
"""
print('OK1')

#arZero = array('d', [0]*3)
arZero = array('d', [0]*1)
#arZc = array('d', [-L_bend/2-L_drift/2, 0, L_bend/2+L_drift/2])
arZc = array('d', [0])
#magFldCnt = srwlib.SRWLMagFldC([bend1, drift1, bend1], arZero, arZero, arZc)
magFldCnt = srwlib.SRWLMagFldC([bend1], arZero, arZero, arZc)
"""
        :param _arMagFld: magnetic field structures array
        :param _arXc: horizontal center positions of magnetic field elements in arMagFld array [m]
        :param _arYc: vertical center positions of magnetic field elements in arMagFld array [m]
        :param _arZc: longitudinal center positions of magnetic field elements in arMagFld array [m]
"""
print('OK2')
arPrecPar = [2]  

#Definitions and allocation for the Trajectory waveform
# number of trajectory points along longitudinal axis
npTraj = 10001
partTraj = srwlib.SRWLPrtTrj()
print('OK3')
partTraj.partInitCond = part
partTraj.allocate(npTraj, True)
partTraj.ctStart = -0.15 #-0.55 * und.nPer * und.per
partTraj.ctEnd = 0.15 #0.55 * und.nPer * und.per #magFldCnt.MagFld[0].rz
print(partTraj)
print(magFldCnt)
partTraj = srwlib.srwl.CalcPartTraj(partTraj, magFldCnt, arPrecPar)
print('OK4')
ctMesh = [partTraj.ctStart, partTraj.ctEnd, partTraj.np]
for i in range(partTraj.np):
        partTraj.arX[i] *= 1000
        partTraj.arY[i] *= 1000
plots.append([
        uti_plot.uti_plot1d,
        partTraj.arX, ctMesh, ['ct [m]', 'Horizontal Position [mm]'],
    ])
plots.append([
        uti_plot.uti_plot1d,
        partTraj.arY, ctMesh, ['ct [m]', 'Vertical Position [mm]'],
    ])