__author__ = 'swebb'

from RadTrack.genesis.rbXGenesisTInd import RbXGenesisTInd

test_plotter = RbXGenesisTInd()

test_plotter.parse_output('xgenesis_testdata.out')

test_plotter.set_ploterrors()

test_plotter.set_semilog()

test_plotter.plot_data('z', 'Bunching')