from radtrack.util.RbMath import rpn, rpnVariableDict
import pytest

def test_rpn_success():
    testList = [("1 2 +", 3),
                ("100 10 /", 10),
                ("10 17 -", -7),
                ("6 9 *", 54),
                ("6 9 mult", 54),
                ("5 sqr", 25),
                ("16 sqr 4 3 -35 * * - sqrt -16 + 2 3 * /", 5.0/3.0),
                ("2 10x", 100),
                ("1 4 4 0 dist2", 5.0),
                ("1 2 2 minN", 1),
                ("1 2 3 3 maxN", 3),
                ("1.23", 1.23)]

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

    for walkTuple in os.walk(os.path.join(os.getcwd(), 'use_cases', 'elegant')):
        dirName = walkTuple[0]
        for fileName in [os.path.join(dirName, name) for name in walkTuple[2] if name.endswith('.lte')]:
            # Load rpn expressions from associated .ele files
            for eleFileName in [os.path.join(dirName, name) for name in walkTuple[2] if name.endswith('.ele')]:
                if 'template' in eleFileName.lower():
                    continue
                with open(eleFileName) as f:
                    insideRPNsection = False
                    insideQuote = False
                    for line in f:
                        line = line.strip()
                        if line == '&rpn_expression':
                            insideRPNsection = True
                        elif line == '&end' and insideRPNsection:
                            break
                        elif insideRPNsection:
                            if '"' in line:
                                if insideQuote:
                                    line = line.split('"')[0]
                                else:
                                    line = line.split('"')[1]
                                insideQuote = not insideQuote
                            if line:
                                try:
                                    rpn(line)
                                except ValueError:
                                    pass
            # Test that files load without errors
            elementDictionary, _ = fileImporter(fileName)

            for element in elementDictionary.values():
                if element.isBeamline():
                    continue
                for index, thing in enumerate(element.data):
                    if element.dataType[index].lower() == 'string':
                        continue
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
                        if thing:
                            print(rpnVariableDict)
                            print(fileName)
                            print(element.name)
                            print(type(element))
                            print(element.displayLine())
                            print(thing)
                            print(element.dataType[index])
                            assert False
