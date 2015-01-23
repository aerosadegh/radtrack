__author__ = 'swebb'

from Radtrack.fel.fodocell import fodocell

focallength = 0.66
driftlength = 2.0

myfodocell = fodocell.fodocell()
myfodocell.make_fodo_cell(driftlength, focallength)

myfodocell.plot_beta_function()