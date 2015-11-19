import os, glob, subprocess, string
import radtrack.beamlines.RbElegantElements as ele
import radtrack.beamlines.RbOpticalElements as opt
from radtrack.RbUtility import insideQuote

import radtrack.util.resource as resource
if not os.getenv('RPN_DEFNS', None):
    os.environ['RPN_DEFNS'] = resource.filename('defns.rpn')

exportEnd = '_export.lte'

elegantFilesLocation = os.path.join(os.getcwd(), 'deprecated', 'elegant')
elegantTestFile = os.path.join(elegantFilesLocation, 'elegantTest.ele')
particleFileList = glob.glob(os.path.join(elegantFilesLocation, 'beamlines', '*.lte'))
excludedList = ['dtSweep.lte',
                'fourDipoleCSR.lte',
                'lattice.lte',
                'multiple.lte',
                'mv15-c5-v2-ring.lte']

opticalFileList = glob.glob(os.path.join(os.getcwd(), 'deprecated', 'laser_transport', '*.rad'))

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
            elementDictionary1, default1 = fileHandler.fileImporter(fileName)
            exportFileName = os.path.splitext(fileName)[0] + exportEnd
            fileHandler.exportToFile(exportFileName, elementDictionary1, default1)
            with open(exportFileName) as f:
                # Check that lines are not split inside quotes
                for line in f:
                    assert not insideQuote(line, len(line) - 1)

            elementDictionary2, default2 = fileHandler.fileImporter(exportFileName)

            if not elementDictionary1 == elementDictionary2:
                for name in elementDictionary1:
                    e1 = elementDictionary1[name]
                    e2 = elementDictionary2[name]
                    if not e1 == e2:
                        print fileName
                        print name
                        if not e1.isBeamline():
                            assert compareNormalizedElementData(e1, e2)
                        else:
                            for index in range(max(len(e1.data), len(e2.data))):
                                assert compareNormalizedElementData(e1.data[index], e2.data[index])
            assert default1 == default2

            # Test elegant simulation on exported file
            # Choose the beam line with the most elements for testing
            try:
                if os.path.basename(fileName) in excludedList:
                    continue

                longestLength = 0
                longest = None
                for beamline in [el for el in elementDictionary2.values() if el.isBeamline()]:
                    length = beamline.getNumberOfElements()
                    if length > longestLength:
                        longest = beamline
                        longestLength = length
                if fileList == particleFileList:
                    with open(elegantTestFile, 'w') as f:
                        f.write(elegantSimTemplate % (exportFileName, longest.name, sddsFileName))
                    assert subprocess.call(['elegant', elegantTestFile]) == 0
            finally:
                for fileName in glob.glob(os.path.splitext(elegantTestFile)[0] + '.*') \
                        + glob.glob('*.out') \
                        + [exportFileName]:
                    os.remove(fileName)

def compareNormalizedElementData(e1, e2):
    print e1.data
    print e2.data
    for thing1, thing2 in zip(e1.data, e2.data):
        for thing in [thing1, thing2]:
            thing = string.replace(thing, '-0', '-')
            if thing.startswith('.'):
                thing = '0' + thing
        if thing1 != thing2 and float(thing1) != float(thing2):
            return False
    return True


if __name__ == '__main__':
    test_import_export()
