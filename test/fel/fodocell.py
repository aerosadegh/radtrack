__author__ = 'swebb'

from RadTrack.fel.fodocell import fodocell

focallength = 0.66
driftlength = 1.0

myfodocell = fodocell()
myfodocell.make_fodo_cell(driftlength, focallength)

myfodocell.plot_beta_function()