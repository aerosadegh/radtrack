print 'RPN Test ...'

from RbUtility import rpn

testList = []
testList.append(("1 2 +", 3))
testList.append(("100 10 /", 10))
testList.append(("10 17 -", -7))
testList.append(("6 9 *", 54))
testList.append(("5 sqr", 25))
testList.append(("16 sqr 4 3 -35 * * - sqrt -16 + 2 3 * /", 5.0/3.0))

for test in testList:
    a = test[0]
    b = test[1]
    c = rpn(a)
    if c != b:
        print a, '=', b, 'not', c
        raise Exception

# These tests should fail
try:
    for exp in ["1 + 2", "+ 1 2", "1 2 3", "a"]:
        rpn(exp)
except:
    pass
else:
    raise Exception("Invalid RPN Expression \"" + exp + "\"did not cause error.")

# Find RPN expressions in files that can't be processed
import glob, sys, os
import radtrack.rbcbt as rbcbt

currentDirectory = os.getcwd()
os.chdir('external\\elegant\\beamlines')

ignoreList = ['case_line.lte', 'name_test.lte']
fileList = [fileName for fileName in glob.glob('*.lte') if fileName not in ignoreList]

alreadySeen = []
try:
    for fileName in fileList:
        # Test that files load without errors
        loader = rbcbt.RbCbt('particle', None)
        loader.importFile(fileName)

        for element in loader.elementDictionary.values():
            if element.isBeamline():
                continue
            for thing in element.data:
                if thing in alreadySeen:
                    continue
                try:
                    answer = rpn(thing)
                    try:
                        if answer == float(thing):
                            continue
                        else:
                            print 'Conflict:', thing, '=', answer, 'or', float(thing)
                            raise Exception
                    except ValueError:
                        print fileName + ':', thing, '=', answer
                except ValueError:
                    if thing != '' and \
                            thing not in ['', '"+X"', '"+Y"', '"-Y"', '"-X"'] and \
                            all([x not in thing.lower() for x in \
                                ['coord', '%', 'centroid', 'ideal', 'param', 'sdds']]) and \
                            thing.lower() not in ['"t"', '"w"']:
                        print fileName, ':', element.name, type(element), element.displayLine(), thing
                        raise
                alreadySeen.append(thing)

    print 'Passed.'
finally:
    os.chdir(currentDirectory)
