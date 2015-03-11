__author__ = 'swebb'

from matplotlib import pyplot as plt
import numpy as np

class fodocell(object):
    def __init__(self, Lu, l, K):
        self.Lu = Lu
        self.quad_K = K
        self.quad_l = l
        rootK = np.sqrt(K)
        rootKl = rootK*l
        quadF = np.matrix(np.zeros((4,4)))
        quadF[0,0] = np.cos(rootKl)
        quadF[0,1] = np.sin(rootKl)/rootK
        quadF[1,0] = -rootK*np.sin(rootKl)
        quadF[1,1] = np.cos(rootKl)
        quadF[2,2] = np.cosh(rootKl)
        quadF[2,3] = np.sinh(rootKl)/rootK
        quadF[3,2] = rootK*np.sinh(rootKl)
        quadF[3,3] = np.cosh(rootKl)

        quadD = np.matrix(np.zeros((4,4)))
        quadD[0,0] = np.cosh(rootKl)
        quadD[0,1] = np.sinh(rootKl)/rootK
        quadD[1,0] = rootK*np.sinh(rootKl)
        quadD[1,1] = np.cosh(rootKl)
        quadD[2,2] = np.cos(rootKl)
        quadD[2,3] = np.sin(rootKl)/rootK
        quadD[3,2] = -rootK*np.sin(rootKl)
        quadD[3,3] = np.cos(rootKl)

        drift = np.matrix(np.zeros((4,4)))
        drift[0,0] = 1.
        drift[0,1] = Lu
        drift[1,0] = 0.
        drift[1,1] = 1.
        drift[2,2] = 1.
        drift[2,3] = Lu
        drift[3,2] = 0.
        drift[3,3] = 1.

        self.transfer_matrix = np.dot(quadD, drift)
        self.transfer_matrix = np.dot(drift, self.transfer_matrix)
        self.transfer_matrix = np.dot(quadF, self.transfer_matrix)

        #print 'FODO self.transfer_matrix =', self.transfer_matrix
        stability = 0.5*(self.transfer_matrix[0,0]+self.transfer_matrix[1,1])
        if abs(stability) > 1.:
            print '!Warning -- FODO lattice may be unstable in the horizontal'
        stability = 0.5*(self.transfer_matrix[2,2]+self.transfer_matrix[3,3])
        if abs(stability) > 1.:
            print '!Warning -- FODO lattice may be unstable in the vertical'

    def compute_phase_advance(self):
        phix = np.arccos(0.5*self.transfer_matrix[2,2]+
                        0.5*self.transfer_matrix[3,3])
        phiy = np.arccos(0.5*self.transfer_matrix[0,0]+
                        0.5*self.transfer_matrix[1,1])
        return phix, phiy

    def compute_average_beta(self):
        print self.transfer_matrix
        phix, phiy = self.compute_phase_advance()
        beta_average = (self.Lu+self.quad_l)/phix+(self.Lu+self.quad_l)/phiy
        return beta_average

    def get_transfer_map(self):
        return self.transfer_matrix

    def get_twiss_parameters(self):
        phix, phiy = self.compute_phase_advance()
        sinphix = np.sin(phix)
        sinphiy = np.sin(phiy)
        betay  = self.transfer_matrix[0,1]/sinphiy
        gammay = -self.transfer_matrix[1,0]/sinphiy
        alphay = (self.transfer_matrix[0,0]-
                  self.transfer_matrix[1,1])/(2.*sinphiy)

        betax  = self.transfer_matrix[2,3]/sinphix
        gammax = -self.transfer_matrix[3,2]/sinphix
        alphax = (self.transfer_matrix[2,2]-
                  self.transfer_matrix[3,3])/(2.*sinphix)

        # Check Twiss parameters for consistency
        xcheck = (betax*gammax - alphax**2 - 1)
        ycheck = (betay*gammay - alphay**2 - 1)

        if abs(xcheck)>1.e-8 or abs(ycheck)>1.e-8:
            msg = 'Transfer matrix for FODO cell is not valid'
            raise Exception(msg)

        return betax, gammax, alphax, betay, gammay, alphay

    def plot_beta_function(self):
        betax, gammax, alphax, betay, gammay, alphay = \
            self.get_twiss_parameters()
        avgbeta = self.compute_average_beta()

        sArray = np.arange(0, self.Lu, 0.1*self.Lu)

        #After passing through the thin quad, the focusing changes the Twiss
        #  parameters
        gammax += 2.*alphax/self.f + betax/self.f**2
        alphax += betax/self.f
        gammay += -2.*alphay/self.f + betay/self.f**2
        alphay += -betay/self.f

        betaXArray   = 1./gammax + gammax*(sArray - alphax/gammax)**2
        betaYArray   = 1./gammay + gammay*(sArray - alphay/gammay)**2

        tailXArray = betaXArray[::-1]
        tailYArray = betaYArray[::-1]
        betaXArray   = np.append(betaXArray, tailXArray[1::])
        betaYArray   = np.append(betaYArray, tailYArray[1::])

        sArray = np.append(sArray, sArray[1::]+self.Lu)

        plt.plot(sArray, betaXArray, label=r'$\beta_x$', c='b')
        plt.plot(sArray, betaYArray, label=r'$\beta_y$', c='r')

        plt.legend()

        plt.tight_layout()
        plt.show()
