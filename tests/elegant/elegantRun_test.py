import os, subprocess, glob, hashlib

import radtrack.util.resource as resource

if not os.getenv('RPN_DEFNS', None):
    os.environ['RPN_DEFNS'] = resource.filename('defns.rpn')


def test_elegant_run():
    elegantTestFile = 'LCLS21Feb08-testing.ele'
    beamLineFile = 'LCLS21Feb08-testing.lte'
    outputFile = os.path.splitext(elegantTestFile)[0] + '.out'
    comparisonFile = 'after.sdds'
    os.chdir('tests/elegant')

    assert subprocess.call(['elegant', elegantTestFile]) == 0

    with open(outputFile) as out, open(comparisonFile) as comp, open('before.sdds') as before:
        outSum = hashlib.md5(out.read()).hexdigest()
        compSum = hashlib.md5(comp.read()).hexdigest()
        beforeSum = hashlib.md5(before.read()).hexdigest()

    assert beforeSum != outSum
    assert outSum == compSum

    for fileName in glob.glob(os.path.splitext(elegantTestFile)[0] + '.*') + glob.glob('*.out'):
        if fileName not in [elegantTestFile, beamLineFile] and os.path.exists(fileName):
            os.remove(fileName)


if __name__ == '__main__':
    test_import_export()

