from radtrack.RbUtility import rpn
import pytest

def test_rpn_success():
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
        assert c == b

# These tests should fail
def test_rpn_fail():
    for exp in ["1 + 2", "+ 1 2", "1 2 3", "a"]:
        with pytest.raises(ValueError):
            rpn(exp)

# Find RPN expressions in files that can't be processed
def test_rpn_files():
    import glob, sys, os
    from radtrack.beamlines.RbElegantElements import fileImporter

    alreadySeen = []
    for fileName in glob.glob(os.path.join(os.getcwd(), 'deprecated', 'elegant', 'beamlines', '*.lte')):
        # Test that files load without errors
        elementDictionary, _ = fileImporter(fileName)

        for element in loader.elementDictionary.values():
            if element.isBeamline():
                continue
            for thing in element.data:
                if thing in alreadySeen:
                    continue
                alreadySeen.append(thing)
                try:
                    answer = rpn(thing)
                    try:
                        if answer == float(thing):
                            continue # Just a number
                        else:
                            assert answer == float(thing) # 2 interpretations of value
                    except ValueError:
                        pass # thing is an unambiguous rpn expression
                except ValueError:
                    if thing != '' and \
                            thing not in ['', '"+X"', '"+Y"', '"-Y"', '"-X"'] and \
                            all([x not in thing.lower() for x in \
                                ['coord', '%', 'centroid', 'ideal', 'param', 'sdds']]) and \
                            thing.lower() not in ['"t"', '"w"']:
                        assert (fileName, ':', element.name, type(element), element.displayLine(), thing) == None
