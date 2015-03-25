"""
Test script for the Genesis lattice generation and simulation execution
modules using the Tesla Test Facility lattice. This lattice has segmented
undulators and external focusing, making it an ideal test.
"""

__author__ = 'swebb'

from radtrack.genesis.RbGenLattice import GenLattice
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rc('text', usetex=True)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 18}

mpl.rc('font', **font)
import numpy as np
from scipy import constants as consts
from radtrack.genesis.rbExecuteGenesis import rbExecuteGenesis

# A doublet cell

my_lattice = GenLattice('ttf.lat')

gamma0 = 1956.947
emittance = 2.000000e-6 #2 mm-mrad
l_undulator = 2.73e-2
dBdx_quad = 37. #T/m
k_quadrupole = dBdx_quad*consts.e/(consts.m_e*gamma0*consts.c)
aw = 0.896
l_quad = 3*l_undulator
l_drift1 = 16*l_undulator
l_drift2 = 2*l_undulator
l_und_segment = 163*l_undulator
und_spacing = 26*l_undulator
n_cells = 6

pos = 0.
# add quads and undulators
for x in range(0, n_cells):
    my_lattice.add_undulator(0.896,pos, l_und_segment)
    pos += l_und_segment
    my_lattice.add_drift(pos, l_drift2)
    pos += l_drift2
    my_lattice.add_quadrupole(k_quadrupole, pos, l_quad)
    pos += l_quad
    my_lattice.add_drift(pos, l_drift1)
    pos += l_drift1
    my_lattice.add_quadrupole(-k_quadrupole, pos, l_quad)
    pos += l_quad
    my_lattice.add_drift(pos, l_drift2)
    pos += l_drift2

betax, alphax, betay, alphay, transfermap = my_lattice.compute_beamline()

print u'\u03B2_x =', betax
print u'\u03B2_y =', betay
#print u'<\u03B2_x> =', (2*ldrift1+ldrift2+4*lquad)/1.7
#print u'<\u03B2_y> =', (2*ldrift1+ldrift2+4*lquad)/1.25
print u'\u03B1_x =', alphax
print u'\u03B1_y =', alphay
print 'X radius =', np.sqrt(1.2e-6*betax/1202.5)
print 'Y radius =', np.sqrt(1.2e-6*betay/1202.5)
print 'transfer map =\n', transfermap

betax, betay, s = my_lattice.compute_beta_func()

#plt.plot(s, betax, c='r', label=r'$\beta_x$')
#plt.plot(s, betay, c='g', label=r'$\beta_y$')
#plt.ylabel(r'$\beta~\textrm{[m/rad]}$')
#plt.xlabel(r'$s~\textrm{[m]}$')
#plt.ylim([0., 1.5*max(betax)])
#plt.xlim([0., s[-1]])
#plt.legend()
#plt.tight_layout()
#plt.show()

my_lattice.export_genesis_lattice(l_undulator, gamma0)

run_genesis = rbExecuteGenesis()
run_genesis.execute_genesis('ttf.in')