__author__ = 'swebb'

from RadTrack.genesis.rbXGenesisTDep import RbXGenesisTDep

test_plotter = RbXGenesisTDep()
test_plotter.parse_output('xgenesis_testdata_tdep.out')
#test_plotter.parse_output('euvl.out')
#test_plotter.average_over_s()

test_plotter.plot_data('z', 'Power')