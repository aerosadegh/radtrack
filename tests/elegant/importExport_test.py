import os, glob, sys, subprocess
from itertools import izip_longest
import radtrack.beamlines.RbElegantElements as ele
import radtrack.beamlines.RbOpticalElements as opt
from radtrack.RbUtility import insideQuote

# QApplication needs to be instantiated to use QWidgets
# that can't be isolated from the rest of the application.
# If this isn't here, the test suite will simply halt with
# no messages.
#
# Note: make sure this is only called once during the entire test
# run. If more than one QApplications are created, python will
# crash at the end of the test suite.
from PyQt4 import QtGui
app = QtGui.QApplication(sys.argv)

exportEnd = '_export.lte'

elegantFilesLocation = os.path.join(os.getcwd(), 'deprecated', 'elegant')
elegantTestFile = os.path.join(elegantFilesLocation, 'elegantTest.ele')
particleFileList = glob.glob(os.path.join(elegantFilesLocation, 'beamlines', '*.lte'))

opticalFileList = glob.glob(
        os.path.join(os.getcwd(), 'deprecated', 'laser_transport', '*.rad'))

fileLists = [particleFileList, opticalFileList]
fileHandlers = [ele, opt]

elegantSimTemplate = '''&run_setup
    lattice = "%s",
    use_beamline = %s,
    default_order = 2,
    p_central_mev = 200.0,
    output = %%s.out,
    centroid = %%s.cen,
    sigma = %%s.sig,
    final = %%s.fin,
    parameters = %%s.param,
    magnets = %%s.mag,
    random_number_seed = 987654321,
    combine_bunch_statistics = 0,
    concat_order = 2,
    tracking_updates = 1,
    echo_lattice = 0,
&end

&run_control
    n_steps = 1,
    reset_rf_for_each_step = 1,
&end

&twiss_output
    matched = 0,
    concat_order = 3,
    beta_x = 5, alpha_x = 0,
    beta_y = 5, alpha_y = 0,
    output_at_each_step = 1,
    statistics = 1,
    concat_order = 3,
    filename = %%s.twi,
&end

&sdds_beam
    input = "%s",
&end

&matrix_output
    SDDS_output = %%s.mat,
    SDDS_output_order = 3,
    output_at_each_step = 1,
&end

&track
&end

&stop
&end'''

sddsFileName = os.path.join(elegantFilesLocation, 'bunches', 'elegantSimTest.sdds')
# Test that importing an .lte file and an exported version of that file
# result in the same elements being created
def test_import_export():
    for fileList, fileHandler in zip(fileLists, fileHandlers):
        for fileName in fileList:
            elementDictionary1, _ = fileHandler.fileImporter(fileName)
            exportFileName = os.path.splitext(fileName)[0] + exportEnd
            fileHandler.exportToFile(exportFileName, elementDictionary1)
            with open(exportFileName) as f:
                # Check that lines are not split inside quotes
                for lineNumber, line in enumerate(f.readlines()):
                    assert not insideQuote(line, len(line))

            elementDictionary2, _ = fileHandler.fileImporter(exportFileName)

            assert all([element1 == element2 for (element1, element2) in \
                    izip_longest(elementDictionary1.values(), elementDictionary2.values())])

            # Test elegant simulation on exported file
            try:
                longestLength = 0
                longest = None
                for beamline in [el for el in elementDictionary2.values() if el.isBeamline()]:
                    if len(beamline.data) > longestLength:
                        longest = beamline
                        longestLength = len(beamline.data)
                if fileList == particleFileList:
                    with open(elegantTestFile, 'w') as f:
                        f.write(elegantSimTemplate % (exportFileName, longest.name, sddsFileName))
                    assert subprocess.call(['elegant', elegantTestFile]) == 0
            finally:
                for fileName in glob.glob(os.path.splitext(elegantTestFile)[0] + '.*'):
                    os.remove(fileName)
                os.remove(exportFileName)

if __name__ == '__main__':
    test_import_export()
