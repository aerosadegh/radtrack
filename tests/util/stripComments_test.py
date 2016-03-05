from radtrack.util.stringTools import stripComments

def test_strip_comments():
    # Test 1 (Quoted comment character)
    inputString  = 'This is a test that "#" is treated as a comment. # This should not appear.'
    outputString = 'This is a test that "#" is treated as a comment.'

    stripString = stripComments(inputString, '#')
    assert stripString == outputString

    # Test 2 (Escaped comment character)
    inputString  = 'This is a test with an escaped \#. This sentence should appear. # This should not.'
    outputString = 'This is a test with an escaped \#. This sentence should appear.'

    stripString = stripComments(inputString, '#')
    assert stripString == outputString

    # Test 3 (No comment character)
    inputString  = 'This is an uncommented string.'
    outputString = inputString

    stripString = stripComments(inputString, '#')
    assert stripString == outputString
