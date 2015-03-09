"""
RbParticle Tracker is the generic class to handle particle-field
interactions in a very generic framework. The class should work for any
combination of particles, a single mover, and any combination of fields.

moduleauthor:: Stephen Webb <swebb@radiasoft.net
Copyright (c) 2014 RadiaBeam Technologies. All rights reserved
"""

import warnings

__author__ = 'swebb'
__copyright__ = "Copyright &copy RadiaBeam Technologies 2013, all rights " \
                "reserved"
__version__ = "0.1"
__email__ = "swebb@radiasoft.net"

class RbParticleTracker:

    def __init__(self, t0, dt):
        # Create the dictionaries to hold the particles & fields
        self.fielddict = {}
        self.ptcldict  = {}
        # Only one mover allowed!
        self.mover     = -1
        self.movername = 'noname'
        self.t0 = t0
        self.dt = dt


    def addField(self, fieldclass, fieldname):
        """
        Add a field class with a name as a string
        :param fieldclass:
        :param fieldname:
        :return:
        """
        if type(fieldname) != str:
            raise TypeError('field name', fieldname, 'must be a string type')

        if fieldname in self.fielddict.keys():
            msg = 'Replacing field', fieldname
        else:
            msg = 'Adding field', fieldname
        print msg
        self.fielddict[fieldname] = fieldclass


    def addPtcls(self, ptclclass, ptclname):
        """
        Add a particle class with a name as a string
        :param ptclclass:
        :param ptclname:
        :return:
        """
        if type(ptclname) != str:
            raise TypeError('field name', ptclname, 'must be a string type')

        if ptclname in self.fielddict.keys():
            msg = 'Replacing field', ptclname
        else:
            msg = 'Adding field', ptclname
        print msg
        self.fielddict[ptclname] = ptclclass


    def addMover(self, moverclass, movername):
        """
        Add a mover class
        :param moverclass: mover class
        :param movername: name assigned to mover
        :return:
        """
        if moverclass != -1:
            msg = '!Warning! the particle tracker can only support '\
                          'one particle mover.\n'
            msg += 'the current mover,', self.movername
            msg += ', is being replaced with', movername
            warnings.warn(msg)
        self.movername = movername
        self.mover = moverclass


    def initialize(self):
        """
        Begin the particle and field updates. Assumption is a
        time-staggered second order approach. This requires the particles
        be drifted half a time-step forward.
        :return:
        """
        for bunches in self.ptcldict.keys():
            self.mover.halfmove(bunches.momenta, bunches.position, +1)


    def finalize(self):
        """
        Finish the particle and field updates. Half-drift the particles
        backwards half a time step to get the right final positions
        :return:
        """
        for bunches in self.ptcldict.keys():
            self.mover.halfmove(bunches.momenta, bunches.positions, -1)



    def update(self):
        """
        Update the particle and field data
        :return:
        """
        # Currently supports set fields, so we need particles to update with
        #  the fields.
        for bunches in self.ptcldict.keys():
            sumEFields = np.zeros(bunches.nptcls*3).reshape(bunches.nptcls,3)
            sumBFields = np.zeros(bunches.nptcls*3).reshape(bunches.nptcls,3)
            for fields in self.fielddict.keys():
                sumEFields+=fields.evaluateEField(bunches.positions, self.t0)
                sumBFields+=fields.evaluateBField(bunches.positions, self.t0)
            self.mover.accelerate(bunches.momenta, sumEFields, sumBFields)
            self.mover.move(bunches.momenta, bunches.positions)

        self.t0 += self.dt


    def returnPtclData(self, filename):
        """
        Return the particle data
        :return:
        """
        # Take a half-step backward to synchronize ptcl position and momentum
        self.finalize()

        # Take a half-step forward to undo the work
        self.initialize()


    def returnFieldData(self, filename):
        """
        Return the field data
        :param filename:
        :return:
        """
        warnings.warn('returnFieldData is not currently supported')

        return 0