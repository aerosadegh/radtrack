__author__ = 'swebb'

from RadTrack.genesis.rbXGenesisTInd import RbXGenesis

test_plotter = RbXGenesis()

test_plotter.parse_output('xgenesis_testdata.out')

test_plotter.set_ploterrors()

test_plotter.set_semilog()

test_plotter.plot_data('z', 'Bunching')