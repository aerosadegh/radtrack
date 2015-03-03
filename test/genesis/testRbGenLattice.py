__author__ = 'swebb'

from RadTrack.genesis.RbGenLattice import GenLattice
from matplotlib import pyplot as plt

# A simple FODO cell

my_lattice = GenLattice()

f = 3 #meters

lquad = 0.05
kq = 1/(f*lquad)
ldrift1 = 1.
ldrift2 = 1.2

pos = 0.
my_lattice.add_quadrupole(kq, pos, lquad)
pos += lquad
my_lattice.add_drift(pos, ldrift1)
pos += ldrift1
my_lattice.add_quadrupole(-kq, pos, lquad)
pos += lquad
my_lattice.add_drift(pos, ldrift2)
pos += ldrift2
my_lattice.add_quadrupole(-kq, pos, lquad)
pos += lquad
my_lattice.add_drift(pos, ldrift1)
pos += ldrift1
my_lattice.add_quadrupole(kq, pos, lquad)
pos += lquad

betax, alphax, betay, alphay, transfermap = my_lattice.compute_beamline()

print u'\u03B2_x =', betax
print u'\u03B2_y =', betay
print u'\u03B1_x =', alphax
print u'\u03B1_y =', alphay
print 'transfer map =\n', transfermap

betax, betay, s = my_lattice.compute_beta_func()

print u'\u03B2_x =', betax
print u'\u03B2_y =', betay
print 's =', s

plt.plot(s, betax, c='r', label=u'\u03B2_x')
plt.plot(s, betay, c='g', label=u'\u03B2_y')
plt.legend()
plt.tight_layout()
plt.show()