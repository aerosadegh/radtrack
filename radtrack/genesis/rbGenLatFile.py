"""
Copyright (c) 2015 RadiaBeam Technologies. All rights reserved

classes for genesis propagation
"""


__author__ = 'swebb'
__version__= '1.0'

import os

class GenLatFile(object):
    """
    Class for generating a properly formatted Genesis1.3 .lat file.
    """

    def __init__(self, filename, elems_dict, unit_length):
        """
        Class constructor

        Args:

            filename (string): the name of the file the lattice is to be
            exported as
            elems_dict (string): a dictionary of the elements for the
            genesis lattice
            unit_length (float): the unit length for genesis, usually the
            undulator period
        """

        self.elems_dict = elems_dict
        self.unit_length = unit_length
        self.filename = filename

    def write_lat_file(self):
        """
        Writes the lattice file specified in the constructor
        """

        # If the lattice file exists, remove it and start over
        if os.path.isfile(self.filename):
            os.remove(self.filename)

        lat = open(self.filename, 'w')

        header = '? VERSION = 1.0\n'
        header += '? UNITLENGTH = ' + str(self.unit_length) + '\n'
        lat.write(header)

        quad_label =  '#\n'
        quad_label += '# Quads:\n'
        quad_label += '# QF    dB/dx       L        space\n'
        quad_label += '#--------------------------------------\n'
        lat.write(quad_label)

        # Start with quads
        for quad_array in self.elems_dict['QF']:
            quadline = 'QF    '
            quadline += str(quad_array[0]) + '    '
            quadline += str(quad_array[1]) + '    '
            quadline += str(quad_array[2]) + '    \n'
            lat.write(quadline)

        und_label =  '#\n'
        und_label += '# Undulators:\n'
        und_label += '# AW    AW0       L        space\n'
        und_label += '#--------------------------------------\n'
        lat.write(und_label)

        # Add undulators
        for und_array in self.elems_dict['AW']:
            undline = 'AW    '
            undline += str(und_array[0]) + '    '
            undline += str(und_array[1]) + '    '
            undline += str(und_array[2]) + '    \n'
            lat.write(undline)

        lat.close()