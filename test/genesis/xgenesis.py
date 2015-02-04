__author__ = 'swebb'

from RadTrack.genesis.rbXGenesis import RbXGenesis

test_plotter = RbXGenesis()

test_plotter.parse_output('xgenesis_testdata.out')

test_plotter.plot_data('z', 'Far Field')