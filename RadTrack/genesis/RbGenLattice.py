"""
Copyright (c) 2015 RadiaBeam Technologies. All rights reserved

classes for genesis propagation
"""

__author__ = 'swebb'

import numpy as np

class GenLattice:

    def __init__(self):
        self.list = []


    def add_quadrupole(self, Kq, pos, length):
        """
        Add a quadrupole
        :param Kq:
        :param pos:
        :param length:
        :return:
        """
        # Add the quad to the list

        quadrupoleDict = {}
        quadrupoleDict['type'] = 'quadrupole'
        quadrupoleDict['Kq'] = Kq
        quadrupoleDict['pos'] = pos
        quadrupoleDict['length'] = length

        # Add the transfer map
        transfermap = np.zeros((4,4))
        Kl = np.sqrt(np.abs(Kq))*length
        if Kq > 0:
            transfermap[0,0] = np.cos(Kl)
            transfermap[0,1] = np.sin(Kl)/np.sqrt(np.abs(Kq))
            transfermap[1,0] = -np.sin(Kl)*np.sqrt(np.abs(Kq))
            transfermap[1,1] = np.cos(Kl)

            transfermap[2,2] = np.cosh(Kl)
            transfermap[2,3] = np.sinh(Kl)/np.sqrt(np.abs(Kq))
            transfermap[3,2] = np.sinh(Kl)*np.sqrt(np.abs(Kq))
            transfermap[3,3] = np.cosh(Kl)

        else:

            transfermap[0,0] = np.cosh(Kl)
            transfermap[0,1] = np.sinh(Kl)/np.sqrt(np.abs(Kq))
            transfermap[1,0] = np.sinh(Kl)*np.sqrt(np.abs(Kq))
            transfermap[1,1] = np.cosh(Kl)

            transfermap[2,2] = np.cos(Kl)
            transfermap[2,3] = np.sin(Kl)/np.sqrt(np.abs(Kq))
            transfermap[3,2] = -np.sin(Kl)*np.sqrt(np.abs(Kq))
            transfermap[3,3] = np.cos(Kl)

        quadrupoleDict['map'] = transfermap

        self.list.append(quadrupoleDict)


    def add_undulator(self, aw, pos, length):
        """
        Add an undulator
        :param aw:
        :param pos:
        :param length:
        :return:
        """

        # Add the undulator to the list

        undulatorDict = {}
        undulatorDict['type'] = 'undulator'
        undulatorDict['aw'] = aw
        undulatorDict['pos'] = pos
        undulatorDict['length'] = length

        # Ignoring undulator focusing for now...
        transfermap = np.identity(4)
        transfermap[0,1] = length
        transfermap[2,3] = length
        undulatorDict['map'] = transfermap

        self.list.append(undulatorDict)


    def add_drift(self, pos, length):
        """
        Add a drift
        :param pos:
        :param length:
        :return:
        """

        driftDict = {}
        driftDict['type'] = 'drift'
        driftDict['pos'] = pos
        driftDict['length'] = length

        transfermap = np.identity(4)
        transfermap[0,1] = length
        transfermap[2,3] = length
        driftDict['map'] = transfermap

        self.list.append(driftDict)


    def compute_beamline(self):
        """
        Compute the transfer matrix and Twiss parameters
        :return:
        """

        transfermap = np.identity(4)

        for elements in self.list:
            transfermap = np.dot(transfermap, elements['map'])

        phi_x = np.arccos(0.5*(transfermap[0,0] + transfermap[1,1]))
        phi_y = np.arccos(0.5*(transfermap[2,2] + transfermap[3,3]))

        print 'phi_x =', phi_x
        print 'phi_y =', phi_y

        betax = transfermap[0,1]/np.sin(phi_x)
        betay = transfermap[2,3]/np.sin(phi_y)
        alphax = 0.5*(transfermap[0,0]-transfermap[1,1])/np.sin(phi_x)
        alphay = 0.5*(transfermap[2,2]-transfermap[3,3])/np.sin(phi_y)

        return betax, alphax, betay, alphay, transfermap


    def compute_beta_func(self):

        betax, alphax, betay, alphay, transfermap = self.compute_beamline()
        gammax = (1.+alphax**2)/betax
        gammay = (1.+alphay**2)/betay
        twissx = np.array([betax, alphax, gammax])
        twissy = np.array([betay, alphay, gammay])
        betax_array = [betax]
        betay_array = [betay]
        s_position = [0.]

        for element in self.list:
            if element['type'] == 'quadrupole':
                map = element['map']
                Mtwiss = np.zeros((3,3))
                Mtwiss[0,0] = (map[0,0])**2
                Mtwiss[0,1] = -2.*map[0,0]*map[0,1]
                Mtwiss[0,2] = (map[0,1])**2
                Mtwiss[1,0] = -map[0,0]*map[1,0]
                Mtwiss[1,1] = map[0,0]*map[1,1]
                Mtwiss[1,2] = -map[0,1]*map[1,1]
                Mtwiss[2,0] = map[1,0]**2
                Mtwiss[2,1] = -2.*map[1,1]*map[1,0]
                Mtwiss[2,2] = (map[1,1])**2

                twissx = np.dot(Mtwiss, twissx)
                betax_array.append(twissx[0])

                Mtwiss[0,0] = (map[2,2])**2
                Mtwiss[0,1] = -2.*map[2,2]*map[2,3]
                Mtwiss[0,2] = (map[2,3])**2
                Mtwiss[1,0] = -map[2,2]*map[3,2]
                Mtwiss[1,1] = map[2,2]*map[3,3]
                Mtwiss[1,2] = -map[2,3]*map[3,3]
                Mtwiss[2,0] = map[3,2]**2
                Mtwiss[2,1] = -2.*map[3,3]*map[3,2]
                Mtwiss[2,2] = (map[3,3])**2

                twissy = np.dot(Mtwiss, twissy)
                betay_array.append(twissy[0])

                s_position.append(element['pos']+element['length'])

            # will need to add special behavior for undulator here
            else:
                ds = 0.01*element['length']
                my_position = 0.
                Mtwiss = np.identity(3)
                Mtwiss[0,1] = -2.
                Mtwiss[0,2] = ds**2
                Mtwiss[1,2] = -ds
                while my_position < element['length']:
                    twissx = np.dot(Mtwiss, twissx)
                    twissy = np.dot(Mtwiss, twissy)
                    my_position += ds
                    betax_array.append(twissx[0])
                    betay_array.append(twissy[0])
                    s_position.append(element['pos']+my_position)

        return betay_array, betay_array, s_position