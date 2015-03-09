"""
emPusherTest tests the s-based Boris integrator against a constant
electromagnetic field.

moduleauthor:: Stephen Webb <swebb@radiasoft.net
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'swebb'

# dummy class for returning a constant E- and B-field that should yield
# E X B drift

import numpy as np
import scipy.constants as consts


class constEM:

    def __init__(self):
        self.E = 1.e-5*np.array([2., 0., 0.])
        self.B = 1.e-5*np.array([0., 1., 0.])

    def getEField(self, x):
        return self.E

    def getBField(self, x):
        return self.B

try:

    print 'Testing Lorentz force pushers... '

    from radtrack.ptclmovers.RbBorisVay import RbBorisVay
    from PtclTests import PtclTests
    pusher = RbBorisVay(consts.e, consts.m_e, 1.e-8)
    ptclGamma = 101.  # make a particle with gamma = 101. v in y direction
    ptclu = consts.c*np.sqrt(ptclGamma**2 - 1.)
    x = [np.array([1., 0., 0.])]
    v = [np.array([0., ptclu, 0.])]
    fields = constEM()
    efield = [fields.getEField(x)]
    bfield = [fields.getBField(x)]

    expectedX = np.array([1.00000000e+00,   2.99777763e+00,   1.51624746e-16])
    expectedU = np.array([3.51764015e-02,   3.02775541e+10,   3.06281988e-06])
    tol = 1.e-8

    # Sequence tests the implementation of drift-kick-drift 2nd order
    # integrator scheme. This makes sure x and v are synchronous in time at
    # the end of the simulation
    # half move forward
    x = pusher.halfmove(v, x, 1)
    # full accelerate and move
    u = pusher.accelerate(v, efield, bfield)
    x = pusher.move(v, x)
    # half move backward
    x = pusher.halfmove(v, x, -1)

    failed = False
    xerror = x[0] - expectedX
    uerror = u[0] - expectedU
    metricX = np.dot(xerror, xerror)/np.dot(expectedX, expectedX)
    metricV = np.dot(uerror, uerror)/np.dot(expectedU, expectedU)

    print 'BorisVay pusher test error:'
    print 'Xerror =', metricX
    print 'Verror =', metricV

    if metricX > tol:
        print 'X failed tolerances with x =', x, ', Expected:', expectedX
        failed = True

    if metricV > tol:
        print 'V failed tolerances with v =', u, ', Expected:', expectedU
        failed = True

    if failed:
        raise Exception('emPusherTest has failed')

except Exception as e:
    print e
    raise

print 'Passed.'



