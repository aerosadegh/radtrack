__author__ = 'swebb'

from RadTrack.genesis.rbXGenesisTDep import RbXGenesisTDep

test_plotter = RbXGenesisTDep()

print 'plotter generated'

test_plotter.parse_output('xgenesis_testdata_tdep.out')

print 'data parsed'

test_plotter.plot_data('s', 'Power')

print 'data plotted'