from radtrack.RbUtility import stripComments

def test_strip_comments():
    inputString  = 'This is a test that "#" is treated as a comment. # This should not appear.'
    outputString = 'This is a test that "#" is treated as a comment.'

    stripString = stripComments(inputString, '#')

    assert stripString == outputString
