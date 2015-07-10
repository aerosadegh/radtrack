from radtrack.RbUtility import rpn
import pytest

def test_rpn_success():
    testList = [("1 2 +", 3),
                ("100 10 /", 10),
                ("10 17 -", -7),
                ("6 9 *", 54),
                ("5 sqr", 25),
                ("16 sqr 4 3 -35 * * - sqrt -16 + 2 3 * /", 5.0/3.0),
                ("2 10x", 100),
                ("1 4 4 0 dist2", 5.0),
                ("1 2 2 minN", 1),
                ("1 2 3 3 maxN", 3)]

    for test in testList:
        assert rpn(test[0]) == test[1]

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

        for element in elementDictionary.values():
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
                            thing.lower() not in ['', '+x', '+y', '-y', '-x', 't', 'w'] and \
                            all([x not in thing.lower() for x in \
                                ['coord', '%', 'centroid', 'ideal', 'param', 'sdds']]):
                        assert (fileName, ':', element.name, type(element), element.displayLine(), thing) == None
