__author__ = 'swebb'

from RadTrack.genesis.rbXGenesisTDep import RbXGenesisTDep

test_plotter = RbXGenesisTDep()
test_plotter.parse_output('xgenesis_testdata_tdep.out')

test_plotter.plot_data('s', 'Power')

test_plotter.plot_data('z', 'Far Field')