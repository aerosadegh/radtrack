__author__ = 'swebb'

from matplotlib import pyplot as plt
import numpy as np

class fodocell:
    def __init__(self):
        self.f = False
        self.Lu = False
        self.transfer_matrix = np.matrix(np.zeros((4,4)))

    def make_fodo_cell(self, Lu, f):
        self.Lu = Lu
        self.f = f
        LuOf = self.Lu/self.f
        stability = 1.-0.5*LuOf**2
        if abs(stability) > 1.:
            print '!Warning -- FODO lattice may be unstable'

        self.transfer_matrix[0,0] = 1. - 0.5*LuOf**2
        self.transfer_matrix[0,1] = self.Lu*(2.+LuOf)
        self.transfer_matrix[1,0] = -0.5*LuOf*(1-0.5*LuOf)/self.f
        self.transfer_matrix[1,1] = 1. - 0.5*LuOf**2
        self.transfer_matrix[2,2] = 1. - 0.5*LuOf**2
        self.transfer_matrix[2,3] = self.Lu*(2.-LuOf)
        self.transfer_matrix[3,2] = -0.5*LuOf*(1+0.5*LuOf)/self.f
        self.transfer_matrix[3,3] = 1. - 0.5*LuOf**2

        print self.transfer_matrix

    def compute_average_beta(self):
        if self.f and self.Lu:
            print self.transfer_matrix
            phi = np.arccos(self.transfer_matrix[0,0])
            beta_average = 2*self.Lu/phi
            return beta_average
        else:
            print 'FODO cell not specified'
            return

    def get_transfer_map(self):
        return self.transfer_matrix

    def get_twiss_parameters(self):
        if self.f and self.Lu:
            phi = np.arccos(self.transfer_matrix[0,0])
            sinphi = np.sin(phi)
            betax  = self.transfer_matrix[0,1]/sinphi
            gammax = -self.transfer_matrix[1,0]/sinphi
            alphax = (self.transfer_matrix[0,0]-
                      self.transfer_matrix[1,1])/(2.*sinphi)

            betay  = self.transfer_matrix[2,3]/sinphi
            gammay = -self.transfer_matrix[3,2]/sinphi
            alphay = (self.transfer_matrix[2,2]-
                      self.transfer_matrix[3,3])/(2.*sinphi)

            print 'X beta, gamma, alpha =', betax, gammax, alphax
            print 'Y beta, gamma, alpha =', betay, gammay, alphay

            # Check Twiss parameters for consistency
            xcheck = (betax*gammax - alphax**2 - 1)
            print 'xcheck =', xcheck
            ycheck = (betay*gammay - alphay**2 - 1)
            print 'ycheck =', ycheck

            if abs(xcheck)>1.e-8 or abs(ycheck)>1.e-8:
                msg = 'Transfer matrix for FODO cell is not valid'
                raise Exception(msg)

            return betax, gammax, alphax, betay, gammay, alphay
        else:
            print 'Transfer matrix not specified'
            return

    def plot_beta_function(self):
        betax, gammax, alphax, betay, gammay, alphay = \
            self.get_twiss_parameters()
        avgbeta = self.compute_average_beta()

        sArray = np.arange(0, self.Lu, 0.1*self.Lu)

        betaXArray   = 1./gammax + gammax*(sArray - alphax/gammax)**2
        betaYArray   = 1./gammay + gammay*(sArray - alphay/gammay)**2
        betaXArray   = np.append(betaXArray, betaXArray[1:-1])
        betaYArray   = np.append(betaYArray, betaYArray[1:-1])

        print betaXArray

        sArray = np.append(sArray, sArray[1:-1]+self.Lu)
        print 's=',sArray

        plt.plot(sArray, betaXArray, label=r'$\beta_x$', c='b')
        plt.plot(sArray, betaYArray, label=r'$\beta_y$', c='r')

        plt.legend()

        plt.tight_layout()
        plt.show()