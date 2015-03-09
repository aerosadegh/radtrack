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

# A doublet cell

my_lattice = GenLattice('doublet_lattice.lat')

f = 1.1 #meters

lundulator = 2.27e-2

lquad = 2*lundulator
print 'lquad =', lquad
kq = 1/(f*lquad)
print 'kq =', kq
ldrift1 = 9*lundulator
print 'l =', ldrift1
ldrift2 = 90*lundulator
print 'L =', ldrift2

n_cells = 1

pos = 0.
for x in range(0, n_cells):
    my_lattice.add_quadrupole(kq, pos, lquad)
    pos += lquad
    #my_lattice.add_drift(pos, ldrift1)
    my_lattice.add_undulator(0.849, pos, ldrift1)
    pos += ldrift1
    my_lattice.add_quadrupole(-kq, pos, lquad)
    pos += lquad
    my_lattice.add_undulator(0.849, pos, ldrift2)
    pos += ldrift2
    my_lattice.add_quadrupole(-kq, pos, lquad)
    pos += lquad
    #my_lattice.add_drift(pos, ldrift1)
    my_lattice.add_undulator(0.849, pos, ldrift1)
    pos += ldrift1
    my_lattice.add_quadrupole(kq, pos, lquad)
    pos += lquad

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

plt.plot(s, betax, c='r', label=r'$\beta_x$')
plt.plot(s, betay, c='g', label=r'$\beta_y$')
plt.ylabel(r'$\beta~\textrm{[m/rad]}$')
plt.xlabel(r'$s~\textrm{[m]}$')
plt.ylim([0., 1.5*max(betax)])
plt.xlim([0., s[-1]])
plt.legend()
plt.tight_layout()
plt.show()

my_lattice.export_genesis_lattice(0.0227, 1202.5)