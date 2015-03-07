"""
This is a test of the various undulator implementations to make sure they
return the correct answers

moduleauthor:: Stephen Webb <swebb@radiasoft.net
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

__author__ = 'swebb'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "1.0"
__email__ = "swebb@radiasoft.net"

failed = False

try:

    print 'testing undulator fields... '
    from RadTrack.fields.RbIdealPlanarUndulator \
        import RbIdealPlanarUndulator as planarUndulator
    import numpy as np

    tol = 1.e-8

    lambda_w = 0.025 # [cm]
    B0 = 1.25 # [T]
    r = np.array([0.01, -0.005, 2.72, -0.01, 0.007, 3.51]).reshape(2,3)
    myplanarundulator = planarUndulator(B0, lambda_w)
    B = myplanarundulator.evaluateBField(r, 0.)
    expectedB = np.array([ 0., 0.38627124, 0., 0., -1.01127124,
                           0.]).reshape(2,3)
    bError = B[:] - expectedB[:]
    error = 0.
    for idx in range(2):
        error += np.dot(bError[idx], bError[idx])\
                 /np.dot(expectedB[idx], expectedB[idx])

    print 'Ideal planar undulator test error:'
    print 'Berror =', error

    if error > tol:
        print 'B failed tolerances with B =', B, ', Expected:', expectedB
        failed = True

    if failed:
        raise Exception('testUndulatorFields has failed')


except Exception as e:
    print e
    raise

print 'Passed.'