"""
Python class to emulate XGenesis postprocessing of GENESIS1.3 simulations.
Parses the GENESIS .out file

Copyright (c) RadiaBeam Technologies, 2015. All rights reserved.
"""
__author__ = 'swebb'
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rc('text', usetex=True)
mpl.rc('font', size=14)


class RbXGenesisTInd:

    def __init__(self):
        self.file_open = False
        self.data_set = {}
        self.data_label = {}
        self.data_set['z']     = -1
        self.data_label['z'] = r'$z~\textrm{[m]}$'
        self.data_set['aw']    = -1
        self.data_label['aw'] = r'$a_w$'
        self.data_set['QF']    = -1
        self.data_label['QF'] = r'$\frac{dB}{dx}~\textrm{[T/m]}$'
        self.data_set['Power'] = -1
        self.data_label['Power'] = r'$P~\textrm{[W]}$'
        self.data_set['Increment'] = -1
        self.data_label['Increment'] = \
            r'$\frac{1}{P} \frac{dP}{dz}~\textrm{[m^{-1}]}$'
        self.data_set['p_mid'] = -1
        self.data_label['p_mid'] = '???'
        self.data_set['Phase'] = -1
        self.data_label['Phase'] = r'$\Phi~\textrm{[rad]}$'
        self.data_set['Rad. Size'] = -1
        self.data_label['Rad. Size'] = r'$\sigma_{\textrm{rad.}}~\textrm{[m]}$'
        self.data_set['Far Field'] = -1
        self.data_label['Far Field'] =\
            r'$\frac{dP}{d \Omega}~\textrm{[W/rad^2]}$'
        self.data_set['Energy'] = -1
        self.data_label['Energy'] = r'$\gamma - \gamma_0$'
        self.data_set['Energy Spread'] = -1
        self.data_label['Energy Spread'] = r'$\sigma_E~\textrm{[keV]}$'
        self.data_set['X Beam Size'] = -1
        self.data_label['X Beam Size'] = r'$\sigma_x~\textrm{[m]}$'
        self.data_set['Y Beam Size'] = -1
        self.data_label['Y Beam Size'] =  r'$\sigma_y~\textrm{[m]}$'
        self.data_set['X Centroid'] = -1
        self.data_label['X Centroid'] = r'$\langle x \rangle~\textrm{[m]}$'
        self.data_set['Y Centroid'] = -1
        self.data_label['Y Centroid'] = r'$\langle y \rangle~\textrm{[m]}$'
        self.data_set['Bunching'] = -1
        self.data_label['Bunching'] = r'$|\langle \exp(i \theta)\rangle|$'
        self.data_set['Error'] = -1
        self.data_label['Error'] = r'$\frac{\Delta P}{P}~\textrm{[\%]}$'

        self.semilog = False
        self.perrorbars = False


    def parse_output(self, filename):
        """
        Parse a GENESIS .out file
        :param filename:
        :return:
        """

        genesis_file = open(filename, 'r')
        line = genesis_file.readline()
        # Advance to find where the number of data entries are
        while not 'entries per record' in line:
            line = genesis_file.readline()
        num_steps = int(line.split()[0])
        for key in self.data_set.keys():
            self.data_set[key] = np.zeros(num_steps-1)

        first_three_keys = ['z', 'aw', 'QF']
        last_keys = ['Power', 'Increment', 'p_mid', 'Phase', 'Rad. Size',
                     'Energy', 'Bunching', 'X Beam Size', 'Y Beam Size',
                     'Error', 'X Centroid', 'Y Centroid', 'Energy Spread',
                     'Far Field']

        # Advance to the first set of data
        while not 'z[m]' in line:
            line = genesis_file.readline()


        # Read in the first three keys first
        for lineIdx in range(0, num_steps-1):
            line = genesis_file.readline()
            for idx in range(0, len(first_three_keys)-1):
                self.data_set[first_three_keys[idx]][lineIdx] = float(
                    line.split()[idx])

        while not 'power' in line:
            line = genesis_file.readline()

        for lineIdx in range(0, num_steps-1):
            line = genesis_file.readline()
            for idx in range(0, len(last_keys)):
                self.data_set[last_keys[idx]][lineIdx] = float(line.split()[
                    idx])

        genesis_file.close()


    def set_semilog(self):
        """
        Make the y-axis logarithmic for plotting
        :return:
        """
        if self.semilog == False:
            self.semilog = True
        else:
            self.semilog = False


    def set_ploterrors(self):
        """
        Plot error bars on the power
        :return:
        """
        if self.perrorbars == False:
            self.perrorbars = True
        else:
            self.perrorbars = False


    def plot_data(self, x_axis, y_axis):
        """
        Plot data from the keys given as arguments
        :param x_axis:
        :param y_axis:
        :return: plot
        """
        if not x_axis in self.data_set.keys():
            msg = 'Data type', x_axis, 'not recognized'
            Exception(msg)
        if not y_axis in self.data_set.keys():
            msg = 'Data type', y_axis, 'not recognized'
            Exception(msg)

        plt.plot(self.data_set[x_axis], self.data_set[y_axis])

        if self.perrorbars and y_axis == 'Power':
            power_error = self.data_set['Error']*self.data_set['Power']/100.
            plt.errorbar(self.data_set[x_axis], self.data_set[y_axis],
                            yerr=power_error, ecolor='r')

        if self.semilog:
            plt.yscale('log')

        plt.xlabel(self.data_label[x_axis])
        plt.ylabel(self.data_label[y_axis])
        plt.tight_layout()
        plt.show()


    def compute_saturation(self):

        place_max = np.argmax(self.data_set['Power'])

        saturation_power  = self.data_set['Power'][place_max]
        saturation_length = self.data_set['z'][place_max]

        return saturation_power, saturation_length